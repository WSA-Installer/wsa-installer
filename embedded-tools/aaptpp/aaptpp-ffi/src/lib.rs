//! C-ABI FFI for AAPT++. Consumed by native code such as the WSA Installer
//! Explorer shell extension (`ApkIconShlExt.cpp`) to extract APK metadata and
//! icons correctly (replacing the hand-rolled ZIP reader + manifest guesswork).
//!
//! All string/buffer-returning functions follow this contract:
//!   * First call with `out_buf == NULL`, `out_len == 0` to query the required
//!     size in bytes (excluding the NUL terminator for strings). The return
//!     value is the required size.
//!   * Allocate a buffer of that size (+1 for NUL on strings) and call again
//!     with `out_buf` pointing to it; the function fills it and returns the
//!     number of bytes written.
//!   * Buffers allocated by this library for `aaptpp_*` results must be freed
//!     with `aaptpp_free`.

use aaptpp_core::{
    analyze_file, icon_bytes_file, manifest_text_file,
    icon::png_to_ico,
};
use std::os::raw::{c_char, c_int};
use std::path::Path;
use std::ptr;

/// Opaque handle is not used across calls; result buffers are plain bytes.

unsafe fn write_cstr(out_buf: *mut c_char, out_len: *mut usize, s: &str) -> usize {
    let bytes = s.as_bytes();
    let need = bytes.len() + 1; // include NUL
    if out_buf.is_null() {
        *out_len = need;
        return need;
    }
    let cap = *out_len;
    if cap < need {
        return need;
    }
    for (i, b) in bytes.iter().enumerate() {
        *out_buf.add(i) = *b as c_char;
    }
    *out_buf.add(bytes.len()) = 0;
    need
}

unsafe fn write_bytes(out_buf: *mut u8, out_len: *mut usize, data: &[u8]) -> usize {
    let need = data.len();
    if out_buf.is_null() {
        *out_len = need;
        return need;
    }
    let cap = *out_len;
    if cap < need {
        return need;
    }
    ptr::copy_nonoverlapping(data.as_ptr(), out_buf, need);
    need
}

/// Free a buffer previously returned/allocated by this library via an
/// out_buf query+fill. Call with the same pointer.
#[no_mangle]
pub extern "C" fn aaptpp_free(ptr: *mut u8) {
    if !ptr.is_null() {
        unsafe {
            // We allocated via Vec<u8>::into_raw for string/binary results.
            let _ = Vec::from_raw_parts(ptr, 0, 0);
        }
    }
}

/// Return aggregated package info as a JSON string.
/// Caller frees the returned C string with `aaptpp_free` (cast to u8*).
#[no_mangle]
pub extern "C" fn aaptpp_package_info_json(
    path: *const c_char,
    out_buf: *mut c_char,
    out_len: *mut usize,
) -> usize {
    if path.is_null() || out_len.is_null() {
        return 0;
    }
    let path = unsafe { std::ffi::CStr::from_ptr(path) };
    let path = match path.to_str() {
        Ok(p) => p,
        Err(_) => return 0,
    };
    let info = match analyze_file(Path::new(path)) {
        Ok(i) => i,
        Err(_) => return 0,
    };
    let json = match serde_json::to_string(&info) {
        Ok(j) => j,
        Err(_) => return 0,
    };
    unsafe { write_cstr(out_buf, out_len, &json) }
}

/// Extract the best application icon as PNG bytes.
/// Returns the number of bytes written (or required). For binary data,
/// `out_buf` is a `uint8_t*`. Caller frees with `aaptpp_free`.
#[no_mangle]
pub extern "C" fn aaptpp_extract_best_icon(
    path: *const c_char,
    prefer_round: c_int,
    out_buf: *mut u8,
    out_len: *mut usize,
) -> usize {
    if path.is_null() || out_len.is_null() {
        return 0;
    }
    let path = unsafe { std::ffi::CStr::from_ptr(path) };
    let path = match path.to_str() {
        Ok(p) => p,
        Err(_) => return 0,
    };
    let bytes = match icon_bytes_file(Path::new(path), prefer_round != 0) {
        Ok(b) => b,
        Err(_) => return 0,
    };
    unsafe { write_bytes(out_buf, out_len, &bytes) }
}

/// Resolve the concrete icon resource path (e.g.
/// "res/mipmap-xxxhdpi/ic_launcher.png") declared by the manifest.
/// Returns a NUL-terminated C string; free with `aaptpp_free`.
#[no_mangle]
pub extern "C" fn aaptpp_resolve_icon_path(
    path: *const c_char,
    out_buf: *mut c_char,
    out_len: *mut usize,
) -> usize {
    if path.is_null() || out_len.is_null() {
        return 0;
    }
    let path = unsafe { std::ffi::CStr::from_ptr(path) };
    let path = match path.to_str() {
        Ok(p) => p,
        Err(_) => return 0,
    };
    let resolved = match resolve_icon_path_impl(path) {
        Some(s) => s,
        None => return 0,
    };
    unsafe { write_cstr(out_buf, out_len, &resolved) }
}

/// Convert a PNG buffer to an ICO buffer. `png` points to `png_len` bytes.
/// `out_buf` receives ICO bytes; returns bytes written (or required).
#[no_mangle]
pub extern "C" fn aaptpp_png_to_ico(
    png: *const u8,
    png_len: usize,
    out_buf: *mut u8,
    out_len: *mut usize,
) -> usize {
    if png.is_null() || out_len.is_null() || png_len == 0 {
        return 0;
    }
    let png_slice = unsafe { std::slice::from_raw_parts(png, png_len) };
    let ico = match png_to_ico(png_slice) {
        Ok(v) => v,
        Err(_) => return 0,
    };
    unsafe { write_bytes(out_buf, out_len, &ico) }
}

fn resolve_icon_path_impl(path: &str) -> Option<String> {
    use aaptpp_core::archive::ZipArchive;
    use aaptpp_core::manifest::parse_manifest;
    use aaptpp_core::resources::{parse_resources, pick_best_icon_path, resolve_resource_key};
    let mut za = ZipArchive::open_path(Path::new(path)).ok()?;
    let names = za.entry_names();
    let manifest_name = if names.iter().any(|e| e == "AndroidManifest.xml") {
        "AndroidManifest.xml".to_string()
    } else if names.iter().any(|e| e == "base/AndroidManifest.xml") {
        "base/AndroidManifest.xml".to_string()
    } else {
        return None;
    };
    let mbuf = za.read_entry(&manifest_name).ok()?;
    let m = parse_manifest(&mbuf).ok()?;
    let rid = m.icon_res.or(m.round_icon_res)?;
    let arsc_name = if names.iter().any(|e| e == "resources.arsc") {
        "resources.arsc".to_string()
    } else if names.iter().any(|e| e == "base/resources.arsc") {
        "base/resources.arsc".to_string()
    } else {
        return None;
    };
    let arsc = za.read_entry(&arsc_name).ok()?;
    let table = parse_resources(&arsc).ok()?;
    let key = resolve_resource_key(&table, rid)?;
    pick_best_icon_path(&key, &names)
}
