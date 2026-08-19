use crate::archive::ZipArchive;
use crate::cert::read_signature;
use crate::detect::{self, PackageType};
use crate::error::{AaptError, Result};
use crate::icon::extract_best_icon;
use crate::manifest::{manifest_to_text, parse_manifest_flexible, Manifest};
use crate::resources::{parse_resources, resolve_resource_value};
use serde::Serialize;
use std::collections::HashMap;

// ──────────────────────────────────────────────
// Manifest
// ──────────────────────────────────────────────
#[derive(Clone, Debug, Default, Serialize)]
pub struct ManifestInfo {
    pub package: String,
    pub version_name: Option<String>,
    pub version_code: Option<String>,
    pub split_name: Option<String>,
    pub config_for_split: Option<String>,
    pub install_location: Option<String>,
    pub platform_build_version_code: Option<String>,
    pub platform_build_version_name: Option<String>,
}

#[derive(Clone, Debug, Default, Serialize)]
pub struct SdkInfo {
    pub min: Option<u32>,
    pub target: Option<u32>,
    pub max: Option<u32>,
    pub compile: Option<u32>,
    pub compile_codename: Option<String>,
}

#[derive(Clone, Debug, Default, Serialize)]
pub struct ApplicationInfo {
    pub debuggable: bool,
    pub allow_backup: Option<bool>,
    pub supports_rtl: Option<bool>,
    pub is_game: Option<bool>,
    pub multi_arch: Option<bool>,
    pub has_code: Option<bool>,
    pub test_only: Option<bool>,
    pub hardware_accelerated: Option<bool>,
    pub large_heap: Option<bool>,
    pub persistent: Option<bool>,
    pub extract_native_libs: Option<bool>,
    pub vm_safe_mode: Option<bool>,
    pub kill_after_restore: Option<bool>,
    pub restore_any_version: Option<bool>,
    pub theme: Option<String>,
    pub network_security_config: Option<String>,
    pub app_component_factory: Option<String>,
    pub backup_agent: Option<String>,
    pub full_backup_content: Option<String>,
    pub data_extraction_rules: Option<String>,
    pub task_affinity: Option<String>,
    pub request_legacy_external_storage: Option<bool>,
    pub enable_on_back_invoked_callback: Option<bool>,
    pub banner_res: Option<u32>,
}

// ──────────────────────────────────────────────
// Permissions
// ──────────────────────────────────────────────
#[derive(Clone, Debug, Default, Serialize)]
pub struct PermissionInfo {
    pub name: String,
    pub max_sdk_version: Option<u32>,
    pub required_feature: Option<String>,
    pub sdk_23: bool,
}

// ──────────────────────────────────────────────
// Features & Libraries
// ──────────────────────────────────────────────
#[derive(Clone, Debug, Default, Serialize)]
pub struct FeatureInfo {
    pub name: Option<String>,
    pub required: bool,
    pub gl_es_version: Option<u32>,
}

#[derive(Clone, Debug, Default, Serialize)]
pub struct LibraryInfo {
    pub name: String,
    pub required: bool,
}

// ──────────────────────────────────────────────
// Intent Filters
// ──────────────────────────────────────────────
#[derive(Clone, Debug, Default, Serialize)]
pub struct IntentFilterInfo {
    pub actions: Vec<String>,
    pub categories: Vec<String>,
    pub schemes: Vec<String>,
    pub hosts: Vec<String>,
    pub ports: Vec<String>,
    pub paths: Vec<String>,
    pub path_patterns: Vec<String>,
    pub path_prefixes: Vec<String>,
    pub mime_types: Vec<String>,
    pub browsable: bool,
}

// ──────────────────────────────────────────────
// Components (activities, services, receivers, providers, aliases)
// ──────────────────────────────────────────────
#[derive(Clone, Debug, Default, Serialize)]
pub struct ComponentDetail {
    pub name: String,
    pub component_type: String,
    pub exported: Option<bool>,
    pub enabled: Option<bool>,
    pub permission: Option<String>,
    pub process: Option<String>,
    pub icon_res: Option<u32>,
    pub label_res: Option<u32>,
    pub task_affinity: Option<String>,
    pub direct_boot_aware: Option<bool>,
    pub intent_filters: Vec<IntentFilterInfo>,
    pub meta_data: Vec<MetaEntryInfo>,

    // Activity-specific
    pub launch_mode: Option<String>,
    pub screen_orientation: Option<String>,
    pub config_changes: Option<String>,
    pub window_soft_input_mode: Option<String>,
    pub parent_activity_name: Option<String>,
    pub no_history: Option<bool>,
    pub exclude_from_recents: Option<bool>,
    pub always_retain_task_state: Option<bool>,
    pub clear_task_on_launch: Option<bool>,
    pub finish_on_task_launch: Option<bool>,
    pub allow_task_reparenting: Option<bool>,
    pub document_launch_mode: Option<String>,
    pub max_recents: Option<u32>,
    pub supports_picture_in_picture: Option<bool>,
    pub resizeable_activity: Option<bool>,
    pub color_mode: Option<String>,
    pub show_for_all_users: Option<bool>,
    pub auto_remove_from_recents: Option<bool>,
    pub max_aspect_ratio: Option<f32>,
    pub min_aspect_ratio: Option<f32>,

    // Service-specific
    pub foreground_service_type: Option<String>,

    // Provider-specific
    pub authorities: Option<String>,
    pub read_permission: Option<String>,
    pub write_permission: Option<String>,
    pub grant_uri_permissions: Option<bool>,
    pub multiprocess: Option<bool>,
    pub init_order: Option<i32>,
    pub syncable: Option<bool>,

    // Alias-specific
    pub target_activity: Option<String>,
    pub target_package: Option<String>,
}

// ──────────────────────────────────────────────
// Compatibility
// ──────────────────────────────────────────────
#[derive(Clone, Debug, Default, Serialize)]
pub struct SupportsScreensInfo {
    pub small_screens: Option<bool>,
    pub normal_screens: Option<bool>,
    pub large_screens: Option<bool>,
    pub xlarge_screens: Option<bool>,
    pub resizeable: Option<bool>,
    pub any_density: Option<bool>,
}

#[derive(Clone, Debug, Default, Serialize)]
pub struct CompatibleScreen {
    pub screen_size: Option<u32>,
    pub screen_density: Option<u32>,
}

#[derive(Clone, Debug, Default, Serialize)]
pub struct OriginalPackage {
    pub name: String,
}

#[derive(Clone, Debug, Default, Serialize)]
pub struct OverlayInfo {
    pub target_package: String,
    pub target_name: Option<String>,
    pub priority: Option<i32>,
    pub is_static: Option<bool>,
    pub required_property: Option<String>,
}

// ──────────────────────────────────────────────
// Meta Data
// ──────────────────────────────────────────────
#[derive(Clone, Debug, Default, Serialize)]
pub struct MetaEntryInfo {
    pub name: String,
    pub value: Option<String>,
    pub resource: Option<u32>,
}

// ──────────────────────────────────────────────
// Resources
// ──────────────────────────────────────────────
#[derive(Clone, Debug, Default, Serialize)]
pub struct ResourceInfo {
    pub has_resources: bool,
    pub total_entries: usize,
    pub packages: Vec<ResourcePackageInfo>,
    pub locales: Vec<String>,
    pub densities: Vec<String>,
    pub configurations: Vec<String>,
}

#[derive(Clone, Debug, Default, Serialize)]
pub struct ResourcePackageInfo {
    pub id: u8,
    pub name: String,
    pub type_names: Vec<String>,
    pub entry_count: usize,
}

// ──────────────────────────────────────────────
// Icon
// ──────────────────────────────────────────────
#[derive(Clone, Debug, Default, Serialize)]
pub struct IconInfo {
    pub present: bool,
    pub resource: Option<u32>,
    pub round_resource: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub resource_path: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub container_icon: Option<String>,
    #[serde(skip_serializing_if = "Vec::is_empty")]
    pub density_icons: Vec<(u32, String)>,
}

// ──────────────────────────────────────────────
// Signing
// ──────────────────────────────────────────────
#[derive(Clone, Debug, Default, Serialize)]
pub struct SigningInfo {
    pub v1: bool,
    pub v2: bool,
    pub v3: bool,
    pub v4: bool,
    pub schemes: Vec<String>,
    pub certificates: Vec<CertificateDetail>,
}

#[derive(Clone, Debug, Default, Serialize)]
pub struct CertificateDetail {
    pub subject: String,
    pub issuer: String,
    pub serial_number: String,
    pub not_before: String,
    pub not_after: String,
    pub expired: bool,
    pub sha1: String,
    pub sha256: String,
    pub md5: String,
    pub algorithm: String,
    pub public_key_type: String,
    pub public_key_bits: u32,
}

// ──────────────────────────────────────────────
// Native Libraries
// ──────────────────────────────────────────────
#[derive(Clone, Debug, Default, Serialize)]
pub struct NativeLibsInfo {
    pub supported_abis: Vec<String>,
    pub primary_abi: Option<String>,
    pub has_64bit: bool,
    pub has_32bit: bool,
    pub total_libs: usize,
    pub per_abi: Vec<AbiLibInfo>,
}

#[derive(Clone, Debug, Default, Serialize)]
pub struct AbiLibInfo {
    pub abi: String,
    pub libs: Vec<String>,
    pub count: usize,
}

// ──────────────────────────────────────────────
// Archive
// ──────────────────────────────────────────────
#[derive(Clone, Debug, Default, Serialize)]
pub struct ArchiveInfo {
    pub file_size: u64,
    pub compressed_size: u64,
    pub total_entries: usize,
    pub compression_ratio: f64,
}

// ──────────────────────────────────────────────
// Top-level PackageInfo
// ──────────────────────────────────────────────
#[derive(Clone, Debug, Default, Serialize)]
pub struct PackageInfo {
    // Identity
    pub file: String,
    pub package_type: String,
    pub file_size: u64,
    pub compressed_size: u64,

    // Manifest
    pub manifest: ManifestInfo,
    pub sdk: SdkInfo,
    pub application: ApplicationInfo,

    // Permissions
    pub permissions: Vec<PermissionInfo>,

    // Components
    pub components: Vec<ComponentDetail>,
    pub launcher_activity: Option<String>,

    // Features & Libraries
    pub features: Vec<FeatureInfo>,
    pub libraries: Vec<LibraryInfo>,

    // Compatibility
    pub supports_screens: Option<SupportsScreensInfo>,
    pub compatible_screens: Vec<CompatibleScreen>,
    pub original_packages: Vec<OriginalPackage>,
    pub overlays: Vec<OverlayInfo>,

    // Meta
    pub meta_data: Vec<MetaEntryInfo>,

    // Resources
    pub resources: ResourceInfo,

    // Icon
    pub icon: IconInfo,

    // App Name (resolved through multi-layer algorithm)
    pub app_name: String,

    // Native Libraries
    pub native_libs: NativeLibsInfo,

    // Signing
    pub signing: SigningInfo,

    // Archive / Container
    pub archive: ArchiveInfo,
    pub obb: Vec<String>,
    pub apk_members: Vec<String>,
    pub split_modules: Vec<String>,
    pub feature_modules: Vec<String>,
}

// ──────────────────────────────────────────────
// Analyze file
// ──────────────────────────────────────────────
pub fn analyze_file(path: &std::path::Path) -> Result<PackageInfo> {
    let file_size = std::fs::metadata(path)?.len();
    let ptype = detect::detect_file(path)?;
    let mut za = ZipArchive::open_path(path)?;
    let names: Vec<String> = za.entry_names().iter().map(|s| s.to_string()).collect();
    analyze_from_archive(path, ptype, file_size, &mut za, &names)
}

pub fn analyze_from_archive<R: std::io::Read + std::io::Seek>(
    path: &std::path::Path,
    ptype: PackageType,
    file_size: u64,
    za: &mut ZipArchive<R>,
    names: &[String],
) -> Result<PackageInfo> {
    if ptype == PackageType::Aab {
        return analyze_aab(path, ptype, file_size, za, names);
    }
    if matches!(ptype, PackageType::Xapk | PackageType::Apks | PackageType::Apkm) {
        return analyze_container(path, ptype, file_size, za, names);
    }
    analyze_apk_inner(path, ptype, file_size, za, names)
}

fn analyze_apk_inner<R: std::io::Read + std::io::Seek>(
    path: &std::path::Path,
    ptype: PackageType,
    file_size: u64,
    za: &mut ZipArchive<R>,
    names: &[String],
) -> Result<PackageInfo> {
    let file_name = path.file_name().map(|s| s.to_string_lossy().to_string()).unwrap_or_default();
    let manifest_name = if names.iter().any(|e| e == "AndroidManifest.xml") {
        "AndroidManifest.xml"
    } else if names.iter().any(|e| e == "base/AndroidManifest.xml") {
        "base/AndroidManifest.xml"
    } else {
        ""
    };

    let mut info = PackageInfo {
        file: file_name.clone(),
        package_type: ptype.as_str().to_string(),
        file_size,
        compressed_size: file_size,
        archive: ArchiveInfo {
            file_size,
            compressed_size: file_size,
            total_entries: names.len(),
            compression_ratio: if file_size > 0 { 100.0 } else { 0.0 },
        },
        ..Default::default()
    };

    let mut label_res = None;
    if !manifest_name.is_empty() {
        if let Ok(buf) = za.read_entry(manifest_name) {
            if let Ok(m) = parse_manifest_flexible(&buf) {
                label_res = m.label_res;
                fill_from_manifest(&mut info, &m);
            }
        }
    }

    // Resolve app_name through resources.arsc (multi-layer algorithm)
    resolve_app_name(&mut info, za, names, label_res);

    // Archive scanning
    let compression_info = scan_archive_entries(za, names);
    info.archive.compressed_size = compression_info.0;
    info.archive.total_entries = names.len();
    info.archive.compression_ratio = if file_size > 0 {
        (compression_info.0 as f64 / file_size as f64) * 100.0
    } else {
        0.0
    };

    // Container metadata
    let apk_members = detect::apk_members(names);
    info.apk_members = apk_members.clone();
    if !apk_members.is_empty() && ptype != PackageType::Apk {
        info.split_modules = apk_members
            .iter()
            .filter(|e| {
                std::path::Path::new(e).file_name().map(|f| f.to_string_lossy().to_lowercase() != "base.apk").unwrap_or(false)
            })
            .cloned()
            .collect();
    }

    // Native libs
    scan_native_libs(names, &mut info);

    // OBB
    for n in names {
        if n.to_lowercase().ends_with(".obb") {
            info.obb.push(n.clone());
        }
    }

    // Certificates/signing
    if let Ok(sig) = read_signature(za) {
        info.signing.v1 = sig.v1;
        info.signing.v2 = sig.v2;
        info.signing.v3 = sig.v3;
        for c in &sig.certs {
            info.signing.certificates.push(CertificateDetail {
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

    // Resources info
    scan_resources(za, names, &mut info);

    // Icon presence
    info.icon.present = extract_best_icon(za, false).is_ok();

    Ok(info)
}

fn analyze_aab<R: std::io::Read + std::io::Seek>(
    path: &std::path::Path,
    ptype: PackageType,
    file_size: u64,
    za: &mut ZipArchive<R>,
    names: &[String],
) -> Result<PackageInfo> {
    let manifest_name = names
        .iter()
        .find(|e| e.ends_with("manifest/AndroidManifest.xml"))
        .cloned()
        .or_else(|| names.iter().find(|e| e.as_str() == "base/AndroidManifest.xml").cloned());

    let mut info = PackageInfo {
        file: path.file_name().map(|s| s.to_string_lossy().to_string()).unwrap_or_default(),
        package_type: ptype.as_str().to_string(),
        file_size,
        compressed_size: file_size,
        archive: ArchiveInfo { file_size, compressed_size: file_size, total_entries: names.len(), compression_ratio: 0.0 },
        ..Default::default()
    };

    let mut label_res = None;
    if let Some(mname) = manifest_name {
        if let Ok(buf) = za.read_entry(&mname) {
            if let Ok(m) = parse_manifest_flexible(&buf) {
                label_res = m.label_res;
                fill_from_manifest(&mut info, &m);
            }
        }
    }

    info.apk_members = detect::apk_members(names);
    info.split_modules = info.apk_members.iter().filter(|e| {
        std::path::Path::new(e).file_name().map(|f| f.to_string_lossy().to_lowercase() != "base.apk").unwrap_or(false)
    }).cloned().collect();

    resolve_app_name(&mut info, za, names, label_res);
    scan_resources(za, names, &mut info);
    info.icon.present = extract_best_icon(za, false).is_ok();

    Ok(info)
}

fn analyze_container<R: std::io::Read + std::io::Seek>(
    path: &std::path::Path,
    ptype: PackageType,
    file_size: u64,
    za: &mut ZipArchive<R>,
    names: &[String],
) -> Result<PackageInfo> {
    if let Some(base) = detect::base_apk_member(names) {
        if let Ok(bytes) = za.read_entry(&base) {
            let mut inner = ZipArchive::new(std::io::Cursor::new(bytes))?;
            let inner_names: Vec<String> = inner.entry_names().iter().map(|s| s.to_string()).collect();
            let mut inner_info = analyze_apk_inner(path, PackageType::Apk, file_size, &mut inner, &inner_names)?;

            // Merge container-level data
            if inner_info.launcher_activity.is_none() {
                if let Some(l) = scan_launcher_in_splits(za, names, &base) {
                    inner_info.launcher_activity = Some(l);
                }
            }

            if !inner_info.icon.present && names.iter().any(|e| e == "icon.png") {
                inner_info.icon.present = za.read_entry("icon.png").ok()
                    .map(|b| b.len() >= 8 && (&b[0..4] == b"\x89PNG" || &b[0..2] == b"\xff\xd8"))
                    .unwrap_or(false);
            }

            inner_info.file = path.file_name().map(|s| s.to_string_lossy().to_string()).unwrap_or_default();
            inner_info.package_type = ptype.as_str().to_string();
            inner_info.apk_members = detect::apk_members(names);
            inner_info.split_modules = inner_info.apk_members.iter().filter(|e| {
                std::path::Path::new(e).file_name().map(|f| f.to_string_lossy().to_lowercase() != "base.apk").unwrap_or(false)
            }).cloned().collect();
            return Ok(inner_info);
        }
    }
    analyze_apk_inner(path, ptype, file_size, za, names)
}

// ──────────────────────────────────────────────
// Fill from manifest
// ──────────────────────────────────────────────
pub(crate) fn fill_from_manifest(info: &mut PackageInfo, m: &Manifest) {
    // Manifest identity
    info.manifest.package = m.package.clone();
    info.manifest.version_name = m.version_name.clone();
    info.manifest.version_code = m.version_code.clone();
    info.manifest.install_location = m.install_location.clone();
    info.manifest.platform_build_version_code = m.compile_sdk.map(|v| v.to_string());
    info.manifest.platform_build_version_name = m.compile_sdk_codename.clone();

    // Split (extract from raw element)
    if let Some(v) = m.raw.attr_value("split").and_then(|v| v.as_str()) {
        info.manifest.split_name = Some(v.to_string());
    }
    if let Some(v) = m.raw.attr_value("configForSplit").and_then(|v| v.as_str()) {
        info.manifest.config_for_split = Some(v.to_string());
    }

    // SDK
    info.sdk.min = m.min_sdk;
    info.sdk.target = m.target_sdk;
    info.sdk.compile = m.compile_sdk;
    info.sdk.compile_codename = m.compile_sdk_codename.clone();
    if let Some(uses_sdk) = m.raw.find("uses-sdk") {
        if info.sdk.min.is_none() {
            if let Some(v) = uses_sdk.attr_value("minSdkVersion") {
                info.sdk.min = Some(int_val(v) as u32);
            }
        }
        if info.sdk.target.is_none() {
            if let Some(v) = uses_sdk.attr_value("targetSdkVersion") {
                info.sdk.target = Some(int_val(v) as u32);
            }
        }
        if let Some(v) = uses_sdk.attr_value("maxSdkVersion") {
            info.sdk.max = Some(int_val(v) as u32);
        }
    }

    // Application
    let app = m.raw.find("application");
    if let Some(app) = app {
        if let Some(v) = app.attr_value("debuggable") { info.application.debuggable = int_val(v) != 0; }
        if let Some(v) = app.attr_value("allowBackup") { info.application.allow_backup = Some(int_val(v) != 0); }
        if let Some(v) = app.attr_value("supportsRtl") { info.application.supports_rtl = Some(int_val(v) != 0); }
        if let Some(v) = app.attr_value("isGame") { info.application.is_game = Some(int_val(v) != 0); }
        if let Some(v) = app.attr_value("multiArch") { info.application.multi_arch = Some(int_val(v) != 0); }
        if let Some(v) = app.attr_value("hasCode") { info.application.has_code = Some(int_val(v) != 0); }
        if let Some(v) = app.attr_value("testOnly") { info.application.test_only = Some(int_val(v) != 0); }
        if let Some(v) = app.attr_value("hardwareAccelerated") { info.application.hardware_accelerated = Some(int_val(v) != 0); }
        if let Some(v) = app.attr_value("largeHeap") { info.application.large_heap = Some(int_val(v) != 0); }
        if let Some(v) = app.attr_value("persistent") { info.application.persistent = Some(int_val(v) != 0); }
        if let Some(v) = app.attr_value("extractNativeLibs") { info.application.extract_native_libs = Some(int_val(v) != 0); }
        if let Some(v) = app.attr_value("vmSafeMode") { info.application.vm_safe_mode = Some(int_val(v) != 0); }
        if let Some(v) = app.attr_value("killAfterRestore") { info.application.kill_after_restore = Some(int_val(v) != 0); }
        if let Some(v) = app.attr_value("restoreAnyVersion") { info.application.restore_any_version = Some(int_val(v) != 0); }
        if let Some(v) = app.attr_value("requestLegacyExternalStorage") { info.application.request_legacy_external_storage = Some(int_val(v) != 0); }
        if let Some(v) = app.attr_value("enableOnBackInvokedCallback") { info.application.enable_on_back_invoked_callback = Some(int_val(v) != 0); }
        if let Some(v) = app.attr_value("theme").and_then(|v| format_resource(v)) { info.application.theme = Some(v); }
        if let Some(v) = app.attr_value("networkSecurityConfig").and_then(|v| format_resource(v)) { info.application.network_security_config = Some(v); }
        if let Some(v) = app.attr_value("appComponentFactory").and_then(|v| v.as_str()) { info.application.app_component_factory = Some(v.to_string()); }
        if let Some(v) = app.attr_value("backupAgent").and_then(|v| v.as_str()) { info.application.backup_agent = Some(v.to_string()); }
        if let Some(v) = app.attr_value("fullBackupContent").and_then(|v| format_resource(v)) { info.application.full_backup_content = Some(v); }
        if let Some(v) = app.attr_value("dataExtractionRules").and_then(|v| format_resource(v)) { info.application.data_extraction_rules = Some(v); }
        if let Some(v) = app.attr_value("taskAffinity").and_then(|v| v.as_str()) { info.application.task_affinity = Some(v.to_string()); }

        // Banner
        if let Some(v) = app.attr_value("banner").and_then(|v| v.as_resource()) {
            info.application.banner_res = Some(v);
        }
    }

    // Icon resources
    info.icon.resource = m.icon_res;
    info.icon.round_resource = m.round_icon_res;

    // Permissions
    for perm in m.raw.find_all("uses-permission") {
        let name = perm.attr_value("name").and_then(|v| v.as_str()).unwrap_or("").to_string();
        let max_sdk = perm.attr_value("maxSdkVersion").map(|v| int_val(v) as u32);
        let required_feat = perm.attr_value("requiredFeature").and_then(|v| v.as_str()).map(|s| s.to_string());
        info.permissions.push(PermissionInfo { name, max_sdk_version: max_sdk, required_feature: required_feat, sdk_23: false });
    }
    for perm in m.raw.find_all("uses-permission-sdk-23") {
        let name = perm.attr_value("name").and_then(|v| v.as_str()).unwrap_or("").to_string();
        let max_sdk = perm.attr_value("maxSdkVersion").map(|v| int_val(v) as u32);
        info.permissions.push(PermissionInfo { name, max_sdk_version: max_sdk, required_feature: None, sdk_23: true });
    }

    // Features
    for feat in &m.uses_features {
        info.features.push(FeatureInfo {
            name: feat.name.clone(),
            required: feat.required,
            gl_es_version: feat.gl_es_version,
        });
    }

    // Libraries
    for lib in &m.uses_libraries {
        info.libraries.push(LibraryInfo { name: lib.clone(), required: true });
    }

    // Meta-data
    for meta in &m.metadata {
        info.meta_data.push(MetaEntryInfo {
            name: meta.name.clone(),
            value: meta.value.clone(),
            resource: meta.resource,
        });
    }

    // Components
    let _ = fill_components(&m, &mut info.components, "activity", "activity");
    let _ = fill_components(&m, &mut info.components, "service", "service");
    let _ = fill_components(&m, &mut info.components, "receiver", "receiver");
    let _ = fill_components(&m, &mut info.components, "provider", "provider");
    let _ = fill_components(&m, &mut info.components, "activity-alias", "activity-alias");

    // Launcher activity
    let mut launcher_candidates = m.activities.clone();
    launcher_candidates.extend_from_slice(&m.activities); // from interpret()
    let all_activities = m.raw.find_all("activity");
    let all_aliases = m.raw.find_all("activity-alias");
    for act in &all_activities {
        let has_main = act.find_all("intent-filter").iter().any(|f| {
            f.find_all("action").iter().any(|a| a.attr_value("name").and_then(|v| v.as_str()).map(|s| s == "android.intent.action.MAIN").unwrap_or(false))
        });
        let has_launcher = act.find_all("intent-filter").iter().any(|f| {
            f.find_all("category").iter().any(|c| c.attr_value("name").and_then(|v| v.as_str()).map(|s| s == "android.intent.category.LAUNCHER").unwrap_or(false))
        });
        if has_main && has_launcher {
            info.launcher_activity = act.attr_value("name").and_then(|v| v.as_str()).map(|s| s.to_string());
            break;
        }
    }
    if info.launcher_activity.is_none() {
        for alias in &all_aliases {
            let has_main = alias.find_all("intent-filter").iter().any(|f| {
                f.find_all("action").iter().any(|a| a.attr_value("name").and_then(|v| v.as_str()).map(|s| s == "android.intent.action.MAIN").unwrap_or(false))
            });
            let has_launcher = alias.find_all("intent-filter").iter().any(|f| {
                f.find_all("category").iter().any(|c| c.attr_value("name").and_then(|v| v.as_str()).map(|s| s == "android.intent.category.LAUNCHER").unwrap_or(false))
            });
            if has_main && has_launcher {
                info.launcher_activity = alias.attr_value("name").and_then(|v| v.as_str()).map(|s| s.to_string());
                break;
            }
        }
    }
    info.launcher_activity = m.launcher_activity.clone().or(info.launcher_activity.clone());

    // Supports screens
    if let Some(ss) = m.raw.find("supports-screens") {
        let mut s = SupportsScreensInfo::default();
        if let Some(v) = ss.attr_value("smallScreens") { s.small_screens = Some(int_val(v) != 0); }
        if let Some(v) = ss.attr_value("normalScreens") { s.normal_screens = Some(int_val(v) != 0); }
        if let Some(v) = ss.attr_value("largeScreens") { s.large_screens = Some(int_val(v) != 0); }
        if let Some(v) = ss.attr_value("xlargeScreens") { s.xlarge_screens = Some(int_val(v) != 0); }
        if let Some(v) = ss.attr_value("resizeable") { s.resizeable = Some(int_val(v) != 0); }
        if let Some(v) = ss.attr_value("anyDensity") { s.any_density = Some(int_val(v) != 0); }
        info.supports_screens = Some(s);
    }

    // Compatible screens
    if let Some(cs) = m.raw.find("compatible-screens") {
        for screen in cs.find_all("screen") {
            let size = screen.attr_value("screenSize").map(|v| int_val(v) as u32);
            let density = screen.attr_value("screenDensity").map(|v| int_val(v) as u32);
            info.compatible_screens.push(CompatibleScreen { screen_size: size, screen_density: density });
        }
    }

    // Original packages
    for op in m.raw.find_all("original-package") {
        if let Some(name) = op.attr_value("name").and_then(|v| v.as_str()) {
            info.original_packages.push(OriginalPackage { name: name.to_string() });
        }
    }

    // Overlays
    for ov in m.raw.find_all("overlay") {
        if let Some(tp) = ov.attr_value("targetPackage").and_then(|v| v.as_str()) {
            info.overlays.push(OverlayInfo {
                target_package: tp.to_string(),
                target_name: ov.attr_value("targetName").and_then(|v| v.as_str()).map(|s| s.to_string()),
                priority: ov.attr_value("priority").map(|v| int_val(v) as i32),
                is_static: ov.attr_value("isStatic").map(|v| int_val(v) != 0),
                required_property: ov.attr_value("requiredProperty").and_then(|v| v.as_str()).map(|s| s.to_string()),
            });
        }
    }

    // App name (will be refined in resolve_app_name)
    info.app_name = m.label_text.clone().unwrap_or_else(|| m.package.clone());
}

fn fill_components(m: &Manifest, out: &mut Vec<ComponentDetail>, tag: &str, comp_type: &str) {
    for elem in m.raw.find_all(tag) {
        let name = elem.attr_value("name").and_then(|v| v.as_str()).unwrap_or("").to_string();
        let mut c = ComponentDetail {
            name: name.clone(),
            component_type: comp_type.to_string(),
            exported: match elem.attr_value("exported") {
                Some(crate::manifest::Value::Bool(b)) => Some(*b),
                Some(crate::manifest::Value::Int(i)) => Some(*i != 0),
                _ => None,
            },
            enabled: match elem.attr_value("enabled") {
                Some(crate::manifest::Value::Bool(b)) => Some(*b),
                Some(crate::manifest::Value::Int(i)) => Some(*i != 0),
                _ => None,
            },
            permission: elem.attr_value("permission").and_then(|v| v.as_str()).map(|s| s.to_string()),
            process: elem.attr_value("process").and_then(|v| v.as_str()).map(|s| s.to_string()),
            icon_res: elem.attr_value("icon").and_then(|v| v.as_resource()),
            label_res: elem.attr_value("label").and_then(|v| v.as_resource()),
            task_affinity: elem.attr_value("taskAffinity").and_then(|v| v.as_str()).map(|s| s.to_string()),
            direct_boot_aware: elem.attr_value("directBootAware").map(|v| int_val(v) != 0),
            ..Default::default()
        };

        // Activity-specific
        if comp_type == "activity" || comp_type == "activity-alias" {
            c.launch_mode = elem.attr_value("launchMode").and_then(|v| v.as_str()).map(|s| s.to_string());
            c.screen_orientation = elem.attr_value("screenOrientation").and_then(|v| v.as_str()).map(|s| s.to_string());
            c.config_changes = elem.attr_value("configChanges").and_then(|v| v.as_str()).map(|s| s.to_string());
            c.window_soft_input_mode = elem.attr_value("windowSoftInputMode").and_then(|v| v.as_str()).map(|s| s.to_string());
            c.parent_activity_name = elem.attr_value("parentActivityName").and_then(|v| v.as_str()).map(|s| s.to_string());
            c.no_history = elem.attr_value("noHistory").map(|v| int_val(v) != 0);
            c.exclude_from_recents = elem.attr_value("excludeFromRecents").map(|v| int_val(v) != 0);
            c.always_retain_task_state = elem.attr_value("alwaysRetainTaskState").map(|v| int_val(v) != 0);
            c.clear_task_on_launch = elem.attr_value("clearTaskOnLaunch").map(|v| int_val(v) != 0);
            c.finish_on_task_launch = elem.attr_value("finishOnTaskLaunch").map(|v| int_val(v) != 0);
            c.allow_task_reparenting = elem.attr_value("allowTaskReparenting").map(|v| int_val(v) != 0);
            c.document_launch_mode = elem.attr_value("documentLaunchMode").and_then(|v| v.as_str()).map(|s| s.to_string());
            c.max_recents = elem.attr_value("maxRecents").map(|v| int_val(v) as u32);
            c.supports_picture_in_picture = elem.attr_value("supportsPictureInPicture").map(|v| int_val(v) != 0);
            c.resizeable_activity = elem.attr_value("resizeableActivity").map(|v| int_val(v) != 0);
            c.color_mode = elem.attr_value("colorMode").and_then(|v| v.as_str()).map(|s| s.to_string());
            c.show_for_all_users = elem.attr_value("showForAllUsers").map(|v| int_val(v) != 0);
            c.auto_remove_from_recents = elem.attr_value("autoRemoveFromRecents").map(|v| int_val(v) != 0);
        }

        // Alias-specific
        if comp_type == "activity-alias" {
            c.target_activity = elem.attr_value("targetActivity").and_then(|v| v.as_str()).map(|s| s.to_string());
            c.target_package = elem.attr_value("targetPackage").and_then(|v| v.as_str()).map(|s| s.to_string());
        }

        // Service-specific
        if comp_type == "service" {
            c.foreground_service_type = elem.attr_value("foregroundServiceType").and_then(|v| v.as_str()).map(|s| s.to_string());
        }

        // Provider-specific
        if comp_type == "provider" {
            c.authorities = elem.attr_value("authorities").and_then(|v| v.as_str()).map(|s| s.to_string());
            c.read_permission = elem.attr_value("readPermission").and_then(|v| v.as_str()).map(|s| s.to_string());
            c.write_permission = elem.attr_value("writePermission").and_then(|v| v.as_str()).map(|s| s.to_string());
            c.grant_uri_permissions = elem.attr_value("grantUriPermissions").map(|v| int_val(v) != 0);
            c.multiprocess = elem.attr_value("multiprocess").map(|v| int_val(v) != 0);
            c.init_order = elem.attr_value("initOrder").map(|v| int_val(v) as i32);
            c.syncable = elem.attr_value("syncable").map(|v| int_val(v) != 0);
        }

        // Intent filters
        for filt in elem.find_all("intent-filter") {
            let mut fi = IntentFilterInfo::default();
            for a in filt.find_all("action") {
                if let Some(v) = a.attr_value("name").and_then(|v| v.as_str()) {
                    fi.actions.push(v.to_string());
                }
            }
            for cat in filt.find_all("category") {
                if let Some(v) = cat.attr_value("name").and_then(|v| v.as_str()) {
                    fi.categories.push(v.to_string());
                    if v == "android.intent.category.BROWSABLE" { fi.browsable = true; }
                }
            }
            for d in filt.find_all("data") {
                if let Some(v) = d.attr_value("scheme").and_then(|v| v.as_str()) { fi.schemes.push(v.to_string()); }
                if let Some(v) = d.attr_value("host").and_then(|v| v.as_str()) { fi.hosts.push(v.to_string()); }
                if let Some(v) = d.attr_value("port").and_then(|v| v.as_str()) { fi.ports.push(v.to_string()); }
                if let Some(v) = d.attr_value("path").and_then(|v| v.as_str()) { fi.paths.push(v.to_string()); }
                if let Some(v) = d.attr_value("pathPattern").and_then(|v| v.as_str()) { fi.path_patterns.push(v.to_string()); }
                if let Some(v) = d.attr_value("pathPrefix").and_then(|v| v.as_str()) { fi.path_prefixes.push(v.to_string()); }
                if let Some(v) = d.attr_value("mimeType").and_then(|v| v.as_str()) { fi.mime_types.push(v.to_string()); }
            }
            c.intent_filters.push(fi);
        }

        // Meta-data
        for meta in elem.find_all("meta-data") {
            c.meta_data.push(MetaEntryInfo {
                name: meta.attr_value("name").and_then(|v| v.as_str()).unwrap_or("").to_string(),
                value: meta.attr_value("value").and_then(|v| v.as_str()).map(|s| s.to_string()),
                resource: meta.attr_value("resource").and_then(|v| v.as_resource()),
            });
        }

        out.push(c);
    }
}

// ──────────────────────────────────────────────
// Multi-layer App Name Resolution
// ──────────────────────────────────────────────
/// Check if string contains ASCII control characters (0x00-0x1F, 0x7F)
fn has_control_chars(s: &str) -> bool {
    s.chars().any(|c| c as u32 <= 0x1F || c as u32 == 0x7F)
}
/// Layer 1: <application> label resource → resolve through resources.arsc
/// Layer 2: Scan resources.arsc string pool for common keys ("app_name", "title", etc.)
/// Layer 3: Text value of label (already set in fill_from_manifest)
/// Layer 4: Package name (already set as fallback)
fn resolve_app_name<R: std::io::Read + std::io::Seek>(
    info: &mut PackageInfo,
    za: &mut ZipArchive<R>,
    names: &[String],
    label_res: Option<u32>,
) {
    if !names.iter().any(|e| e == "resources.arsc") {
        return;
    }
    let entry_name = if names.iter().any(|e| e == "resources.arsc") {
        "resources.arsc"
    } else {
        match names.iter().find(|e| e.ends_with("resources.arsc")) {
            Some(s) => s.as_str(),
            None => return,
        }
    };

    let Ok(arsc_buf) = za.read_entry(entry_name) else { return };
    let Ok(table) = parse_resources(&arsc_buf) else { return };

    let app = info.manifest.package.clone();
    let mut found = false;

    // Layer 1: Resolve <application> label resource ID
    // If the resolved string has control characters, save raw for cleanup later
    let mut raw_from_label: Option<String> = None;
    if let Some(rid) = label_res {
        if let Some((value, _key)) = resolve_resource_value(&table, rid) {
            if let crate::resources::ResValue::String(s) = &value {
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

    // Layer 2: Try common string keys in resource table
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
                            if let crate::resources::ResValue::String(s) = &entry.value {
                                if !s.is_empty()
                                    && !has_control_chars(s)
                                    && !s.contains('\u{0}')
                                {
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
    // Layer 3: Text value of label (already set via fill_from_manifest)
    // If still not resolved, try cleaning control chars from raw string
    if !found {
        let target = raw_from_label.as_deref().unwrap_or(&info.app_name);
        let cleaned: String = target.chars().filter(|&c| c as u32 > 0x1F && c as u32 != 0x7F).collect();
        let cleaned = cleaned.trim().to_string();
        if !cleaned.is_empty() && cleaned != app {
            info.app_name = cleaned;
        }
    }
}

// ──────────────────────────────────────────────
// Archive scanning
// ──────────────────────────────────────────────
fn scan_archive_entries<R: std::io::Read + std::io::Seek>(
    za: &mut ZipArchive<R>,
    names: &[String],
) -> (u64, usize) {
    let mut total_compressed = 0u64;
    for name in names {
        if let Some(entry) = za.entries.get(name) {
            total_compressed += entry.compressed_size;
        }
    }
    (total_compressed, names.len())
}

// ──────────────────────────────────────────────
// Native library scanning
// ──────────────────────────────────────────────
pub(crate) fn scan_native_libs(names: &[String], info: &mut PackageInfo) {
    let mut abi_map: HashMap<String, Vec<String>> = HashMap::new();
    for n in names {
        let l = n.to_lowercase();
        if l.contains("lib/") && l.ends_with(".so") {
            let parts: Vec<&str> = n.split('/').collect();
            if parts.len() >= 3 {
                let arch = parts[1].to_string();
                abi_map.entry(arch.clone()).or_default().push(n.clone());
            }
        }
    }
    let mut abis: Vec<String> = abi_map.keys().cloned().collect();
    abis.sort_by(|a, b| {
        let priority = |x: &str| match x {
            "arm64-v8a" => 0,
            "armeabi-v7a" => 1,
            "x86_64" => 2,
            "x86" => 3,
            _ => 4,
        };
        priority(a).cmp(&priority(b))
    });
    let total: usize = abi_map.values().map(|v| v.len()).sum();
    info.native_libs = NativeLibsInfo {
        supported_abis: abis.clone(),
        primary_abi: abis.first().cloned(),
        has_64bit: abis.iter().any(|a| a.contains("64")),
        has_32bit: abis.iter().any(|a| !a.contains("64")),
        total_libs: total,
        per_abi: abis.iter().map(|a| AbiLibInfo {
            abi: a.clone(),
            libs: abi_map.get(a).cloned().unwrap_or_default(),
            count: abi_map.get(a).map(|v| v.len()).unwrap_or(0),
        }).collect(),
    };
}

// ──────────────────────────────────────────────
// Resources scanning
// ──────────────────────────────────────────────
pub(crate) fn scan_resources<R: std::io::Read + std::io::Seek>(
    za: &mut ZipArchive<R>,
    names: &[String],
    info: &mut PackageInfo,
) {
    let entry_name = if names.iter().any(|e| e == "resources.arsc") {
        "resources.arsc"
    } else {
        match names.iter().find(|e| e.ends_with("resources.arsc")) {
            Some(s) => s.as_str(),
            None => return,
        }
    };
    let Ok(arsc_buf) = za.read_entry(entry_name) else { return };
    let Ok(table) = parse_resources(&arsc_buf) else { return };

    let mut total = 0;
    let mut locales = Vec::new();
    let mut densities = Vec::new();
    let mut pkg_infos = Vec::new();
    let mut configs = Vec::new();

    for pkg in &table.packages {
        let mut pkg_entry_count = 0;
        for (_tid, tb) in &pkg.types {
            pkg_entry_count += tb.entries.len();
            total += tb.entries.len();
        }
        pkg_infos.push(ResourcePackageInfo {
            id: pkg.id,
            name: pkg.name.clone(),
            type_names: pkg.type_names.clone(),
            entry_count: pkg_entry_count,
        });
    }

    // Detect locales/densities from directory names
    for n in names {
        let l = n.to_lowercase();
        if l.contains("/values-") || l.contains("/mipmap-") || l.contains("/drawable-") {
            // Extract configuration suffixes
            if let Some(suffix) = l.rsplit('-').next() {
                let parts: Vec<&str> = suffix.split('-').collect();
                for part in &parts {
                    match *part {
                        "en" | "en-rUS" | "en-rGB" | "fr" | "de" | "es" | "it" | "ja" | "ko" | "zh" | "zh-rCN" | "zh-rTW" | "ru" | "ar" | "pt" | "pt-rBR" | "nl" | "tr" | "sv" | "da" | "fi" | "pl" | "cs" | "hu" | "el" | "ro" | "th" | "vi" | "hi" | "bn" => {
                            if !locales.contains(&part.to_string()) { locales.push(part.to_string()); }
                        }
                        _ => {}
                    }
                    if part.ends_with("dpi") && *part != "anydpi" {
                        if !densities.contains(&part.to_string()) { densities.push(part.to_string()); }
                    }
                }
            }
        }
    }

    // Unique config strings
    for n in names {
        let l = n.to_lowercase();
        let dir = if l.starts_with("res/") {
            n.split('/').nth(1)
        } else if l.starts_with("base/res/") {
            n.split('/').nth(2)
        } else {
            None
        };
        if let Some(d) = dir {
            if !configs.contains(&d.to_string()) && d.contains('-') {
                configs.push(d.to_string());
            }
        }
    }

    info.resources = ResourceInfo {
        has_resources: true,
        total_entries: total,
        packages: pkg_infos,
        locales,
        densities,
        configurations: configs,
    };
}

// ──────────────────────────────────────────────
// Helpers
// ──────────────────────────────────────────────
fn int_val(v: &crate::manifest::Value) -> i64 {
    match v {
        crate::manifest::Value::Int(i) => *i,
        crate::manifest::Value::Bool(b) => *b as i64,
        crate::manifest::Value::Resource(r) => *r as i64,
        crate::manifest::Value::Str(s) => s.trim().parse::<i64>().unwrap_or(0),
        _ => 0,
    }
}

fn format_resource(v: &crate::manifest::Value) -> Option<String> {
    match v {
        crate::manifest::Value::Resource(r) => Some(format!("@0x{:08x}", r)),
        crate::manifest::Value::Str(s) => Some(s.clone()),
        _ => None,
    }
}

// ──────────────────────────────────────────────
// Legacy convenience functions
// ──────────────────────────────────────────────
pub fn icon_bytes_file(path: &std::path::Path, prefer_round: bool) -> Result<Vec<u8>> {
    // Try pipeline first to get AAPT-derived icon path
    if let Ok(source) = crate::pipeline::select_source_apk(path) {
        // For containers, prefer a container-level icon.png over the inner APK's vector XML
        if source.original_type.is_some() {
            if let Some(ref cp) = source.container_path {
                if let Ok(mut cza) = ZipArchive::open_path(cp) {
                    if let Ok(bytes) = crate::icon::extract_container_top_icon(&mut cza) {
                        return Ok(bytes);
                    }
                }
            }
        }
        if let Ok(info) = crate::pipeline::extract_metadata(&source) {
            let aapt_path = info.icon.resource_path.as_deref();
            let mut za = ZipArchive::open_path(&source.path)?;
            if let Ok(bytes) = crate::icon::extract_best_icon_with_aapt_path(&mut za, aapt_path, prefer_round) {
                return Ok(bytes);
            }
        }
    }
    // Fallback: direct extraction without AAPT info
    let mut za = ZipArchive::open_path(path)?;
    extract_best_icon(&mut za, prefer_round)
}

pub fn manifest_text_file(path: &std::path::Path) -> Result<String> {
    let ptype = detect::detect_file(path)?;
    let mut za = ZipArchive::open_path(path)?;
    let names: Vec<String> = za.entry_names().iter().map(|s| s.to_string()).collect();
    let buf = read_manifest_bytes(&mut za, &names, ptype)
        .ok_or_else(|| AaptError::NotFound("AndroidManifest.xml".into()))?;
    let m = parse_manifest_flexible(&buf)?;
    Ok(manifest_to_text(&m))
}

fn read_manifest_bytes<R: std::io::Read + std::io::Seek>(
    za: &mut ZipArchive<R>,
    names: &[String],
    ptype: PackageType,
) -> Option<Vec<u8>> {
    if ptype == PackageType::Aab {
        let mname = names.iter()
            .find(|e| e.ends_with("manifest/AndroidManifest.xml"))
            .or_else(|| names.iter().find(|e| e.as_str() == "base/AndroidManifest.xml"))
            .cloned();
        return mname.and_then(|m| za.read_entry(&m).ok());
    }
    if matches!(ptype, PackageType::Xapk | PackageType::Apks | PackageType::Apkm) {
        if let Some(base) = detect::base_apk_member(names) {
            if let Ok(bytes) = za.read_entry(&base) {
                if let Ok(mut inner) = ZipArchive::new(std::io::Cursor::new(bytes)) {
                    let inner_names: Vec<String> = inner.entry_names().iter().map(|s| s.to_string()).collect();
                    let mname = if inner_names.iter().any(|e| e == "AndroidManifest.xml") {
                        "AndroidManifest.xml".to_string()
                    } else if inner_names.iter().any(|e| e == "base/AndroidManifest.xml") {
                        "base/AndroidManifest.xml".to_string()
                    } else {
                        return None;
                    };
                    return inner.read_entry(&mname).ok();
                }
            }
        }
        return None;
    }
    let mname = if names.iter().any(|e| e == "AndroidManifest.xml") {
        "AndroidManifest.xml"
    } else if names.iter().any(|e| e == "base/AndroidManifest.xml") {
        "base/AndroidManifest.xml"
    } else {
        return None;
    };
    za.read_entry(mname).ok()
}

fn scan_launcher_in_splits<R: std::io::Read + std::io::Seek>(
    za: &mut ZipArchive<R>,
    names: &[String],
    base: &str,
) -> Option<String> {
    for m in names {
        if !m.ends_with(".apk") || m == base {
            continue;
        }
        let bytes = za.read_entry(m).ok()?;
        let mut inner = ZipArchive::new(std::io::Cursor::new(bytes)).ok()?;
        let inner_names: Vec<String> = inner.entry_names().iter().map(|s| s.to_string()).collect();
        if !inner_names.iter().any(|e| e == "AndroidManifest.xml") {
            continue;
        }
        if let Ok(buf) = inner.read_entry("AndroidManifest.xml") {
            if let Ok(manifest) = parse_manifest_flexible(&buf) {
                if manifest.launcher_activity.is_some() {
                    return manifest.launcher_activity;
                }
            }
        }
    }
    None
}
