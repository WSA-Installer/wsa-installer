//! `resources.arsc` table parser. Resolves resource references (e.g. the
//! `android:icon` value `@mipmap/ic_launcher`) into concrete entry names such as
//! `res/mipmap-xxxhdpi-v26/ic_launcher.png`, choosing the highest-density variant
//! by default.

use crate::error::{AaptError, Result};
use std::collections::HashMap;

const CHUNK_TABLE: u16 = 0x0002;
const CHUNK_PACKAGE: u16 = 0x0200;
const CHUNK_TYPE_SPEC: u16 = 0x0202;
const CHUNK_TYPE: u16 = 0x0201;
const CHUNK_LIBRARY: u16 = 0x0203;
const CHUNK_OVERLAYABLE: u16 = 0x0204;
const CHUNK_STRING_POOL: u16 = 0x0001;
const ENTRY_FLAG_COMPLEX: u32 = 1;

#[derive(Clone, Debug, Default)]
pub struct ResourceTable {
    pub string_pool: Vec<String>,
    pub packages: Vec<ResourcePackage>,
}

#[derive(Clone, Debug, Default)]
pub struct ResourcePackage {
    pub id: u8,
    pub name: String,
    pub type_names: Vec<String>,
    pub key_names: Vec<String>,
    /// type_id -> type entries (key_id -> ResEntry)
    pub types: HashMap<u8, TypeBlock>,
}

#[derive(Clone, Debug, Default)]
pub struct TypeBlock {
    pub name: String,
    pub entries: HashMap<u32, ResEntry>,
}

#[derive(Clone, Debug)]
pub struct ResEntry {
    pub key: String,
    pub value: ResValue,
    /// For complex entries (bags): (attribute_id, value) pairs.
    pub map_entries: Vec<(u32, ResValue)>,
}

#[derive(Clone, Debug)]
pub enum ResValue {
    String(String),
    Int(u32),
    Reference(u32),
    /// Theme attribute reference (?attr/...), resolved through theme style
    Attribute(u32),
    Other(u8, u32),
}

/// Parse a resources.arsc buffer.
pub fn parse_resources(buf: &[u8]) -> Result<ResourceTable> {
    let mut p = Parser {
        buf,
        pos: 0,
        string_pool: Vec::new(),
    };
    p.parse()
}

struct Parser<'a> {
    buf: &'a [u8],
    pos: usize,
    string_pool: Vec<String>,
}

impl<'a> Parser<'a> {
    fn parse(&mut self) -> Result<ResourceTable> {
        let mut table = ResourceTable::default();
        let chunk_type = self.read_u16()?;
        let _header = self.read_u16()?;
        let _chunk_size = self.read_u32()?;
        if chunk_type != CHUNK_TABLE {
            return Err(AaptError::BadMagic {
                expected: format!("{:04x}", CHUNK_TABLE),
                found: format!("{:04x}", chunk_type),
            });
        }
        let _pkg_count = self.read_u32()?;
        // global string pool follows
        if self.pos + 8 <= self.buf.len() {
            let t = self.read_u16()?;
            self.pos -= 2;
            if t == CHUNK_STRING_POOL {
                table.string_pool = self.read_string_pool()?;
                self.string_pool = table.string_pool.clone();
            }
        }
        while self.pos + 8 <= self.buf.len() {
            let start = self.pos;
            let chunk_type = self.read_u16()?;
            let _header = self.read_u16()?;
            let chunk_size = self.read_u32()? as usize;
            if chunk_size < 8 || start + chunk_size > self.buf.len() {
                break;
            }
            if chunk_type == CHUNK_PACKAGE {
                let pkg = self.read_package(start)?;
                table.packages.push(pkg);
            }
            self.pos = start + chunk_size;
        }
        Ok(table)
    }

    fn read_package(&mut self, start: usize) -> Result<ResourcePackage> {
        // header already consumed (type, header, size)
        let id = self.read_u32()? as u8;
        let mut name_buf = [0u16; 128];
        for i in 0..128 {
            name_buf[i] = self.read_u16()?;
        }
        let name = String::from_utf16_lossy(&name_buf[..])
            .trim_end_matches('\0')
            .to_string();
        let _type_strings = self.read_u32()?;
        let _last_public_type = self.read_u32()?;
        let _key_strings = self.read_u32()?;
        let _last_public_key = self.read_u32()?;
        let _type_id_offset = if (self.pos - start) < 0x120 {
            // Newer packages have a typeIdOffset field in the 0x120-byte header.
            self.read_u32()?
        } else {
            0
        };

        let _type_strings_off = start + 8 + 0x10 /*id+name(256)*/ + 4 * 4;
        // type string pool: located at start + (typeStrings offset). We recorded
        // _type_strings as offset from package start. Read it directly.
        let mut pkg = ResourcePackage {
            id,
            name,
            ..Default::default()
        };

        // Save position, jump to type string pool.
        let saved = self.pos;
        let tpool_off = _type_strings as usize;
        self.pos = start + tpool_off;
        pkg.type_names = self.read_string_pool()?;
        let after_type_strings = self.pos;
        // key string pool
        self.pos = start + _key_strings as usize;
        pkg.key_names = self.read_string_pool()?;
        let after_key_strings = self.pos;

        // Start scanning for TYPE_SPEC and TYPE chunks after the key string pool.
        let scan_start = after_type_strings.max(after_key_strings);
        self.pos = scan_start;
        let mut scan = scan_start;
        while scan + 8 <= self.buf.len() {
            let t = u16::from_le_bytes(self.buf[scan..scan + 2].try_into().unwrap());
            let sz = u32::from_le_bytes(self.buf[scan + 4..scan + 8].try_into().unwrap()) as usize;
            if sz < 8 || scan + sz > self.buf.len() {
                break;
            }
            if t == CHUNK_TYPE {
                let (tid, tb) = self.read_type_block(start, &pkg)?;
                // Merge entries: a type may have multiple TYPE chunks per config.
                // File order is most-specific → least-specific (default is last).
                // Keep the FIRST entry for each id (best match for locale/density).
                let block = pkg.types.entry(tid).or_insert_with(|| TypeBlock {
                    name: tb.name.clone(),
                    ..Default::default()
                });
                for (k, v) in tb.entries {
                    block.entries.entry(k).or_insert(v);
                }
                scan = self.pos;
            } else if t == CHUNK_TYPE_SPEC {
                scan += sz;
                self.pos = scan;
            } else if t == CHUNK_STRING_POOL {
                // Skip any remaining string pool chunks (aapt2 may add extra pools)
                scan += sz;
                self.pos = scan;
            } else if t == CHUNK_LIBRARY || t == CHUNK_OVERLAYABLE {
                // Skip library dependencies and overlayables (aapt2)
                scan += sz;
                self.pos = scan;
            } else {
                // Unknown chunk type — skip it instead of breaking (aapt2 may use
                // additional chunk types that we don't need to parse).
                scan += sz;
                self.pos = scan;
            }
        }
        self.pos = saved;
        Ok(pkg)
    }

    fn read_type_block(&mut self, _pkg_start: usize, pkg: &ResourcePackage) -> Result<(u8, TypeBlock)> {
        let start = self.pos;
        let _t = self.read_u16()?;
        let _header = self.read_u16()?;
        let _size = self.read_u32()?;
        let type_id = self.read_u8()?;
        let _res0 = self.read_u8()?;
        let _res1 = self.read_u16()?;
        let _entry_count = self.read_u32()?;
        let entries_start = self.read_u32()?;
        let entries_abs = start + entries_start as usize;

        let type_name = pkg
            .type_names
            .get((type_id - 1) as usize)
            .cloned()
            .unwrap_or_else(|| format!("type{}", type_id));

        let mut block = TypeBlock {
            name: type_name,
            ..Default::default()
        };

        let entry_count =
            u32::from_le_bytes(self.buf[start + 12..start + 16].try_into().unwrap()) as usize;
        let is_sparse = (_res0 & 0x01) != 0;
        let offsets_base = start + _header as usize;

        if is_sparse {
            // Sparse entries: each is ResTable_sparseTypeEntry { idx(16), offset(16 in 4tu) }.
            // offset is in 4-byte units from entriesStart.
            for si in 0..entry_count {
                if offsets_base + si * 4 + 4 > self.buf.len() {
                    break;
                }
                let raw = u32::from_le_bytes(
                    self.buf[offsets_base + si * 4..offsets_base + si * 4 + 4]
                        .try_into()
                        .unwrap(),
                );
                let idx = (raw >> 16) as u16;
                let off_4tu = (raw & 0xFFFF) as usize;
                let entry_abs = entries_abs + off_4tu * 4;
                if let Some(entry) = self.read_entry(entry_abs, pkg, type_id, idx as u32) {
                    block.entries.insert(idx as u32, entry);
                }
            }
        } else {
            // Standard entries: u32 offset per entry, 0xFFFFFFFF = no entry.
            for i in 0..entry_count {
                if offsets_base + i * 4 + 4 > self.buf.len() {
                    break;
                }
                let off = u32::from_le_bytes(
                    self.buf[offsets_base + i * 4..offsets_base + i * 4 + 4]
                        .try_into()
                        .unwrap(),
                ) as usize;
                if off == 0xFFFF_FFFF {
                    continue;
                }
                let entry_abs = entries_abs + off;
                if let Some(entry) = self.read_entry(entry_abs, pkg, type_id, i as u32) {
                    block.entries.insert(i as u32, entry);
                }
            }
        }
        self.pos = start + _size as usize;
        Ok((type_id, block))
    }

    fn read_entry(
        &self,
        abs: usize,
        pkg: &ResourcePackage,
        _type_id: u8,
        key_idx: u32,
    ) -> Option<ResEntry> {
        if abs + 8 > self.buf.len() {
            return None;
        }
        let size = u16::from_le_bytes(self.buf[abs..abs + 2].try_into().unwrap());
        let flags = u16::from_le_bytes(self.buf[abs + 2..abs + 4].try_into().unwrap());
        let key = pkg
            .key_names
            .get(key_idx as usize)
            .cloned()
            .unwrap_or_default();
        if flags as u32 & ENTRY_FLAG_COMPLEX != 0 {
            // Complex entry (bag): read map entries
            let parent_id = u32::from_le_bytes(self.buf[abs + 4..abs + 8].try_into().unwrap());
            let count_raw = u32::from_le_bytes(self.buf[abs + 8..abs + 12].try_into().unwrap()) as usize;
            let map_start = abs + size as usize;
            // Sanity-check count against remaining buffer space
            let max_possible = (self.buf.len().saturating_sub(map_start)) / 12;
            let count = count_raw.min(max_possible);
            let mut map_entries = Vec::with_capacity(count);
            for i in 0..count {
                let me_off = map_start + i * 12; // 4 (name_id) + 8 (Res_value)
                if me_off + 12 > self.buf.len() {
                    break;
                }
                let name_id = u32::from_le_bytes(self.buf[me_off..me_off + 4].try_into().unwrap());
                let val = self.read_raw_res_value(me_off + 4)?;
                map_entries.push((name_id, val));
            }
            return Some(ResEntry {
                key,
                value: ResValue::Other(0x08, parent_id),
                map_entries,
            });
        }
        let val_off = abs + size as usize;
        if val_off + 8 > self.buf.len() {
            return None;
        }
        let value = self.read_raw_res_value(val_off)?;
        Some(ResEntry { key, value, map_entries: Vec::new() })
    }

    fn read_raw_res_value(&self, val_off: usize) -> Option<ResValue> {
        if val_off + 8 > self.buf.len() {
            return None;
        }
        let _val_size = u16::from_le_bytes(self.buf[val_off..val_off + 2].try_into().unwrap());
        let _res0 = self.buf[val_off + 2];
        let data_type = self.buf[val_off + 3];
        let data = u32::from_le_bytes(self.buf[val_off + 4..val_off + 8].try_into().unwrap());
        Some(if data_type == 0x03 {
            let idx = data as usize;
            if idx < self.string_pool.len() {
                ResValue::String(self.string_pool[idx].clone())
            } else {
                ResValue::Other(data_type, data)
            }
        } else if data_type == 0x01 || data_type == 0x07 {
            ResValue::Reference(data)
        } else if data_type == 0x02 {
            ResValue::Attribute(data)
        } else if data_type == 0x10 || data_type == 0x11 || data_type == 0x12 {
            ResValue::Int(data)
        } else if data_type == 0x1c || data_type == 0x1d || data_type == 0x1e || data_type == 0x1f {
            // TYPE_INT_COLOR_ARGB8/RGB4/ARGB4/RGB8 — treat as Int (color)
            // For ARGB8 (0x1C): format #AARRGGBB works directly
            // For RGB8 (0x1F): data is 0x00RRGGBB — high-byte alpha is 0, so strip
            //   and prepend ff: but we can't distinguish in Int, so just pass through
            ResValue::Int(data)
        } else {
            ResValue::Other(data_type, data)
        })
    }

    fn read_string_pool(&mut self) -> Result<Vec<String>> {
        let start = self.pos;
        let chunk_type = self.read_u16()?;
        let header_size = self.read_u16()? as usize;

        // Fixed header is 28 bytes (8 chunk + 20 fields: stringCount, styleCount,
        // flags, stringsStart, stylesStart). Offset table starts at start + 28.
        let chunk_size = self.read_u32()? as usize;
        if chunk_type != CHUNK_STRING_POOL {
            return Err(AaptError::Parse("expected string pool".into()));
        }
        let string_count = self.read_u32()? as usize;
        let _style_count = self.read_u32()?;
        let flags = self.read_u32()?;
        let is_utf8 = (flags & 0x100) != 0;
        let strings_start = self.read_u32()? as usize;
        let _styles_start = self.read_u32()?;

        let offsets_base = start + header_size;
        let mut offsets = Vec::with_capacity(string_count);
        for i in 0..string_count {
            let off =
                u32::from_le_bytes(self.buf[offsets_base + i * 4..offsets_base + i * 4 + 4].try_into().unwrap())
                    as usize;
            offsets.push(off);
        }
        let strings_start_abs = start + strings_start;
        let mut strings = Vec::with_capacity(string_count);
        for off in offsets {
            let p = strings_start_abs + off;
            let s = if is_utf8 {
                let (_, adv1) = read_len_utf8(self.buf, p)?;
                let (byte_len, adv2) = read_len_utf8(self.buf, p + adv1)?;
                String::from_utf8_lossy(&self.buf[p + adv1 + adv2..p + adv1 + adv2 + byte_len]).into_owned()
            } else {
                let len = u16::from_le_bytes(self.buf[p..p + 2].try_into().unwrap()) as usize;
                let mut s = String::with_capacity(len);
                for i in (0..len * 2).step_by(2) {
                    let c = u16::from_le_bytes([self.buf[p + 2 + i], self.buf[p + 3 + i]]);
                    s.push(char::from_u32(c as u32).unwrap_or('�'));
                }
                s
            };
            strings.push(s);
        }
        // Advance position past this pool chunk
        let pool_end = start + chunk_size as usize;
        if pool_end > self.pos {
            self.pos = pool_end;
        }
        Ok(strings)
    }

    fn read_u16(&mut self) -> Result<u16> {
        let b = &self.buf[self.pos..self.pos + 2];
        self.pos += 2;
        Ok(u16::from_le_bytes([b[0], b[1]]))
    }
    fn read_u32(&mut self) -> Result<u32> {
        let b = &self.buf[self.pos..self.pos + 4];
        self.pos += 4;
        Ok(u32::from_le_bytes([b[0], b[1], b[2], b[3]]))
    }
    fn read_u8(&mut self) -> Result<u8> {
        let b = self.buf[self.pos];
        self.pos += 1;
        Ok(b)
    }
}

fn read_len_utf8(buf: &[u8], p: usize) -> Result<(usize, usize)> {
    let first = buf[p] as usize;
    if first < 0x80 {
        Ok((first, 1))
    } else {
        let second = buf[p + 1] as usize;
        Ok(((first & 0x7F) << 8 | second, 2))
    }
}

/// Resolve a resource id to a drawable/mipmap key name within a table,
/// following attribute reference chains (e.g. ?attr/icon → @drawable/ic_launcher).
/// Returns the matching entry key (e.g. "ic_launcher").
pub fn resolve_resource_key(table: &ResourceTable, res_id: u32) -> Option<String> {
    let mut rid = res_id;
    let mut visited = std::collections::HashSet::new();
    loop {
        let pkg_id = ((rid >> 24) & 0xFF) as u8;
        let type_id = ((rid >> 16) & 0xFF) as u8;
        let entry_id = rid & 0xFFFF;
        let mut followed = false;
        for pkg in &table.packages {
            if pkg.id == pkg_id || pkg_id == 0 {
                if let Some(tb) = pkg.types.get(&type_id) {
                    if let Some(e) = tb.entries.get(&entry_id) {
                        match &e.value {
                            ResValue::Reference(next) => {
                                if visited.insert(rid) {
                                    rid = *next;
                                    followed = true;
                                }
                            }
                            _ => return Some(e.key.clone()),
                        }
                    }
                }
                if followed {
                    break;
                }
            }
        }
        if !followed {
            return None;
        }
    }
}

/// Resolve a resource id to its final ResValue, following reference chains.
/// Returns the final ResValue (String, Int, etc.) and the key name.
pub fn resolve_resource_value(table: &ResourceTable, res_id: u32) -> Option<(ResValue, String)> {
    let mut rid = res_id;
    let mut visited = std::collections::HashSet::new();
    loop {
        let pkg_id = ((rid >> 24) & 0xFF) as u8;
        let type_id = ((rid >> 16) & 0xFF) as u8;
        let entry_id = rid & 0xFFFF;
        let mut followed = false;
        for pkg in &table.packages {
            if pkg.id == pkg_id || pkg_id == 0 {
                if let Some(tb) = pkg.types.get(&type_id) {
                    if let Some(e) = tb.entries.get(&entry_id) {
                        match &e.value {
                            ResValue::Reference(next) => {
                                if visited.insert(rid) {
                                    rid = *next;
                                    followed = true;
                                }
                            }
                            _ => return Some((e.value.clone(), e.key.clone())),
                        }
                    }
                }
                if followed {
                    break;
                }
            }
        }
        if !followed {
            return None;
        }
    }
}

/// Resolve a resource id and return its map entries (for complex/bag resources).
/// Follows reference chains. Returns None if not a complex entry.
pub fn resolve_resource_map_entries<'a>(table: &'a ResourceTable, res_id: u32) -> Option<&'a [(u32, ResValue)]> {
    let mut rid = res_id;
    let mut visited = std::collections::HashSet::new();
    loop {
        let pkg_id = ((rid >> 24) & 0xFF) as u8;
        let type_id = ((rid >> 16) & 0xFF) as u8;
        let entry_id = rid & 0xFFFF;
        let mut followed = false;
        for pkg in &table.packages {
            if pkg.id == pkg_id || pkg_id == 0 {
                if let Some(tb) = pkg.types.get(&type_id) {
                    if let Some(e) = tb.entries.get(&entry_id) {
                        if !e.map_entries.is_empty() {
                            return Some(&e.map_entries);
                        }
                        if let ResValue::Reference(next) = &e.value {
                            if visited.insert(rid) {
                                rid = *next;
                                followed = true;
                            }
                        }
                    }
                }
                if followed {
                    break;
                }
            }
        }
        if !followed {
            return None;
        }
    }
}

/// Resolve a theme attribute reference through a theme style.
/// `theme_id` is the resource ID of the theme (e.g. @style/AppTheme).
/// `attr_id` is the attribute ID to look up in the theme.
/// Walks the parent style chain and returns the first matching map entry value.
pub fn resolve_theme_attr_value(table: &ResourceTable, theme_id: u32, attr_id: u32) -> Option<ResValue> {
    let mut visited = std::collections::HashSet::new();
    let mut tid = theme_id;
    loop {
        if !visited.insert(tid) {
            return None;
        }
        let pkg_id = ((tid >> 24) & 0xFF) as u8;
        let type_id = ((tid >> 16) & 0xFF) as u8;
        let entry_id = tid & 0xFFFF;
        let mut found_entry = false;
        for pkg in &table.packages {
            if pkg.id == pkg_id || pkg_id == 0 {
                if let Some(tb) = pkg.types.get(&type_id) {
                    if let Some(e) = tb.entries.get(&entry_id) {
                        found_entry = true;
                        // Check map entries for matching attribute
                        for (name_id, val) in &e.map_entries {
                            if *name_id == attr_id {
                                return Some(val.clone());
                            }
                        }
                        // Follow parent style chain
                        if let ResValue::Reference(parent) = &e.value {
                            tid = *parent;
                        } else if let ResValue::Int(parent) = &e.value {
                            tid = *parent;
                        } else {
                            return None;
                        }
                    }
                }
            }
        }
        if !found_entry {
            return None;
        }
    }
}

/// Given a resolved key name (e.g. "ic_launcher") and a list of archive entry
/// paths, choose the best candidate PNG path by density preference.
pub fn pick_best_icon_path(key: &str, entries: &[String]) -> Option<String> {
    let densities: [&str; 6] = ["xxxhdpi", "xxhdpi", "xhdpi", "hdpi", "mdpi", "ldpi"];
    let prefixes: [&str; 2] = ["", "base/"];
    let key_lc = key.to_lowercase();
    let mut best: Option<(i32, String)> = None;
    for entry in entries {
        let el = entry.to_lowercase();
        if !el.ends_with(".png") {
            continue;
        }
        if !el.contains(&format!("/{}/", key_lc)) && !el.contains(&format!("{}_", key_lc)) {
            // match either res/.../KEY.png or KEY_foreground.png style
            let file = std::path::Path::new(entry)
                .file_name()
                .map(|s| s.to_string_lossy().to_lowercase())
                .unwrap_or_default();
            if file != format!("{}.png", key_lc)
                && !file.starts_with(&format!("{}_", key_lc))
                && !file.starts_with(&format!("{}-", key_lc))
            {
                continue;
            }
            if !el.contains("res/") {
                continue;
            }
        }
        let mut score: i32 = 1000;
        for (i, d) in densities.iter().enumerate() {
            if el.contains(&format!("mipmap-{}", d)) || el.contains(&format!("drawable-{}", d)) {
                score = i as i32;
                break;
            }
        }
        if el.contains("mipmap") {
            score = score.saturating_sub(1);
        }
        if el.contains("round") {
            score = score.saturating_add(2);
        }
        if let Some((bs, _)) = &best {
            if score < *bs {
                best = Some((score, entry.clone()));
            }
        } else {
            best = Some((score, entry.clone()));
        }
    }
    // Prefer explicit key match; fall back.
    let _ = prefixes;
    best.map(|(_, p)| p)
}

/// Last-resort icon picker used when resource resolution yields no usable path
/// (e.g. obfuscated resource tables where entry names no longer match archive
/// paths). Scans `res/**.png` entries and scores by launcher-likelihood and
/// density, returning the best candidate path.
pub fn scan_best_icon_path(entries: &[String]) -> Option<String> {
    let densities: [&str; 6] = ["xxxhdpi", "xxhdpi", "xhdpi", "hdpi", "mdpi", "ldpi"];
    let mut best: Option<(i32, String)> = None;
    for entry in entries {
        let el = entry.to_lowercase();
        if !el.ends_with(".png") || !el.contains("res/") {
            continue;
        }
        let file = std::path::Path::new(entry)
            .file_name()
            .map(|s| s.to_string_lossy().to_lowercase())
            .unwrap_or_default();
        // Only consider plausible launcher icons.
        let launcher_like = el.contains("mipmap")
            || el.contains("drawable")
            || file.contains("launcher")
            || file.contains("icon")
            || file.starts_with("ic_");
        if !launcher_like {
            continue;
        }
        // Score: lower is better. Strongly prefer mipmap, then density.
        let mut score = if el.contains("mipmap") { 0 } else if el.contains("drawable") { 20 } else { 40 };
        for (i, d) in densities.iter().enumerate() {
            if el.contains(&format!("mipmap-{}", d)) || el.contains(&format!("drawable-{}", d)) {
                score += i as i32;
                break;
            }
        }
        if el.contains("round") {
            score = score.saturating_sub(1);
        }
        if let Some((bs, _)) = &best {
            if score < *bs {
                best = Some((score, entry.clone()));
            }
        } else {
            best = Some((score, entry.clone()));
        }
    }
    best.map(|(_, p)| p)
}
