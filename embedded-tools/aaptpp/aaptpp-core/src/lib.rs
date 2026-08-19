//! AAPT++ core engine: universal Android package parsing.
//!
//! Supports APK, XAPK, APKS, APKM, AAB, OBB and plain ZIP containers. Provides
//! archive reading, type detection, binary-XML manifest parsing, resources.arsc
//! resolution, icon extraction, and read-only certificate/signature reporting.

pub mod archive;
pub mod aapt_wrapper;
pub mod cert;
pub mod detect;
pub mod error;
pub mod icon;
pub mod info;
pub mod manifest;
pub mod pipeline;
pub mod resources;
pub mod vector_drawable;

pub use error::{AaptError, Result};
pub use info::{analyze_file, analyze_from_archive, icon_bytes_file, manifest_text_file, PackageInfo};
pub use detect::{detect_file, PackageType};
pub use pipeline::select_source_apk;
