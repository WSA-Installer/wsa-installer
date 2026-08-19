//! Shared error types for AAPT++ core.

use std::fmt;

#[derive(Debug)]
pub enum AaptError {
    Io(std::io::Error),
    Zip(String),
    BadMagic { expected: String, found: String },
    Parse(String),
    Unsupported(String),
    NotFound(String),
    Crypto(String),
    Other(String),
}

impl fmt::Display for AaptError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AaptError::Io(e) => write!(f, "IO error: {}", e),
            AaptError::Zip(s) => write!(f, "ZIP error: {}", s),
            AaptError::BadMagic { expected, found } => {
                write!(f, "bad magic: expected {}, found {}", expected, found)
            }
            AaptError::Parse(s) => write!(f, "parse error: {}", s),
            AaptError::Unsupported(s) => write!(f, "unsupported: {}", s),
            AaptError::NotFound(s) => write!(f, "not found: {}", s),
            AaptError::Crypto(s) => write!(f, "crypto error: {}", s),
            AaptError::Other(s) => write!(f, "{}", s),
        }
    }
}

impl std::error::Error for AaptError {}

impl From<std::io::Error> for AaptError {
    fn from(e: std::io::Error) -> Self {
        AaptError::Io(e)
    }
}

impl From<flate2::DecompressError> for AaptError {
    fn from(e: flate2::DecompressError) -> Self {
        AaptError::Zip(format!("inflate: {}", e))
    }
}

impl From<flate2::CompressError> for AaptError {
    fn from(e: flate2::CompressError) -> Self {
        AaptError::Zip(format!("deflate: {}", e))
    }
}

pub type Result<T> = std::result::Result<T, AaptError>;
