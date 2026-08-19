use std::collections::HashMap;
use std::path::{Path, PathBuf};

use crate::aapt_wrapper::{self, BadgingInfo};
use crate::archive::ZipArchive;
use crate::cert::read_signature;
use crate::detect::{self, PackageType};
use crate::error::{AaptError, Result};
use crate::info::PackageInfo;
use crate::manifest::parse_manifest_flexible;

#[derive(Debug)]
pub struct SourceApk {
    pub path: PathBuf,
    pub ptype: PackageType,
    pub original_type: Option<PackageType>,
    pub container_path: Option<PathBuf>,
    pub container_meta: Option<HashMap<String, String>>,
    pub container_entries: Option<Vec<String>>,
    pub _temp: Option<PathBuf>,
}

impl Drop for SourceApk {
    fn drop(&mut self) {
        if let Some(ref tmp) = self._temp {
            let _ = std::fs::remove_file(tmp);
        }
    }
}

pub fn select_source_apk(path: &Path) -> Result<SourceApk> {
    let ptype = detect::detect_file(path)?;
    let stem = path.file_stem().map(|s| s.to_string_lossy().to_string()).unwrap_or_default();

    match ptype {
        PackageType::Apk | PackageType::Aab => {
            let entries = list_entries(path);
            Ok(SourceApk {
                path: path.to_path_buf(),
                ptype,
                original_type: None,
                container_path: None,
                container_meta: None,
                container_entries: entries,
                _temp: None,
            })
        }
        PackageType::Xapk | PackageType::Apks | PackageType::Apkm => {
            extract_from_container(path, ptype, &stem)
        }
        _ => Err(AaptError::Parse(format!("unsupported package type: {:?}", ptype))),
    }
}

fn list_entries(path: &Path) -> Option<Vec<String>> {
    ZipArchive::open_path(path)
        .ok()
        .map(|za| za.entry_names().iter().map(|s| s.to_string()).collect())
}

fn extract_from_container(path: &Path, orig_ptype: PackageType, stem: &str) -> Result<SourceApk> {
    let mut za = ZipArchive::open_path(path)?;
    let entries: Vec<String> = za.entry_names().iter().map(|s| s.to_string()).collect();

    let container_meta = parse_container_json(&entries, &mut za);

    // Select base APK
    let apk_name = container_meta.as_ref()
        .and_then(|m| m.get("base_apk").cloned())
        .or_else(|| container_meta.as_ref().and_then(|m| m.get("main_apk").cloned()))
        .unwrap_or_else(|| select_best_apk(&entries));

    let apk_bytes = za.read_entry(&apk_name)?;
    let temp_dir = std::env::temp_dir();
    let temp_path = temp_dir.join(format!("aaptpp_{}_{}.apk", stem, std::process::id()));

    std::fs::write(&temp_path, &apk_bytes).map_err(|e| AaptError::Io(e))?;

    Ok(SourceApk {
        path: temp_path.clone(),
        ptype: PackageType::Apk,
        original_type: Some(orig_ptype),
        container_path: Some(path.to_path_buf()),
        container_meta,
        container_entries: Some(entries),
        _temp: Some(temp_path),
    })
}

fn select_best_apk(entries: &[String]) -> String {
    if entries.iter().any(|e| e == "base.apk") {
        return "base.apk".to_string();
    }
    let mut best: Option<&String> = None;
    for e in entries {
        if e.ends_with(".apk") {
            if best.map(|b| e.len() > b.len()).unwrap_or(true) {
                best = Some(e);
            }
        }
    }
    best.cloned().unwrap_or_else(|| "base.apk".to_string()).clone()
}

fn parse_container_json(entries: &[String], za: &mut ZipArchive<std::fs::File>) -> Option<HashMap<String, String>> {
    let json_name = if entries.iter().any(|e| e == "info.json") {
        "info.json"
    } else if entries.iter().any(|e| e == "manifest.json") {
        "manifest.json"
    } else {
        return None;
    };

    let bytes = za.read_entry(json_name).ok()?;
    let val: serde_json::Value = serde_json::from_slice(&bytes).ok()?;
    let obj = val.as_object()?;
    let mut map = HashMap::new();

    // XAPK manifest.json
    for key in &["package_name", "name", "title", "version_code", "version_name",
                 "min_sdk_version", "target_sdk_version", "icon"] {
        if let Some(v) = obj.get(*key).and_then(|v| v.as_str()) {
            map.insert(key.to_string(), v.to_string());
        }
    }

    // APKM info.json - handle both standard and APKM-specific field names
    if let Some(v) = obj.get("app_name").and_then(|v| v.as_str()) {
        map.insert("app_name".to_string(), v.to_string());
    }
    if let Some(v) = obj.get("pname").and_then(|v| v.as_str()) {
        map.insert("package_name".to_string(), v.to_string());
    }
    if let Some(v) = obj.get("versioncode").and_then(|v| v.as_str()) {
        map.insert("version_code".to_string(), v.to_string());
    }
    // version_name - try multiple fields
    if let Some(v) = obj.get("version_name").and_then(|v| v.as_str())
        .or_else(|| obj.get("release_version").and_then(|v| v.as_str()))
    {
        map.insert("version_name".to_string(), v.to_string());
    }
    // min_sdk_version
    if let Some(v) = obj.get("min_api").and_then(|v| v.as_str())
        .or_else(|| obj.get("min_sdk_version").and_then(|v| v.as_str()))
    {
        map.insert("min_sdk_version".to_string(), v.to_string());
    }
    // target_sdk_version
    if let Some(v) = obj.get("target_sdk_version").and_then(|v| v.as_str()) {
        map.insert("target_sdk_version".to_string(), v.to_string());
    }
    // icon
    if let Some(v) = obj.get("icon").and_then(|v| v.as_str()) {
        map.insert("icon".to_string(), v.to_string());
    }
    // base_apk / main_apk
    if let Some(v) = obj.get("base_apk").and_then(|v| v.as_str())
        .or_else(|| obj.get("main_apk").and_then(|v| v.as_str()))
    {
        map.insert("base_apk".to_string(), v.to_string());
    }

    // XAPK split_apks → base file
    if let Some(splits) = obj.get("split_apks").and_then(|v| v.as_array()) {
        for split in splits {
            let id = split.get("id").and_then(|v| v.as_str()).unwrap_or("");
            if id == "base" {
                if let Some(file) = split.get("file").and_then(|v| v.as_str()) {
                    map.insert("base_apk".to_string(), file.to_string());
                }
            }
        }
    }

    if map.contains_key("package_name") || map.contains_key("app_name") {
        Some(map)
    } else {
        None
    }
}

pub fn extract_metadata(source: &SourceApk) -> Result<PackageInfo> {
    match source.ptype {
        PackageType::Aab => extract_metadata_aab(source),
        _ => extract_metadata_apk(source),
    }
}

fn extract_metadata_apk(source: &SourceApk) -> Result<PackageInfo> {
    let mut info = PackageInfo::default();
    info.file = source.container_path.as_ref()
        .and_then(|p| p.file_name().map(|s| s.to_string_lossy().to_string()))
        .or_else(|| source.path.file_name().map(|s| s.to_string_lossy().to_string()))
        .unwrap_or_default();
    info.package_type = source.original_type
        .map(|t| t.as_str().to_string())
        .unwrap_or_else(|| "APK".to_string());

    let entry_names = source.container_entries.as_deref().unwrap_or(&[]);
    let zip_entries: Vec<String> = if !entry_names.is_empty() {
        entry_names.to_vec()
    } else {
        list_entries(&source.path).unwrap_or_default()
    };

    // ─── Try AAPT dump badging ───
    let mut aapt_ok = false;
    if let Ok(badging) = aapt_wrapper::dump_badging(&source.path) {
        apply_badging(&mut info, &badging);
        aapt_ok = true;
    }

    // ─── Merge container JSON metadata (overrides AAPT) ───
    if let Some(ref meta) = source.container_meta {
        apply_container_meta(&mut info, meta);
    }

    // ─── Custom parser extras (always runs) ───
    let mut za = match ZipArchive::open_path(&source.path) {
        Ok(z) => z,
        Err(_) => return Ok(info),
    };

    let manifest_buf = read_manifest_from_entries(&zip_entries, &mut za);
    if let Some(ref buf) = manifest_buf {
        if let Ok(m) = parse_manifest_flexible(buf) {
            let label_res = m.label_res;

            // Fill manifest fields that AAPT may have missed
            if !aapt_ok || info.manifest.package.is_empty() {
                crate::info::fill_from_manifest(&mut info, &m);
            } else {
                info.manifest.install_location = m.install_location.clone();
                info.manifest.platform_build_version_code = m.compile_sdk.map(|v| v.to_string());
            }

            // Resolve app_name via resources.arsc if AAPT didn't give us a good one
            if !aapt_ok || info.app_name.is_empty() || info.app_name == info.manifest.package {
                if zip_entries.iter().any(|e| e == "resources.arsc") {
                    if let Ok(arsc_buf) = za.read_entry("resources.arsc") {
                        if let Ok(table) = crate::resources::parse_resources(&arsc_buf) {
                            resolve_app_name_from_table(&mut info, &table, label_res);
                        }
                    }
                }
            }

            // Apply remaining manifest fields always
            if let Some(app) = m.raw.find("application") {
                if info.application.theme.is_none() {
                    if let Some(v) = app.attr_value("theme").and_then(|v| format_resource(v)) {
                        info.application.theme = Some(v);
                    }
                }
            }
        }
    }

    // ─── Signing (custom parser) ───
    if let Ok(sig) = read_signature(&mut za) {
        apply_signing(&mut info, &sig);
    }

    // ─── Native libs (custom parser) ───
    crate::info::scan_native_libs(&zip_entries, &mut info);

    // ─── Resources summary (custom parser) ───
    crate::info::scan_resources(&mut za, &zip_entries, &mut info);

    // ─── OBB detection ───
    for n in &zip_entries {
        if n.to_lowercase().ends_with(".obb") {
            info.obb.push(n.clone());
        }
    }

    // ─── Archive info ───
    if let Ok(meta) = std::fs::metadata(&source.path) {
        info.file_size = meta.len();
        info.archive.file_size = meta.len();
        info.archive.total_entries = zip_entries.len();
    }

    // ─── Container members ───
    if let Some(ref centries) = source.container_entries {
        info.apk_members = detect::apk_members(centries);
        info.split_modules = info.apk_members.iter()
            .filter(|e| Path::new(e).file_name().map(|f| f.to_string_lossy().to_lowercase() != "base.apk").unwrap_or(false))
            .cloned()
            .collect();
        if source.container_meta.is_some() {
            info.feature_modules = info.split_modules.clone();
        }
    }

    // Icon presence
    if aapt_ok && !info.icon.density_icons.is_empty() {
        info.icon.present = true;
    } else {
        info.icon.present = info.icon.resource_path.is_some()
            || zip_entries.iter().any(|e| {
                let l = e.to_lowercase();
                l.contains("ic_launcher") || l.contains("launcher_icon")
            });
    }

    Ok(info)
}

fn extract_metadata_aab(source: &SourceApk) -> Result<PackageInfo> {
    let mut info = PackageInfo::default();
    info.file = source.path.file_name().map(|s| s.to_string_lossy().to_string()).unwrap_or_default();
    info.package_type = "AAB".to_string();

    let entries = source.container_entries.as_deref().unwrap_or(&[]);

    let mut za = ZipArchive::open_path(&source.path)?;

    let manifest_name = entries.iter()
        .find(|e| e.ends_with("manifest/AndroidManifest.xml"))
        .or_else(|| entries.iter().find(|e| e.as_str() == "base/AndroidManifest.xml"))
        .cloned();

    if let Some(ref mname) = manifest_name {
        if let Ok(buf) = za.read_entry(mname) {
            if let Ok(m) = parse_manifest_flexible(&buf) {
                let label_res = m.label_res;
                crate::info::fill_from_manifest(&mut info, &m);
                if entries.iter().any(|e| e.ends_with("resources.arsc")) {
                    let arsc_name = entries.iter().find(|e| e.ends_with("resources.arsc")).unwrap();
                    if let Ok(arsc_buf) = za.read_entry(arsc_name) {
                        if let Ok(table) = crate::resources::parse_resources(&arsc_buf) {
                            resolve_app_name_from_table(&mut info, &table, label_res);
                        }
                    }
                }
            }
        }
    }

    crate::info::scan_resources(&mut za, entries, &mut info);
    info.apk_members = detect::apk_members(entries);

    if let Ok(meta) = std::fs::metadata(&source.path) {
        info.file_size = meta.len();
        info.archive.file_size = meta.len();
    }

    Ok(info)
}

fn read_manifest_from_entries(entries: &[String], za: &mut ZipArchive<std::fs::File>) -> Option<Vec<u8>> {
    let mname = if entries.iter().any(|e| e == "AndroidManifest.xml") {
        "AndroidManifest.xml"
    } else if entries.iter().any(|e| e == "base/AndroidManifest.xml") {
        "base/AndroidManifest.xml"
    } else {
        return None;
    };
    za.read_entry(mname).ok()
}

fn resolve_app_name_from_table(
    info: &mut PackageInfo,
    table: &crate::resources::ResourceTable,
    label_res: Option<u32>,
) {
    use crate::resources::ResValue;

    let app = info.manifest.package.clone();
    let mut found = false;

    // Layer 1: Resolve label resource ID
    let mut raw_from_label: Option<String> = None;
    if let Some(rid) = label_res {
        if let Some((value, _key)) = crate::resources::resolve_resource_value(table, rid) {
            if let ResValue::String(s) = &value {
                if !s.is_empty() {
                    if has_control_chars(s) {
                        raw_from_label = Some(s.clone());
                    } else {
                        info.app_name = s.clone();
                        found = true;
                    }
                }
            }
        }
    }

    // Layer 2: Common keys in string table
    if !found && info.app_name == app && !app.is_empty() {
        for pkg in &table.packages {
            for (_tid, tb) in &pkg.types {
                if tb.name == "string" {
                    for (_eid, entry) in &tb.entries {
                        let lower_key = entry.key.to_lowercase();
                        if lower_key == "app_name"
                            || lower_key == "appname"
                            || lower_key == "title"
                            || lower_key == "app_label"
                            || lower_key == "application_name"
                            || lower_key.contains("app_name")
                        {
                            if let ResValue::String(s) = &entry.value {
                                if !s.is_empty() && !has_control_chars(s) {
                                    info.app_name = s.clone();
                                    return;
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    // Layer 3: Strip control chars from raw string
    if !found {
        if let Some(raw) = raw_from_label {
            let cleaned: String = raw.chars().filter(|&c| c as u32 > 0x1F && c as u32 != 0x7F).collect();
            let cleaned = cleaned.trim().to_string();
            if !cleaned.is_empty() && cleaned != app {
                info.app_name = cleaned;
            }
        }
    }
}

fn has_control_chars(s: &str) -> bool {
    s.chars().any(|c| c as u32 <= 0x1F || c as u32 == 0x7F)
}

fn format_resource(v: &crate::manifest::Value) -> Option<String> {
    match v {
        crate::manifest::Value::Resource(r) => Some(format!("@0x{:08x}", r)),
        crate::manifest::Value::Str(s) => Some(s.clone()),
        _ => None,
    }
}

fn apply_badging(info: &mut PackageInfo, badging: &BadgingInfo) {
    if !badging.package.is_empty() {
        info.manifest.package = badging.package.clone();
    }
    if !badging.label.is_empty() {
        info.app_name = badging.label.clone();
    }
    if !badging.version_name.is_empty() {
        info.manifest.version_name = Some(badging.version_name.clone());
    }
    if !badging.version_code.is_empty() {
        info.manifest.version_code = Some(badging.version_code.clone());
    }
    if let Some(v) = badging.min_sdk {
        info.sdk.min = Some(v);
    }
    if let Some(v) = badging.target_sdk {
        info.sdk.target = Some(v);
    }
    if let Some(ref v) = badging.launcher {
        info.launcher_activity = Some(v.clone());
    }
    for p in &badging.permissions {
        info.permissions.push(crate::info::PermissionInfo {
            name: p.clone(),
            max_sdk_version: None,
            required_feature: None,
            sdk_23: false,
        });
    }
    for f in &badging.features {
        info.features.push(crate::info::FeatureInfo {
            name: Some(f.clone()),
            required: true,
            gl_es_version: None,
        });
    }
    for l in &badging.libraries {
        info.libraries.push(crate::info::LibraryInfo {
            name: l.clone(),
            required: true,
        });
    }
    if let Some(ref v) = badging.icon_path {
        info.icon.resource_path = Some(v.clone());
    }
    info.icon.density_icons = badging.density_icons.clone();
}

fn apply_container_meta(info: &mut PackageInfo, meta: &HashMap<String, String>) {
    if let Some(v) = meta.get("app_name") {
        if !v.is_empty() && has_control_chars(v) {
            let cleaned: String = v.chars().filter(|&c| c as u32 > 0x1F && c as u32 != 0x7F).collect();
            if !cleaned.is_empty() {
                info.app_name = cleaned;
            }
        } else if !v.is_empty() {
            info.app_name = v.clone();
        }
    }
    if info.app_name.is_empty() || info.app_name == info.manifest.package {
        if let Some(v) = meta.get("title").or_else(|| meta.get("name")) {
            if !v.is_empty() {
                info.app_name = v.clone();
            }
        }
    }
    if let Some(v) = meta.get("package_name") {
        if !v.is_empty() {
            info.manifest.package = v.clone();
        }
    }
    if let Some(v) = meta.get("version_name") {
        if !v.is_empty() {
            info.manifest.version_name = Some(v.clone());
        }
    }
    if let Some(v) = meta.get("version_code") {
        if !v.is_empty() {
            info.manifest.version_code = Some(v.clone());
        }
    }
    if let Some(v) = meta.get("min_sdk_version") {
        if let Ok(n) = v.parse::<u32>() {
            info.sdk.min = Some(n);
        }
    }
    if let Some(v) = meta.get("target_sdk_version") {
        if let Ok(n) = v.parse::<u32>() {
            info.sdk.target = Some(n);
        }
    }
    if let Some(v) = meta.get("icon") {
        if !v.is_empty() {
            info.icon.container_icon = Some(v.clone());
        }
    }
}

fn apply_signing(info: &mut PackageInfo, sig: &crate::cert::SignatureInfo) {
    info.signing.v1 = sig.v1;
    info.signing.v2 = sig.v2;
    info.signing.v3 = sig.v3;
    for c in &sig.certs {
        info.signing.certificates.push(crate::info::CertificateDetail {
            subject: c.subject.clone(),
            issuer: c.issuer.clone(),
            serial_number: c.serial.clone(),
            not_before: c.not_before.clone(),
            not_after: c.not_after.clone(),
            expired: c.expired,
            sha1: c.sha1.clone(),
            sha256: c.sha256.clone(),
            md5: c.md5.clone(),
            algorithm: c.algorithm.clone(),
            public_key_type: String::new(),
            public_key_bits: 0,
        });
        if !info.signing.schemes.contains(&"v1".to_string()) {
            info.signing.schemes.push("v1".to_string());
        }
    }
    info.signing.schemes.extend(sig.schemes.clone());
    info.signing.schemes.sort();
    info.signing.schemes.dedup();
}

pub fn quick_field<F>(path: &Path, extractor: F) -> Result<String>
where
    F: Fn(&PackageInfo) -> Option<String>,
{
    let source = select_source_apk(path)?;
    let info = extract_metadata(&source)?;
    extractor(&info).ok_or_else(|| AaptError::NotFound("field not found".into()))
}

pub fn has_container_icon(source: &SourceApk) -> Option<Vec<u8>> {
    let entries = source.container_entries.as_ref()?;
    let container = source.container_path.as_ref()?;
    let mut za = ZipArchive::open_path(container).ok()?;

    for name in &["icon.png", "icon.jpg", "icon.webp"] {
        if entries.iter().any(|e| e == name) {
            if let Ok(bytes) = za.read_entry(name) {
                if is_image_bytes(&bytes) {
                    return Some(bytes);
                }
            }
        }
    }

    if let Some(ref meta) = source.container_meta {
        if let Some(icon_ref) = meta.get("icon") {
            if entries.iter().any(|e| e == icon_ref) {
                if let Ok(bytes) = za.read_entry(icon_ref) {
                    if is_image_bytes(&bytes) {
                        return Some(bytes);
                    }
                }
            }
        }
    }

    None
}

pub fn is_image_bytes(bytes: &[u8]) -> bool {
    bytes.len() >= 8
        && (&bytes[0..4] == b"\x89PNG" || &bytes[0..2] == b"\xff\xd8" || &bytes[0..4] == b"RIFF")
}
