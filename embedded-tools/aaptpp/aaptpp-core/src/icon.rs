use crate::archive::ZipArchive;
use crate::detect;
use crate::error::{AaptError, Result};
use crate::manifest::{parse_manifest, parse_manifest_flexible, Value};
use crate::resources::{parse_resources, pick_best_icon_path, resolve_resource_key, scan_best_icon_path};

macro_rules! dbglog {
    ($($arg:tt)*) => {
        if std::env::var("AAPT_DEBUG").is_ok() {
            eprintln!("[DEBUG] {}", format!($($arg)*));
        }
    };
}
use crate::vector_drawable::{encode_png, render_vector_icon_from_apk};
use flate2::read::ZlibDecoder;
use std::io::Read;

pub fn extract_best_icon<R: std::io::Read + std::io::Seek>(
    za: &mut ZipArchive<R>,
    prefer_round: bool,
) -> Result<Vec<u8>> {
    let entries: Vec<String> = za.entry_names().iter().map(|s| s.to_string()).collect();

    if entries.iter().any(|e| e.starts_with("base/")) {
        return extract_icon_aab(za, &entries, prefer_round);
    }

    let is_container = !entries.iter().any(|e| e == "AndroidManifest.xml")
        && entries.iter().any(|e| e.ends_with(".apk"));
    if is_container {
        return extract_icon_container(za, &entries, prefer_round);
    }

    extract_icon_apk(za, &entries, None, prefer_round)
}

pub fn extract_best_icon_with_aapt_path<R: std::io::Read + std::io::Seek>(
    za: &mut ZipArchive<R>,
    aapt_icon_path: Option<&str>,
    prefer_round: bool,
) -> Result<Vec<u8>> {
    let entries: Vec<String> = za.entry_names().iter().map(|s| s.to_string()).collect();

    if entries.iter().any(|e| e.starts_with("base/")) {
        return extract_icon_aab(za, &entries, prefer_round);
    }

    let is_container = !entries.iter().any(|e| e == "AndroidManifest.xml")
        && entries.iter().any(|e| e.ends_with(".apk"));
    if is_container {
        return extract_icon_container(za, &entries, prefer_round);
    }

    extract_icon_apk(za, &entries, aapt_icon_path, prefer_round)
}

/// Extract a top-level icon.png from a container (XAPK/APKM/APKS).
pub fn extract_container_top_icon<R: std::io::Read + std::io::Seek>(za: &mut ZipArchive<R>) -> Result<Vec<u8>> {
    let entries: Vec<String> = za.entry_names().iter().map(|s| s.to_string()).collect();

    if entries.iter().any(|e| e == "icon.png") {
        if let Ok(bytes) = za.read_entry("icon.png") {
            if is_image_bytes(&bytes) {
                return Ok(bytes);
            }
        }
    }

    if entries.iter().any(|e| e == "manifest.json") {
        if let Ok(json_bytes) = za.read_entry("manifest.json") {
            if let Ok(val) = serde_json::from_slice::<serde_json::Value>(&json_bytes) {
                if let Some(icon_path) = val.get("icon").and_then(|v| v.as_str()) {
                    if entries.iter().any(|e| e == icon_path) {
                        if let Ok(bytes) = za.read_entry(icon_path) {
                            if is_image_bytes(&bytes) {
                                return Ok(bytes);
                            }
                        }
                    }
                }
            }
        }
    }

    Err(AaptError::NotFound("no top-level icon in container".into()))
}

fn is_image_bytes(bytes: &[u8]) -> bool {
    bytes.len() >= 8
        && (&bytes[0..4] == b"\x89PNG" || &bytes[0..2] == b"\xff\xd8" || &bytes[0..4] == b"RIFF")
}

fn extract_icon_container<R: std::io::Read + std::io::Seek>(
    za: &mut ZipArchive<R>,
    entries: &[String],
    prefer_round: bool,
) -> Result<Vec<u8>> {
    if entries.iter().any(|e| e == "icon.png") {
        if let Ok(bytes) = za.read_entry("icon.png") {
            if is_image_bytes(&bytes) {
                return Ok(bytes);
            }
        }
    }

    if entries.iter().any(|e| e == "manifest.json") {
        if let Ok(json_bytes) = za.read_entry("manifest.json") {
            if let Ok(val) = serde_json::from_slice::<serde_json::Value>(&json_bytes) {
                if let Some(icon_path) = val.get("icon").and_then(|v| v.as_str()) {
                    if let Ok(bytes) = za.read_entry(icon_path) {
                        if is_image_bytes(&bytes) {
                            return Ok(bytes);
                        }
                    }
                }
            }
        }
    }

    if let Some(base) = detect::base_apk_member(entries) {
        if let Ok(bytes) = za.read_entry(&base) {
            let mut inner = ZipArchive::new(std::io::Cursor::new(bytes))?;
            return extract_best_icon(&mut inner, prefer_round);
        }
    }

    Err(AaptError::NotFound("no icon found in container".into()))
}

fn extract_icon_apk<R: std::io::Read + std::io::Seek>(
    za: &mut ZipArchive<R>,
    entries: &[String],
    aapt_icon_path: Option<&str>,
    prefer_round: bool,
) -> Result<Vec<u8>> {
    if !entries.iter().any(|e| e == "AndroidManifest.xml") {
        return Err(AaptError::NotFound("AndroidManifest.xml".into()));
    }

    // Tier 1: AAPT-derived icon path (from dump badging)
    if let Some(path) = aapt_icon_path {
        dbglog!("extract_icon_apk Tier1: aapt_icon_path='{}'", path);
        if path.ends_with(".xml") {
            if entries.iter().any(|e| e == path) {
                if let Ok(bytes) = za.read_entry(path) {
                    match render_vector_icon_from_apk(&bytes, entries, za, None) {
                        Ok(png) => return Ok(png),
                        Err(e) => dbglog!("Tier1 vector render failed: {}", e),
                    }
                }
            }
        } else if entries.iter().any(|e| e == path) {
            if let Ok(bytes) = za.read_entry(path) {
                if is_image_bytes(&bytes) {
                    return Ok(bytes);
                }
            }
        }
    }

    // Tier 2: Parse manifest, resolve icon resource ID
    if let Ok(manifest_buf) = za.read_entry("AndroidManifest.xml") {
        if let Ok(manifest) = parse_manifest(&manifest_buf) {
            let rid = if prefer_round {
                manifest.round_icon_res.or(manifest.icon_res)
            } else {
                manifest.icon_res.or(manifest.round_icon_res)
            };

            if let Some(rid) = rid {
                if let Some(png) = resolve_icon_via_resources(rid, entries, za) {
                    return Ok(png);
                }
            }

            // Also try vector drawable resolution via manifest icon path
            if let Some(path) = manifest.icon_res.and_then(|_| {
                resolve_icon_path_from_manifest(&manifest, entries, za)
            }) {
                dbglog!("extract_icon_apk Tier2: vector_path='{}'", path);
                if path.ends_with(".xml") {
                    if let Ok(bytes) = za.read_entry(&path) {
                        match render_vector_icon_from_apk(&bytes, entries, za, None) {
                            Ok(png) => return Ok(png),
                            Err(e) => dbglog!("Tier2 vector render failed: {}", e),
                        }
                    }
                } else if let Ok(bytes) = za.read_entry(&path) {
                    if is_image_bytes(&bytes) {
                        return Ok(bytes);
                    }
                }
            }
        }
    }

    // Tier 3: Try well-known launcher icon names
    let common = ["ic_launcher", "launcher_icon", "app_icon", "ic_launcher_foreground"];
    for c in &common {
        if let Some(p) = pick_best_icon_path(c, entries) {
            if let Ok(bytes) = za.read_entry(&p) {
                if is_image_bytes(&bytes) {
                    return Ok(bytes);
                }
            }
        }
    }

    // Tier 4: Scan ALL PNG entries for any launcher-like icon
    if let Some(png) = scan_best_icon_path(entries) {
        if let Ok(bytes) = za.read_entry(&png) {
            if is_image_bytes(&bytes) {
                return Ok(bytes);
            }
        }
    }

    Err(AaptError::NotFound("no suitable icon PNG found".into()))
}

fn resolve_icon_path_from_manifest<R: std::io::Read + std::io::Seek>(
    manifest: &crate::manifest::Manifest,
    entries: &[String],
    za: &mut ZipArchive<R>,
) -> Option<String> {
    // Try to resolve icon resource ID through resources.arsc
    let rid = manifest.icon_res.or(manifest.round_icon_res)?;
    if !entries.iter().any(|e| e == "resources.arsc") {
        return None;
    }
    let arsc_buf = za.read_entry("resources.arsc").ok()?;
    let table = parse_resources(&arsc_buf).ok()?;
    let key = resolve_resource_key(&table, rid)?;
    pick_best_icon_path(&key, entries)
}

fn resolve_icon_via_resources<R: std::io::Read + std::io::Seek>(
    rid: u32,
    entries: &[String],
    za: &mut ZipArchive<R>,
) -> Option<Vec<u8>> {
    if !entries.iter().any(|e| e == "resources.arsc") {
        return None;
    }
    let arsc_buf = za.read_entry("resources.arsc").ok()?;
    let table = parse_resources(&arsc_buf).ok()?;
    let key = resolve_resource_key(&table, rid)?;
    let path = pick_best_icon_path(&key, entries)?;
    let bytes = za.read_entry(&path).ok()?;
    if is_image_bytes(&bytes) {
        Some(bytes)
    } else {
        None
    }
}

fn extract_icon_aab<R: std::io::Read + std::io::Seek>(
    za: &mut ZipArchive<R>,
    entries: &[String],
    prefer_round: bool,
) -> Result<Vec<u8>> {
    let mname = entries
        .iter()
        .find(|e| e.ends_with("manifest/AndroidManifest.xml"))
        .or_else(|| entries.iter().find(|e| e.as_str() == "base/AndroidManifest.xml"))
        .cloned()
        .ok_or_else(|| AaptError::NotFound("AAB manifest not found".into()))?;

    let manifest_buf = za.read_entry(&mname)?;
    let manifest = parse_manifest_flexible(&manifest_buf)?;

    let app = manifest.raw.find("application");
    let icon_name = if prefer_round { "roundIcon" } else { "icon" };
    let fallback = if prefer_round { "icon" } else { "roundIcon" };

    let attr = manifest
        .raw
        .attr(icon_name)
        .or_else(|| app.and_then(|a| a.attr(icon_name)))
        .or_else(|| manifest.raw.attr(fallback))
        .or_else(|| app.and_then(|a| a.attr(fallback)));

    if let Some(attr) = attr {
        let rid = match &attr.value {
            Value::Resource(r) => Some(*r),
            Value::Str(s) => {
                if s.starts_with("@res/") {
                    u32::from_str_radix(s.trim_start_matches("@res/").trim_start_matches("0x"), 16).ok()
                } else {
                    None
                }
            }
            _ => None,
        };

        if let Some(rid) = rid {
            if let Some(png) = resolve_icon_for_aab(rid, entries, za) {
                return Ok(png);
            }
        }

        if let Value::Str(s) = &attr.value {
            let key = s.rsplit('/').next().unwrap_or(s).trim_start_matches('@');
            if !key.is_empty() {
                let aab_entries: Vec<String> = entries
                    .iter()
                    .map(|e| e.strip_prefix("base/").map(|s| s.to_string()).unwrap_or_else(|| e.clone()))
                    .collect();
                if let Some(path) = pick_best_icon_path(key, &aab_entries) {
                    let full = if path.starts_with("base/") {
                        path
                    } else {
                        format!("base/{}", path)
                    };
                    if let Ok(bytes) = za.read_entry(&full) {
                        if is_image_bytes(&bytes) {
                            return Ok(bytes);
                        }
                    }
                }
            }
        }
    }

    // Fallback: try common names in AAB
    let common = ["ic_launcher", "launcher_icon", "app_icon"];
    let aab_entries_stripped: Vec<String> = entries
        .iter()
        .map(|e| e.strip_prefix("base/").map(|s| s.to_string()).unwrap_or_else(|| e.clone()))
        .collect();
    for c in &common {
        if let Some(path) = pick_best_icon_path(c, &aab_entries_stripped) {
            let full = if path.starts_with("base/") { path } else { format!("base/{}", path) };
            if let Ok(bytes) = za.read_entry(&full) {
                if is_image_bytes(&bytes) {
                    return Ok(bytes);
                }
            }
        }
    }

    // Fallback: scan all PNG entries in AAB
    let png_entries: Vec<String> = entries.iter()
        .filter(|e| e.ends_with(".png") || e.ends_with(".webp"))
        .cloned()
        .collect();
    // Prefer mipmap/drawable, larger sizes
    let mut best: Option<(String, usize)> = None;
    for e in &png_entries {
        let lower = e.to_lowercase();
        let score = if lower.contains("mipmap") || lower.contains("drawable") {
            if lower.contains("launcher") || lower.contains("icon") { 100 } else { 50 }
        } else {
            10
        };
        // Extract size from path (e.g., xxxhdpi > xxhdpi > xhdpi)
        let size_score = if lower.contains("xxxhdpi") { 5 }
            else if lower.contains("xxhdpi") { 4 }
            else if lower.contains("xhdpi") { 3 }
            else if lower.contains("hdpi") { 2 }
            else if lower.contains("mdpi") { 1 }
            else { 0 };
        let total = score + size_score;
        if total > best.as_ref().map(|b| b.1).unwrap_or(0) {
            best = Some((e.clone(), total));
        }
    }
    if let Some((path, _)) = best {
        if let Ok(bytes) = za.read_entry(&path) {
            if is_image_bytes(&bytes) || bytes.len() >= 4 && &bytes[0..4] == b"RIFF" {
                return Ok(bytes);
            }
        }
    }

    Err(AaptError::NotFound("no suitable icon PNG found in AAB".into()))
}

fn resolve_icon_for_aab<R: std::io::Read + std::io::Seek>(
    rid: u32,
    entries: &[String],
    za: &mut ZipArchive<R>,
) -> Option<Vec<u8>> {
    let arsc_name = entries.iter().find(|e| e.ends_with("resources.arsc")).cloned().unwrap_or_default();
    if !arsc_name.is_empty() {
        if let Ok(arsc_buf) = za.read_entry(&arsc_name) {
            if let Ok(table) = parse_resources(&arsc_buf) {
                if let Some(key) = resolve_resource_key(&table, rid) {
                    let aab_entries: Vec<String> = entries
                        .iter()
                        .map(|e| e.strip_prefix("base/").map(|s| s.to_string()).unwrap_or_else(|| e.clone()))
                        .collect();
                    if let Some(path) = pick_best_icon_path(&key, &aab_entries) {
                        let full = if path.starts_with("base/") { path } else { format!("base/{}", path) };
                        if let Ok(bytes) = za.read_entry(&full) {
                            if is_image_bytes(&bytes) {
                                return Some(bytes);
                            }
                        }
                    }
                }
            }
        }
    }
    None
}

// ──────────────────────────────────────────────
// Multi-size ICO generation
// ──────────────────────────────────────────────

/// Decode a PNG to raw RGBA bytes.
/// Supports color types: 6 (RGBA), 2 (RGB), 3 (indexed with transparency).
fn png_to_rgba(data: &[u8]) -> Result<(Vec<u8>, usize, usize)> {
    if data.len() < 8 || &data[0..4] != b"\x89PNG" {
        return Err(AaptError::Parse("not a PNG".into()));
    }
    let mut pos = 8;
    let mut w = 0u32;
    let mut h = 0u32;
    let mut bit_depth = 0u8;
    let mut color_type = 0u8;
    let mut idat_data = Vec::new();
    let mut palette = Vec::new();
    let mut trns = Vec::new();

    while pos + 8 <= data.len() {
        let chunk_len = u32::from_be_bytes([data[pos], data[pos+1], data[pos+2], data[pos+3]]) as usize;
        let chunk_type = &data[pos+4..pos+8];
        let chunk_data = &data[pos+8..pos+8+chunk_len];
        if chunk_type == b"IHDR" && chunk_data.len() >= 13 {
            w = u32::from_be_bytes([chunk_data[0], chunk_data[1], chunk_data[2], chunk_data[3]]);
            h = u32::from_be_bytes([chunk_data[4], chunk_data[5], chunk_data[6], chunk_data[7]]);
            bit_depth = chunk_data[8];
            color_type = chunk_data[9];
        } else if chunk_type == b"IDAT" {
            idat_data.extend_from_slice(chunk_data);
        } else if chunk_type == b"PLTE" {
            palette = chunk_data.to_vec();
        } else if chunk_type == b"tRNS" {
            trns = chunk_data.to_vec();
        } else if chunk_type == b"IEND" {
            break;
        }
        pos += 12 + chunk_len;
    }

    if w == 0 || h == 0 {
        return Err(AaptError::Parse("PNG: invalid dimensions".into()));
    }

    // Decompress IDAT data
    let mut decoder = ZlibDecoder::new(idat_data.as_slice());
    let mut raw = Vec::new();
    decoder.read_to_end(&mut raw).map_err(|e| AaptError::Io(e))?;

    let bytes_per_pixel = match color_type {
        6 => 4, // RGBA
        2 => 3, // RGB
        3 => 1, // Indexed
        _ => return Err(AaptError::Unsupported(format!("PNG color type {}", color_type))),
    };

    let stride = 1 + w as usize * bytes_per_pixel;
    let expected = stride * h as usize;
    if raw.len() < expected {
        return Err(AaptError::Parse("PNG: raw data truncated".into()));
    }

    let mut rgba = vec![0u8; w as usize * h as usize * 4];
    for y in 0..h as usize {
        let filter = raw[y * stride];
        let row_start = y * stride + 1;
        for x in 0..w as usize {
            let src_idx = row_start + x * bytes_per_pixel;
            let dst_idx = (y * w as usize + x) * 4;
            match color_type {
                6 => {
                    rgba[dst_idx] = raw[src_idx];
                    rgba[dst_idx+1] = raw[src_idx+1];
                    rgba[dst_idx+2] = raw[src_idx+2];
                    rgba[dst_idx+3] = raw[src_idx+3];
                }
                2 => {
                    rgba[dst_idx] = raw[src_idx];
                    rgba[dst_idx+1] = raw[src_idx+1];
                    rgba[dst_idx+2] = raw[src_idx+2];
                    rgba[dst_idx+3] = 255;
                }
                3 => {
                    let idx = raw[src_idx] as usize;
                    if idx * 3 + 2 < palette.len() {
                        rgba[dst_idx] = palette[idx * 3];
                        rgba[dst_idx+1] = palette[idx * 3 + 1];
                        rgba[dst_idx+2] = palette[idx * 3 + 2];
                        rgba[dst_idx+3] = if idx < trns.len() { trns[idx] } else { 255 };
                    } else {
                        rgba[dst_idx] = 0;
                        rgba[dst_idx+1] = 0;
                        rgba[dst_idx+2] = 0;
                        rgba[dst_idx+3] = 0;
                    }
                }
                _ => {}
            }
        }
        // Apply filter: only Sub(1), Up(2), Average(3), Paeth(4) reconstruction needed
        if filter == 1 {
            for x in 1..w as usize {
                let idx = (y * w as usize + x) * 4;
                let left = (y * w as usize + x - 1) * 4;
                for c in 0..4 {
                    rgba[idx + c] = rgba[idx + c].wrapping_add(rgba[left + c]);
                }
            }
        } else if filter == 2 {
            if y > 0 {
                for x in 0..w as usize {
                    let idx = (y * w as usize + x) * 4;
                    let up = ((y - 1) * w as usize + x) * 4;
                    for c in 0..4 {
                        rgba[idx + c] = rgba[idx + c].wrapping_add(rgba[up + c]);
                    }
                }
            }
        } else if filter == 3 {
            for x in 0..w as usize {
                let idx = (y * w as usize + x) * 4;
                let left_val = if x > 0 {
                    let left = (y * w as usize + x - 1) * 4;
                    let mut lv = [0u8; 4];
                    lv.copy_from_slice(&rgba[left..left+4]);
                    lv
                } else { [0u8; 4] };
                let up_val = if y > 0 {
                    let up = ((y - 1) * w as usize + x) * 4;
                    let mut uv = [0u8; 4];
                    uv.copy_from_slice(&rgba[up..up+4]);
                    uv
                } else { [0u8; 4] };
                for c in 0..4 {
                    let avg = (left_val[c] as u16 + up_val[c] as u16) / 2;
                    rgba[idx + c] = rgba[idx + c].wrapping_add(avg as u8);
                }
            }
        } else if filter == 4 {
            for x in 0..w as usize {
                let idx = (y * w as usize + x) * 4;
                let mut left_val = [0u8; 4];
                if x > 0 { left_val.copy_from_slice(&rgba[(y * w as usize + x - 1) * 4..][..4]); }
                let mut up_val = [0u8; 4];
                if y > 0 { up_val.copy_from_slice(&rgba[((y-1) * w as usize + x) * 4..][..4]); }
                let mut upleft_val = [0u8; 4];
                if x > 0 && y > 0 { upleft_val.copy_from_slice(&rgba[((y-1) * w as usize + x - 1) * 4..][..4]); }
                for c in 0..4 {
                    let p = paeth_predict(left_val[c] as i16, up_val[c] as i16, upleft_val[c] as i16);
                    rgba[idx + c] = rgba[idx + c].wrapping_add(p as u8);
                }
            }
        }
    }

    Ok((rgba, w as usize, h as usize))
}

#[inline]
fn paeth_predict(a: i16, b: i16, c: i16) -> i16 {
    let p = a + b - c;
    let pa = (p - a).abs();
    let pb = (p - b).abs();
    let pc = (p - c).abs();
    if pa <= pb && pa <= pc { a } else if pb <= pc { b } else { c }
}

/// Nearest-neighbor downscale RGBA to target size.
fn scale_rgba(rgba: &[u8], src_w: usize, src_h: usize, dst_w: usize, dst_h: usize) -> Vec<u8> {
    let mut out = vec![0u8; dst_w * dst_h * 4];
    for dy in 0..dst_h {
        for dx in 0..dst_w {
            let sx = dx * src_w / dst_w;
            let sy = dy * src_h / dst_h;
            let si = (sy * src_w + sx) * 4;
            let di = (dy * dst_w + dx) * 4;
            out[di..di+4].copy_from_slice(&rgba[si..si+4]);
        }
    }
    out
}

fn jpeg_dimensions(data: &[u8]) -> Result<(u16, u16)> {
    let mut pos = 2;
    loop {
        if pos + 4 > data.len() {
            return Err(AaptError::Parse("JPEG: unexpected end".into()));
        }
        if data[pos] != 0xFF {
            return Err(AaptError::Parse("JPEG: expected marker".into()));
        }
        let marker = data[pos + 1];
        if marker == 0xC0 || marker == 0xC1 || marker == 0xC2 {
            if pos + 9 > data.len() {
                return Err(AaptError::Parse("JPEG: SOF truncated".into()));
            }
            let height = u16::from_be_bytes([data[pos + 5], data[pos + 6]]);
            let width = u16::from_be_bytes([data[pos + 7], data[pos + 8]]);
            return Ok((width, height));
        }
        if marker == 0xD9 {
            return Err(AaptError::Parse("JPEG: no SOF marker found".into()));
        }
        if marker == 0xDA {
            return Err(AaptError::Parse("JPEG: SOS before SOF".into()));
        }
        let seg_len = u16::from_be_bytes([data[pos + 2], data[pos + 3]]) as usize;
        if seg_len < 2 {
            return Err(AaptError::Parse("JPEG: invalid segment length".into()));
        }
        pos += seg_len + 2;
    }
}

/// Decode WEBP bytes to RGBA
fn webp_to_rgba(data: &[u8]) -> Result<(Vec<u8>, usize, usize)> {
    let img = image::load_from_memory(data)
        .map_err(|e| AaptError::Parse(format!("WEBP decode: {}", e)))?;
    let w = img.width() as usize;
    let h = img.height() as usize;
    let rgba = img.to_rgba8();
    Ok((rgba.to_vec(), w, h))
}

/// Check if bytes are WEBP (RIFF header with WEBP type)
fn is_webp_bytes(data: &[u8]) -> bool {
    data.len() >= 12 && &data[0..4] == b"RIFF" && &data[8..12] == b"WEBP"
}

/// Generate a multi-size ICO from PNG, JPEG, or WEBP bytes.
/// ICO sizes: 16, 24, 32, 48, 64, 96, 128, 256 (only sizes <= original).
pub fn png_to_ico(png: &[u8]) -> Result<Vec<u8>> {
    // Handle JPEG input
    if png.len() >= 2 && png[0] == 0xFF && png[1] == 0xD8 {
        return jpeg_to_ico(png);
    }

    // Handle WEBP input
    if is_webp_bytes(png) {
        let (rgba, w, h) = webp_to_rgba(png)?;
        // Re-encode as PNG first, then build multi-size ICO
        let png_bytes = encode_png(&rgba, w, h).map_err(|e| AaptError::Parse(format!("PNG encode: {}", e)))?;
        return png_to_ico_inner(&png_bytes, &rgba, w, h);
    }

    // Decode PNG to RGBA
    let (rgba, w, h) = png_to_rgba(png)?;
    png_to_ico_inner(png, &rgba, w, h)
}

/// Build multi-size ICO from RGBA data (shared by PNG, JPEG, and WEBP paths).
fn png_to_ico_inner(original_png: &[u8], rgba: &[u8], w: usize, h: usize) -> Result<Vec<u8>> {
    // Define desired sizes (only those <= max(w, h))
    let desired_sizes: &[usize] = &[16, 24, 32, 48, 64, 96, 128, 256];
    let max_dim = w.max(h);
    let sizes: Vec<usize> = desired_sizes.iter()
        .copied()
        .filter(|s| *s <= max_dim)
        .collect();

    if sizes.is_empty() {
        return single_ico(original_png, w as u8, h as u8);
    }

    // Generate PNG at each size and collect
    let mut entries: Vec<(u8, u8, Vec<u8>)> = Vec::new();
    for &size in &sizes {
        if size == w && size == h && original_png.len() >= 8
            && &original_png[0..4] == b"\x89PNG"
        {
            // Original size: use original PNG bytes to avoid re-compression artifacts
            let entry_w = if w >= 256 { 0 } else { w as u8 };
            let entry_h = if h >= 256 { 0 } else { h as u8 };
            entries.push((entry_w, entry_h, original_png.to_vec()));
        } else {
            let scaled = scale_rgba(rgba, w, h, size, size);
            if let Ok(png_bytes) = encode_png(&scaled, size, size) {
                let entry_w = if size >= 256 { 0 } else { size as u8 };
                let entry_h = if size >= 256 { 0 } else { size as u8 };
                entries.push((entry_w, entry_h, png_bytes));
            }
        }
    }

    // Build ICO
    let count = entries.len() as u16;
    let mut out: Vec<u8> = Vec::new();
    out.extend_from_slice(&[0u8, 0]);
    out.extend_from_slice(&[1u8, 0]);
    out.extend_from_slice(&count.to_le_bytes());

    let header_size = 6 + count as usize * 16;
    let mut offset = header_size as u32;
    for (ew, eh, img) in &entries {
        let mut entry = [0u8; 16];
        entry[0] = *ew;
        entry[1] = *eh;
        entry[2] = 0;
        entry[3] = 0;
        entry[4] = 1;
        entry[5] = 0;
        entry[6] = 32;
        entry[7] = 0;
        let img_size = img.len() as u32;
        entry[8..12].copy_from_slice(&img_size.to_le_bytes());
        entry[12..16].copy_from_slice(&offset.to_le_bytes());
        out.extend_from_slice(&entry);
        offset += img_size;
    }

    for (_, _, img) in &entries {
        out.extend_from_slice(img);
    }

    Ok(out)
}

/// Create a single-entry ICO (fallback when multi-size fails).
fn single_ico(data: &[u8], w: u8, h: u8) -> Result<Vec<u8>> {
    let mut out: Vec<u8> = Vec::new();
    out.extend_from_slice(&[0u8, 0]);
    out.extend_from_slice(&[1u8, 0]);
    out.extend_from_slice(&[1u8, 0]);
    let mut entry = [0u8; 16];
    entry[0] = w;
    entry[1] = h;
    entry[2] = 0;
    entry[4] = 1;
    entry[6] = 32;
    let img_size = data.len() as u32;
    entry[8..12].copy_from_slice(&img_size.to_le_bytes());
    let offset = 6u32 + 16u32;
    entry[12..16].copy_from_slice(&offset.to_le_bytes());
    out.extend_from_slice(&entry);
    out.extend_from_slice(data);
    Ok(out)
}

fn jpeg_to_ico(jpeg: &[u8]) -> Result<Vec<u8>> {
    // Decode JPEG to RGBA using jpeg-decoder
    let mut decoder = jpeg_decoder::Decoder::new(jpeg);
    let raw = decoder.decode().map_err(|e| AaptError::Parse(format!("JPEG decode: {}", e)))?;
    let info = decoder.info().ok_or_else(|| AaptError::Parse("JPEG: no info after decode".into()))?;
    let w = info.width as usize;
    let h = info.height as usize;
    if w == 0 || h == 0 {
        return Err(AaptError::Parse("JPEG: invalid dimensions".into()));
    }

    // The decoder outputs RGB pixels (no alpha). Convert to RGBA with full opacity.
    let pixel_count = w * h;
    let mut rgba = Vec::with_capacity(pixel_count * 4);
    for i in 0..pixel_count {
        let off = i * 3;
        rgba.push(raw[off]);       // R
        rgba.push(raw[off + 1]);   // G
        rgba.push(raw[off + 2]);   // B
        rgba.push(255);            // A — full opacity
    }

    // Re-encode as PNG first, then build multi-size ICO
    let png_bytes = encode_png(&rgba, w, h).map_err(|e| AaptError::Parse(format!("PNG encode: {}", e)))?;
    png_to_ico_inner(&png_bytes, &rgba, w, h)
}

// ──────────────────────────────────────────────
// WebP detection helper
// ──────────────────────────────────────────────

/// Check if bytes are WebP (RIFF + WEBP).
#[allow(dead_code)]
pub fn is_webp(bytes: &[u8]) -> bool {
    bytes.len() >= 12
        && &bytes[0..4] == b"RIFF"
        && &bytes[8..12] == b"WEBP"
}

/// Convert SVG bytes to multi-size ICO.
pub fn svg_to_ico(svg: &[u8]) -> Result<Vec<u8>> {
    let (rgba, w, h) = crate::vector_drawable::svg_to_rgba(svg, 256)?;
    let png_bytes = encode_png(&rgba, w, h).map_err(|e| AaptError::Parse(format!("PNG encode: {}", e)))?;
    png_to_ico_inner(&png_bytes, &rgba, w, h)
}

/// Convert Android binary XML vector drawable to ICO (XML → PNG → ICO).
pub fn xml_to_ico(axml_bytes: &[u8]) -> Result<Vec<u8>> {
    let png = crate::vector_drawable::render_vector_icon(axml_bytes, Some(256))?;
    png_to_ico(&png)
}

/// Convert Android binary XML vector drawable to SVG string.
pub fn xml_to_svg(axml_bytes: &[u8]) -> Result<String> {
    crate::vector_drawable::xml_to_svg(axml_bytes)
}
