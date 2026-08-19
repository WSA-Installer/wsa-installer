//! Package type detection. Determines whether a file is an APK, XAPK, APKS, APKM,
//! AAB, OBB, or a plain ZIP, based on archive contents (not just extension).

use crate::archive::ZipArchive;
use crate::error::Result;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum PackageType {
    Apk,
    Xapk,
    Apks,
    Apkm,
    Aab,
    Obx, // generic OBB/OBX container
    Zip,
    Unknown,
}

impl PackageType {
    pub fn as_str(&self) -> &'static str {
        match self {
            PackageType::Apk => "APK",
            PackageType::Xapk => "XAPK",
            PackageType::Apks => "APKS",
            PackageType::Apkm => "APKM",
            PackageType::Aab => "AAB",
            PackageType::Obx => "OBB",
            PackageType::Zip => "ZIP",
            PackageType::Unknown => "UNKNOWN",
        }
    }
}

/// Inspect archive entry names to classify the package.
pub fn detect_from_entries(entries: &[String]) -> PackageType {
    let set: std::collections::HashSet<&String> = entries.iter().collect();
    let has = |n: &str| set.contains(&n.to_string());

    // AAB: Android App Bundle
    if has("BundleConfig.pb") || set.iter().any(|e| e.starts_with("base/")) {
        return PackageType::Aab;
    }
    // APKM: APK Mirror bundle (info.json + multiple apks)
    if has("info.json") && entries.iter().any(|e| e.ends_with(".apk")) {
        return PackageType::Apkm;
    }
    // XAPK: manifest.json + at least one apk
    if has("manifest.json") && entries.iter().any(|e| e.ends_with(".apk")) {
        return PackageType::Xapk;
    }
    // APKS: split apks archive (base.apk + toc.pb, or many split apks)
    if has("toc.pb") && set.iter().any(|e| e.ends_with(".apk")) {
        return PackageType::Apks;
    }
    // APK: single (or only) AndroidManifest at root
    if has("AndroidManifest.xml") {
        return PackageType::Apk;
    }
    // XAPK / generic multi-APK container: multiple .apk members at root and no
    // root AndroidManifest.xml (covers XAPK archives that omit manifest.json).
    if entries.iter().filter(|e| e.ends_with(".apk")).count() > 1 {
        return PackageType::Xapk;
    }
    // OBB: expansion file (payload, often no manifest)
    if entries.iter().any(|e| e.to_lowercase().ends_with(".obb"))
        || (entries.iter().all(|e| !e.ends_with(".apk")) && !has("AndroidManifest.xml"))
    {
        // Heuristic: treat as OBB container if it looks like a media/expansion archive
        if entries.iter().any(|e| {
            let l = e.to_lowercase();
            l.ends_with(".mp4") || l.ends_with(".ogg") || l.ends_with(".wav") || l.contains("patch")
        }) {
            return PackageType::Obx;
        }
    }
    PackageType::Zip
}

/// Count APK members inside a container (for split / bundle metadata).
pub fn apk_members(entries: &[String]) -> Vec<String> {
    entries
        .iter()
        .filter(|e| e.ends_with(".apk"))
        .cloned()
        .collect()
}

/// Choose the "base" APK among members (prefer base.apk, then non-config apks).
pub fn base_apk_member(entries: &[String]) -> Option<String> {
    let apks = apk_members(entries);
    if apks.is_empty() {
        return None;
    }
    if let Some(b) = apks.iter().find(|e| {
        let fn_lower = std::path::Path::new(e).file_name().map(|s| s.to_string_lossy().to_lowercase());
        fn_lower.as_deref() == Some("base.apk")
    }) {
        return Some(b.clone());
    }
    if let Some(b) = apks.iter().find(|e| {
        let fn_lower = std::path::Path::new(e).file_name().map(|s| s.to_string_lossy().to_lowercase());
        fn_lower.map(|s| !s.contains("config")).unwrap_or(false)
    }) {
        return Some(b.clone());
    }
    apks.into_iter().next()
}

/// Open a package and detect its type.
pub fn detect_file(path: &std::path::Path) -> Result<PackageType> {
    let za = ZipArchive::open_path(path)?;
    let names: Vec<String> = za.entry_names().iter().map(|s| s.to_string()).collect();
    Ok(detect_from_entries(&names))
}
