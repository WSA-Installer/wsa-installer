use std::path::{Path, PathBuf};
use std::process::Command;
use std::sync::OnceLock;

use crate::error::{AaptError, Result};

static AAPT_LOCK: OnceLock<Option<PathBuf>> = OnceLock::new();

/// Return `{exe_dir}/aap++/runtime/`, creating it if missing.
fn runtime_dir() -> PathBuf {
    let exe = std::env::current_exe().unwrap_or_else(|_| PathBuf::from("."));
    let dir = exe.parent().unwrap_or(Path::new(".")).join("aap++").join("runtime");
    let _ = std::fs::create_dir_all(&dir);
    dir
}

#[derive(Clone, Debug, Default)]
pub struct BadgingInfo {
    pub package: String,
    pub label: String,
    pub version_name: String,
    pub version_code: String,
    pub min_sdk: Option<u32>,
    pub target_sdk: Option<u32>,
    pub launcher: Option<String>,
    pub density_icons: Vec<(u32, String)>,
    pub icon_path: Option<String>,
    pub permissions: Vec<String>,
    pub features: Vec<String>,
    pub libraries: Vec<String>,
}

pub const EMBEDDED_AAPT: &[u8] = include_bytes!(concat!(env!("CARGO_MANIFEST_DIR"), "/../assets/aapt.exe"));

/// Write embedded aapt.exe to a runtime file and return its path.
pub fn extract_embedded_aapt() -> Result<PathBuf> {
    let aapt_path = runtime_dir().join("aapt.exe");

    let should_write = if aapt_path.exists() {
        let existing = std::fs::read(&aapt_path).ok();
        existing.map(|b| b != EMBEDDED_AAPT).unwrap_or(true)
    } else {
        true
    };

    if should_write {
        std::fs::write(&aapt_path, EMBEDDED_AAPT).map_err(|e| AaptError::Io(e))?;
    }

    Ok(aapt_path)
}

pub fn find_aapt() -> Option<PathBuf> {
    AAPT_LOCK
        .get_or_init(|| {
            let path = runtime_dir().join("aapt.exe");
            if path.exists() {
                return Some(path);
            }
            extract_embedded_aapt().ok()
        })
        .clone()
}

pub fn dump_badging(apk_path: &Path) -> Result<BadgingInfo> {
    let aapt = find_aapt().ok_or_else(|| AaptError::NotFound("aapt.exe not available".into()))?;

    let output = Command::new(&aapt)
        .args(["dump", "badging"])
        .arg(apk_path)
        .output()
        .map_err(|e| AaptError::Io(e))?;

    // Always try to parse stdout, even if exit code is non-zero
    let text = String::from_utf8_lossy(&output.stdout);
    if text.trim().is_empty() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        return Err(AaptError::Parse(format!("aapt dump badging produced no output: {}", stderr)));
    }
    parse_badging(&text)
}

fn parse_badging(text: &str) -> Result<BadgingInfo> {
    let mut info = BadgingInfo::default();

    for line in text.lines() {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }

        if line.starts_with("package:") {
            let v = extract_quoted(line, "name='");
            if !v.is_empty() {
                info.package = v;
            }
            let vc = extract_quoted(line, "versionCode='");
            if !vc.is_empty() {
                info.version_code = vc;
            }
            let vn = extract_quoted(line, "versionName='");
            if !vn.is_empty() {
                info.version_name = vn;
            }
        } else if line.starts_with("application-label:") {
            let v = extract_quoted(line, "'");
            if !v.is_empty() {
                info.label = v;
            }
        } else if line.starts_with("application-icon-") {
            let rest = line.strip_prefix("application-icon-").unwrap_or("");
            let density_str: String = rest.chars().take_while(|c| c.is_ascii_digit()).collect();
            if let Ok(density) = density_str.parse::<u32>() {
                if let Some(path) = rest
                    .strip_prefix(&density_str)
                    .and_then(|s| extract_single_quoted(s))
                {
                    info.density_icons.push((density, path));
                }
            }
        } else if line.starts_with("application:") {
            let v = extract_quoted(line, "icon='");
            if !v.is_empty() {
                info.icon_path = Some(v);
            }
        } else if line.starts_with("launchable-activity:") {
            let v = extract_quoted(line, "name='");
            if !v.is_empty() {
                info.launcher = Some(v);
            }
        } else if line.starts_with("sdkVersion:") {
            let v = extract_quoted(line, "'");
            info.min_sdk = v.parse().ok();
        } else if line.starts_with("targetSdkVersion:") {
            let v = extract_quoted(line, "'");
            info.target_sdk = v.parse().ok();
        } else if line.starts_with("uses-permission:") {
            let v = extract_quoted(line, "name='");
            if !v.is_empty() {
                info.permissions.push(v);
            }
        } else if line.starts_with("uses-feature:") {
            let v = extract_quoted(line, "name='");
            if !v.is_empty() {
                info.features.push(v);
            }
        } else if line.starts_with("uses-library:") || line.starts_with("uses-library-not-required:") {
            let v = extract_quoted(line, "name='");
            if !v.is_empty() {
                info.libraries.push(v);
            }
        }
    }

    info.density_icons.sort_by(|a, b| b.0.cmp(&a.0));

    Ok(info)
}

fn extract_quoted<'a>(line: &'a str, prefix: &str) -> String {
    if let Some(start) = line.find(prefix) {
        let after = &line[start + prefix.len()..];
        let mut result = String::new();
        let mut escaped = false;
        for c in after.chars() {
            if escaped {
                result.push(c);
                escaped = false;
                continue;
            }
            if c == '\\' {
                escaped = true;
                continue;
            }
            if c == '\'' {
                break;
            }
            result.push(c);
        }
        result
    } else {
        String::new()
    }
}

fn extract_single_quoted<'a>(s: &'a str) -> Option<String> {
    let s = s.trim();
    if s.starts_with('\'') {
        let mut result = String::new();
        let mut escaped = false;
        for c in s[1..].chars() {
            if escaped {
                result.push(c);
                escaped = false;
                continue;
            }
            if c == '\\' {
                escaped = true;
                continue;
            }
            if c == '\'' {
                break;
            }
            result.push(c);
        }
        Some(result)
    } else {
        None
    }
}
