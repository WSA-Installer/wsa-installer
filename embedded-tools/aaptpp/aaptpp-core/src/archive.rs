//! Streaming ZIP reader. Parses the End Of Central Directory record (and ZIP64
//! variants), the central directory, and extracts entries on demand. Replaces the
//! hand-rolled ZIP reader used by the shell extension with a correct, allocation
//! conscious implementation.

use crate::error::{AaptError, Result};
use flate2::read::DeflateDecoder;
use std::io::{Read, Seek, SeekFrom};
use std::collections::BTreeMap;

const SIG_LOCAL_FILE: u32 = 0x04034b50;
const SIG_CENTRAL_DIR: u32 = 0x02014b50;
const SIG_EOCD: u32 = 0x06054b50;
const SIG_EOCD64: u32 = 0x06064b50;
const SIG_EOCD64_LOC: u32 = 0x07064b50;
const METHOD_STORED: u16 = 0;
const METHOD_DEFLATED: u16 = 8;

#[derive(Clone, Copy, Debug)]
pub enum Compression {
    Stored,
    Deflated,
    Other(u16),
}

#[derive(Clone, Debug)]
pub struct ZipEntry {
    pub name: String,
    pub method: Compression,
    pub compressed_size: u64,
    pub uncompressed_size: u64,
    pub crc32: u32,
    pub local_header_offset: u64,
}

/// Index of all entries in a ZIP archive plus helpers to extract them.
pub struct ZipArchive<R: Read + Seek> {
    reader: R,
    pub entries: BTreeMap<String, ZipEntry>,
}

impl<R: Read + Seek> ZipArchive<R> {
    pub fn new(mut reader: R) -> Result<Self> {
        let (cd_offset, cd_count) = locate_central_directory(&mut reader)?;
        reader.seek(SeekFrom::Start(cd_offset))?;
        let mut entries: BTreeMap<String, ZipEntry> = BTreeMap::new();
        for _ in 0..cd_count {
            let sig = read_u32(&mut reader)?;
            if sig != SIG_CENTRAL_DIR {
                break;
            }
            // version_made_by(2) version_needed(2) flags(2) method(2)
            let _vmade = read_u16(&mut reader)?;
            let _vneed = read_u16(&mut reader)?;
            let _flags = read_u16(&mut reader)?;
            let method = read_u16(&mut reader)?;
            let _modtime = read_u16(&mut reader)?;
            let _moddate = read_u16(&mut reader)?;
            let crc32 = read_u32(&mut reader)?;
            let comp_size = read_u32(&mut reader)? as u64;
            let uncomp_size = read_u32(&mut reader)? as u64;
            let name_len = read_u16(&mut reader)? as usize;
            let extra_len = read_u16(&mut reader)? as usize;
            let comment_len = read_u16(&mut reader)? as usize;
            let _disk_start = read_u16(&mut reader)?;
            let _internal_attr = read_u16(&mut reader)?;
            let _external_attr = read_u32(&mut reader)?;
            let local_off = read_u32(&mut reader)? as u64;

            let mut name_buf = vec![0u8; name_len];
            reader.read_exact(&mut name_buf)?;
            let name = String::from_utf8_lossy(&name_buf).into_owned();

            let mut extra = vec![0u8; extra_len];
            reader.read_exact(&mut extra)?;
            // ZIP64 extra field (id 0x0001) may override sizes/offsets.
            let (comp_size, uncomp_size, local_off) =
                apply_zip64_extra(&extra, comp_size, uncomp_size, local_off);

            let mut comment = vec![0u8; comment_len];
            reader.read_exact(&mut comment)?;

            let method = match method {
                METHOD_STORED => Compression::Stored,
                METHOD_DEFLATED => Compression::Deflated,
                other => Compression::Other(other),
            };

            entries.insert(
                name.clone(),
                ZipEntry {
                    name,
                    method,
                    compressed_size: comp_size,
                    uncompressed_size: uncomp_size,
                    crc32,
                    local_header_offset: local_off,
                },
            );
        }
        Ok(Self { reader, entries })
    }
}

impl ZipArchive<std::fs::File> {
    pub fn open_path(path: &std::path::Path) -> Result<ZipArchive<std::fs::File>> {
        let f = std::fs::File::open(path)?;
        ZipArchive::<std::fs::File>::new(f)
    }
}

impl<R: Read + Seek> ZipArchive<R> {
    /// Extract a single entry into memory.
    pub fn read_entry(&mut self, name: &str) -> Result<Vec<u8>> {
        let entry = self
            .entries
            .get(name)
            .ok_or_else(|| AaptError::NotFound(format!("zip entry {}", name)))?
            .clone();
        match entry.method {
            Compression::Stored => {
                self.seek_local_data(&entry)?;
                let mut buf = vec![0u8; entry.uncompressed_size as usize];
                self.reader.read_exact(&mut buf)?;
                Ok(buf)
            }
            Compression::Deflated => {
                self.seek_local_data(&entry)?;
                let mut comp = vec![0u8; entry.compressed_size as usize];
                self.reader.read_exact(&mut comp)?;
                let mut decoder = DeflateDecoder::new(&comp[..]);
                let mut out = Vec::with_capacity(entry.uncompressed_size as usize);
                decoder.read_to_end(&mut out)?;
                Ok(out)
            }
            Compression::Other(m) => Err(AaptError::Unsupported(format!(
                "compression method {} for {}",
                m, name
            ))),
        }
    }

    /// Extract an entry if present, else None.
    pub fn read_entry_opt(&mut self, name: &str) -> Result<Option<Vec<u8>>> {
        if self.entries.contains_key(name) {
            Ok(Some(self.read_entry(name)?))
        } else {
            Ok(None)
        }
    }

    fn seek_local_data(&mut self, entry: &ZipEntry) -> Result<()> {
        self.reader
            .seek(SeekFrom::Start(entry.local_header_offset))?;
        let sig = read_u32(&mut self.reader)?;
        if sig != SIG_LOCAL_FILE {
            return Err(AaptError::BadMagic {
                expected: format!("{:08x}", SIG_LOCAL_FILE),
                found: format!("{:08x}", sig),
            });
        }
        let _version = read_u16(&mut self.reader)?;
        let _flags = read_u16(&mut self.reader)?;
        let _method = read_u16(&mut self.reader)?;
        let _modtime = read_u16(&mut self.reader)?;
        let _moddate = read_u16(&mut self.reader)?;
        let _crc = read_u32(&mut self.reader)?;
        let _comp = read_u32(&mut self.reader)?;
        let _uncomp = read_u32(&mut self.reader)?;
        let name_len = read_u16(&mut self.reader)? as usize;
        let extra_len = read_u16(&mut self.reader)? as usize;
        self.reader
            .seek(SeekFrom::Current((name_len + extra_len) as i64))?;
        Ok(())
    }

    pub fn entry_names(&self) -> Vec<String> {
        self.entries.keys().cloned().collect()
    }
}

fn apply_zip64_extra(
    extra: &[u8],
    comp_size: u64,
    uncomp_size: u64,
    local_off: u64,
) -> (u64, u64, u64) {
    let mut i = 0;
    let mut comp = comp_size;
    let mut uncomp = uncomp_size;
    let mut off = local_off;
    while i + 4 <= extra.len() {
        let id = u16::from_le_bytes([extra[i], extra[i + 1]]);
        let size = u16::from_le_bytes([extra[i + 2], extra[i + 3]]) as usize;
        let body = &extra[i + 4..];
        if id == 0x0001 && body.len() >= size {
            let mut p = 0;
            if uncomp_size == 0xFFFF_FFFF {
                if p + 8 <= body.len() {
                    uncomp = u64::from_le_bytes(body[p..p + 8].try_into().unwrap());
                    p += 8;
                }
            }
            if comp_size == 0xFFFF_FFFF {
                if p + 8 <= body.len() {
                    comp = u64::from_le_bytes(body[p..p + 8].try_into().unwrap());
                    p += 8;
                }
            }
            if local_off == 0xFFFF_FFFF {
                if p + 8 <= body.len() {
                    off = u64::from_le_bytes(body[p..p + 8].try_into().unwrap());
                }
            }
            break;
        }
        i += 4 + size;
    }
    (comp, uncomp, off)
}

fn locate_central_directory<R: Read + Seek>(reader: &mut R) -> Result<(u64, u64)> {
    let end = reader.seek(SeekFrom::End(0))?;
    if end < 22 {
        return Err(AaptError::Zip("file too small to be a ZIP".into()));
    }
    let tail = (end as usize).min(65536 + 22);
    let tail_start = end - tail as u64;
    reader.seek(SeekFrom::Start(tail_start))?;
    let mut buf = vec![0u8; tail as usize];
    reader.read_exact(&mut buf)?;

    // Search backwards for EOCD signature.
    let mut eocd = None;
    for i in (0..buf.len().saturating_sub(22) + 1).rev() {
        if buf[i..].len() >= 4 && u32::from_le_bytes(buf[i..i + 4].try_into().unwrap()) == SIG_EOCD {
            eocd = Some(i);
            break;
        }
    }
    let eocd = eocd.ok_or_else(|| AaptError::Zip("EOCD not found".into()))?;

    let cd_offset = read_u32_at(&buf, eocd + 16)? as u64;
    let cd_count = read_u16_at(&buf, eocd + 10)? as u64;
    let _cd_size = read_u32_at(&buf, eocd + 12)? as u64;

    // Detect ZIP64 EOCD locator just before the classic EOCD.
    if eocd >= 20 {
        let loc = eocd - 20;
        if u32::from_le_bytes(buf[loc..loc + 4].try_into().unwrap()) == SIG_EOCD64_LOC {
            let eocd64_off = u64::from_le_bytes(buf[loc + 8..loc + 16].try_into().unwrap());
            return Ok((eocd64_off, read_zip64_cd_count(reader, eocd64_off)?));
        }
    }

    Ok((cd_offset, cd_count))
}

fn read_zip64_cd_count<R: Read + Seek>(reader: &mut R, eocd64_off: u64) -> Result<u64> {
    reader.seek(SeekFrom::Start(eocd64_off))?;
    let sig = read_u32(reader)?;
    if sig != SIG_EOCD64 {
        return Err(AaptError::Zip("bad ZIP64 EOCD signature".into()));
    }
    let _size = read_u64(reader)?;
    let _vmade = read_u16(reader)?;
    let _vneed = read_u16(reader)?;
    let _disk = read_u32(reader)?;
    let _cd_disk = read_u32(reader)?;
    let cd_count_this = read_u64(reader)?;
    let _cd_count_total = read_u64(reader)?;
    let _cd_offset = read_u64(reader)?;
    let _comment_len = read_u32(reader)?;
    Ok(cd_count_this)
}

fn read_u16<R: Read>(r: &mut R) -> Result<u16> {
    let mut b = [0u8; 2];
    r.read_exact(&mut b)?;
    Ok(u16::from_le_bytes(b))
}

fn read_u32<R: Read>(r: &mut R) -> Result<u32> {
    let mut b = [0u8; 4];
    r.read_exact(&mut b)?;
    Ok(u32::from_le_bytes(b))
}

fn read_u64<R: Read>(r: &mut R) -> Result<u64> {
    let mut b = [0u8; 8];
    r.read_exact(&mut b)?;
    Ok(u64::from_le_bytes(b))
}

fn read_u16_at(buf: &[u8], off: usize) -> Result<u16> {
    Ok(u16::from_le_bytes(buf[off..off + 2].try_into().unwrap()))
}

fn read_u32_at(buf: &[u8], off: usize) -> Result<u32> {
    Ok(u32::from_le_bytes(buf[off..off + 4].try_into().unwrap()))
}
