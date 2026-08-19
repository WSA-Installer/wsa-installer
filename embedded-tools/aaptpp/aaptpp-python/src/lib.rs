//! Python bindings for AAPT++ (PyO3).
//!
//! Exposes a drop-in replacement for the legacy `aapt.exe` + manual unzip logic
//! used by `app.py`'s `_parse_apk()`:
//!
//! ```python
//! import aaptpp
//! info = aaptpp.info("app.xapk")          # dict, all types auto-detected
//! png  = aaptpp.icon_bytes("app.aab")     # bytes (PNG) or None
//! xml  = aaptpp.manifest("app.apks")      # decoded manifest text
//! v    = aaptpp.verify("app.apk")         # cert/signature summary (read-only)
//! lst  = aaptpp.list_entries("app.apkm")  # list of entry names
//! ```

use aaptpp_core::{
    analyze_file, icon_bytes_file, manifest_text_file, detect_file,
    error::AaptError,
};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyBytes;
use std::path::Path;

fn to_py_err(e: AaptError) -> PyErr {
    PyValueError::new_err(e.to_string())
}

/// Convert a serializable value into a Python dict via `json.loads`.
fn json_to_pydict(py: Python<'_>, value: &impl serde::Serialize) -> PyResult<PyObject> {
    let s = serde_json::to_string(value).map_err(|e| PyValueError::new_err(e.to_string()))?;
    let json_mod = py.import("json")?;
    let obj = json_mod.call_method1("loads", (s,))?;
    Ok(obj.into())
}

/// Return aggregated package information as a dict (JSON-serializable).
#[pyfunction]
fn info(path: &str) -> PyResult<PyObject> {
    let p = Path::new(path);
    let info = analyze_file(p).map_err(to_py_err)?;
    Python::with_gil(|py| json_to_pydict(py, &info))
}

/// Return package information as a JSON string.
#[pyfunction]
fn info_json(path: &str) -> PyResult<String> {
    let p = Path::new(path);
    let info = analyze_file(p).map_err(to_py_err)?;
    serde_json::to_string(&info).map_err(|e| PyValueError::new_err(e.to_string()))
}

/// Extract the best application icon as raw bytes.
/// `fmt` is currently always PNG (ICO conversion can be done by caller).
#[pyfunction(signature = (path, prefer_round=None))]
fn icon_bytes(path: &str, prefer_round: Option<bool>) -> PyResult<Option<PyObject>> {
    let p = Path::new(path);
    match icon_bytes_file(p, prefer_round.unwrap_or(false)) {
        Ok(bytes) => Python::with_gil(|py| Ok(Some(PyBytes::new(py, &bytes).into()))),
        Err(AaptError::NotFound(_)) => Ok(None),
        Err(e) => Err(to_py_err(e)),
    }
}

/// Return the decoded manifest as text.
#[pyfunction]
fn manifest(path: &str) -> PyResult<String> {
    let p = Path::new(path);
    manifest_text_file(p).map_err(to_py_err)
}

/// Return read-only certificate / signature summary as a dict.
#[pyfunction]
fn verify(path: &str) -> PyResult<PyObject> {
    let p = Path::new(path);
    let info = analyze_file(p).map_err(to_py_err)?;
    let summary = serde_json::json!({
        "v1": info.v1,
        "v2": info.v2,
        "v3": info.v3,
        "schemes": info.signing_schemes,
        "certs": info.certs,
    });
    Python::with_gil(|py| json_to_pydict(py, &summary))
}

/// List archive entry names (relative paths).
#[pyfunction]
fn list_entries(path: &str) -> PyResult<Vec<String>> {
    let p = Path::new(path);
    let pt = detect_file(p).map_err(to_py_err)?;
    let mut za = aaptpp_core::archive::ZipArchive::open_path(p).map_err(to_py_err)?;
    let names = za.entry_names();
    let _ = pt;
    Ok(names)
}

/// Detect package type from a file (returns a string like "APK", "XAPK", ...).
#[pyfunction]
fn detect(path: &str) -> PyResult<String> {
    let p = Path::new(path);
    let pt = detect_file(p).map_err(to_py_err)?;
    Ok(pt.as_str().to_string())
}

#[pymodule]
fn aaptpp(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(info, m)?)?;
    m.add_function(wrap_pyfunction!(info_json, m)?)?;
    m.add_function(wrap_pyfunction!(icon_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(manifest, m)?)?;
    m.add_function(wrap_pyfunction!(verify, m)?)?;
    m.add_function(wrap_pyfunction!(list_entries, m)?)?;
    m.add_function(wrap_pyfunction!(detect, m)?)?;
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}
