//! Android binary XML (AndroidManifest.xml) parser.
//!
//! Binary XML chunks:
//!   0x00080003 RES_XML_TYPE
//!   0x001C0001 RES_STRING_POOL_TYPE
//!   0x00080180 RES_XML_RESOURCE_MAP_TYPE
//!   0x00100102 RES_XML_START_NAMESPACE_TYPE
//!   0x00100101 RES_XML_END_NAMESPACE_TYPE
//!   0x00100100 RES_XML_START_ELEMENT_TYPE
//!   0x00100103 RES_XML_END_ELEMENT_TYPE
//!   0x00100104 RES_XML_CDATA_TYPE
//!   0x02020000.. RES_XML_ATTRIBUTE (inline in start element)
//!
//! This parser extracts structured manifest data (package, versions, SDK levels,
//! permissions, components, intent-filters, metadata, and icon resource refs)
//! without relying on string matching of attribute *values* the way the legacy
//! shell extension did.

use crate::error::{AaptError, Result};
use std::collections::HashMap;

// Binary-XML chunk headers are: type(u16) headerSize(u16) size(u32).
const CHUNK_XML_DOC: u16 = 0x0003; // RES_XML_TYPE
const CHUNK_STRING_POOL: u16 = 0x0001; // RES_STRING_POOL_TYPE
const CHUNK_XML_RESOURCE_MAP: u16 = 0x0180; // RES_XML_RESOURCE_MAP_TYPE
const CHUNK_XML_START_NS: u16 = 0x0100;
const CHUNK_XML_END_NS: u16 = 0x0101;
const CHUNK_XML_START_ELEMENT: u16 = 0x0102;
const CHUNK_XML_END_ELEMENT: u16 = 0x0103;
const CHUNK_XML_CDATA: u16 = 0x0104;

#[derive(Clone, Debug)]
pub enum Value {
    /// A resource reference (e.g. android:icon="@mipmap/ic_launcher").
    Resource(u32),
    /// A theme attribute reference (e.g. android:drawable="?attr/colorControlNormal").
    ThemeResource(u32),
    /// A string value.
    Str(String),
    /// An integer (or bool) value.
    Int(i64),
    /// A color / packed value.
    Color(u32),
    /// A null value.
    Null,
    /// Boolean stored inline.
    Bool(bool),
}

impl Value {
    pub fn as_str(&self) -> Option<&str> {
        match self {
            Value::Str(s) => Some(s),
            _ => None,
        }
    }
    pub fn as_resource(&self) -> Option<u32> {
        match self {
            Value::Resource(r) => Some(*r),
            Value::ThemeResource(r) => Some(*r),
            _ => None,
        }
    }
}

#[derive(Clone, Debug)]
pub struct Attribute {
    pub namespace: Option<String>,
    pub name: String,
    pub value: Value,
}

#[derive(Clone, Debug, Default)]
pub struct Element {
    pub namespace: Option<String>,
    pub name: String,
    pub attributes: Vec<Attribute>,
    pub children: Vec<Element>,
    pub text: Option<String>,
}

impl Element {
    pub fn attr(&self, name: &str) -> Option<&Attribute> {
        self.attributes
            .iter()
            .find(|a| a.name == name || a.name.ends_with(&format!(":{}", name)))
    }

    pub fn attr_value(&self, name: &str) -> Option<&Value> {
        self.attr(name).map(|a| &a.value)
    }

    pub fn find(&self, name: &str) -> Option<&Element> {
        if self.name == name {
            return Some(self);
        }
        for c in &self.children {
            if let Some(f) = c.find(name) {
                return Some(f);
            }
        }
        None
    }

    pub fn find_all(&self, name: &str) -> Vec<&Element> {
        let mut out = Vec::new();
        if self.name == name {
            out.push(self);
        }
        for c in &self.children {
            out.extend(c.find_all(name));
        }
        out
    }
}

/// The decoded manifest.
#[derive(Clone, Debug, Default)]
pub struct Manifest {
    pub raw: Element,
    pub package: String,
    pub version_name: Option<String>,
    pub version_code: Option<String>,
    pub compile_sdk: Option<u32>,
    pub compile_sdk_codename: Option<String>,
    pub min_sdk: Option<u32>,
    pub target_sdk: Option<u32>,
    pub install_location: Option<String>,
    pub debuggable: bool,
    pub icon_res: Option<u32>,
    pub round_icon_res: Option<u32>,
    pub label_res: Option<u32>,
    pub label_text: Option<String>,
    pub banner_res: Option<u32>,
    pub permissions: Vec<String>,
    pub activities: Vec<Component>,
    pub services: Vec<Component>,
    pub receivers: Vec<Component>,
    pub providers: Vec<Component>,
    pub metadata: Vec<MetaEntry>,
    pub uses_features: Vec<Feature>,
    pub uses_libraries: Vec<String>,
    pub native_libs: Vec<String>,
    pub launcher_activity: Option<String>,
}

#[derive(Clone, Debug)]
pub struct Component {
    pub name: String,
    pub exported: Option<bool>,
    pub enabled: Option<bool>,
    pub icon_res: Option<u32>,
    pub label_res: Option<u32>,
    pub permission: Option<String>,
    pub intent_filters: Vec<IntentFilter>,
}

#[derive(Clone, Debug)]
pub struct IntentFilter {
    pub actions: Vec<String>,
    pub categories: Vec<String>,
    pub data_schemes: Vec<String>,
    pub browsable: bool,
}

#[derive(Clone, Debug)]
pub struct MetaEntry {
    pub name: String,
    pub value: Option<String>,
    pub resource: Option<u32>,
}

#[derive(Clone, Debug)]
pub struct Feature {
    pub name: Option<String>,
    pub required: bool,
    pub gl_es_version: Option<u32>,
}

/// Parse a binary XML buffer into a [`Manifest`].
pub fn parse_manifest(buf: &[u8]) -> Result<Manifest> {
    let mut p = Parser::new(buf)?;
    let root = p.parse()?;
    Ok(interpret(root))
}

struct Parser<'a> {
    buf: &'a [u8],
    pos: usize,
    strings: Vec<String>,
    /// resource id -> attribute name (from resource map chunk)
    resmap: HashMap<u32, String>,
    namespaces: Vec<(u32, String)>,
}

impl<'a> Parser<'a> {
    fn new(buf: &'a [u8]) -> Result<Self> {
        if buf.len() < 8 {
            return Err(AaptError::Parse("manifest too small".into()));
        }
        let doc_type = u16::from_le_bytes(buf[0..2].try_into().unwrap());
        let _doc_header = u16::from_le_bytes(buf[2..4].try_into().unwrap());
        if doc_type != CHUNK_XML_DOC {
            return Err(AaptError::BadMagic {
                expected: format!("{:04x}", CHUNK_XML_DOC),
                found: format!("{:04x}", doc_type),
            });
        }
        Ok(Self {
            buf,
            pos: 0,
            strings: Vec::new(),
            resmap: HashMap::new(),
            namespaces: Vec::new(),
        })
    }

    fn parse(&mut self) -> Result<Element> {
        // Skip the XML document header (8 bytes: type u16 + header u16 + size u32).
        self.pos = 8;
        let mut stack: Vec<Element> = Vec::new();
        let mut root: Option<Element> = None;
        while self.pos + 8 <= self.buf.len() {
            let chunk_type = self.read_u16()?;
            let header_size = self.read_u16()? as usize;
            let chunk_size = self.read_u32()? as usize;
            if chunk_size < 8 || self.pos - 8 + chunk_size > self.buf.len() {
                break;
            }
            let chunk_start = self.pos - 8;
            match chunk_type {
                CHUNK_STRING_POOL => {
                    let pool = self.read_string_pool_with_size(chunk_start, chunk_size, header_size)?;
                    self.strings = pool;
                }
                CHUNK_XML_RESOURCE_MAP => {
                    // array of u32 resource ids follows the 8-byte header
                    let count = (chunk_size - 8) / 4;
                    for _ in 0..count {
                        let id = self.read_u32()?;
                        // name resolved lazily from attribute's own string index
                        self.resmap.entry(id).or_insert_with(|| format!("{:08x}", id));
                    }
                }
                CHUNK_XML_START_NS => {
                    let _prefix = self.read_u32()?;
                    let uri = self.read_u32()?;
                    self.namespaces.push((uri, self.get_str(uri as usize)?));
                }
                CHUNK_XML_END_NS => {
                    let _prefix = self.read_u32()?;
                    let uri = self.read_u32()?;
                    self.namespaces.retain(|(u, _)| *u != uri);
                }
                CHUNK_XML_START_ELEMENT => {
                    let elem = self.read_element(chunk_start, header_size, chunk_size)?;
                    stack.push(elem);
                }
                CHUNK_XML_END_ELEMENT => {
                    if let Some(closed) = stack.pop() {
                        if let Some(parent) = stack.last_mut() {
                            parent.children.push(closed);
                        } else {
                            root = Some(closed);
                            break;
                        }
                    } else {
                        break;
                    }
                }
                CHUNK_XML_CDATA => {
                    let _idx = self.read_u32()?;
                    let _size = self.read_u32()?;
                    let _lines = self.read_u32()?;
                    let _unk = self.read_u32()?;
                    let _res0 = self.read_u16()?;
                    let _res1 = self.read_u16()?;
                    let data = self.read_u32()?;
                    let _typ = self.read_u16()?;
                    if let Some(parent) = stack.last_mut() {
                        parent.text = Some(self.decode_typed_value(data, 0).unwrap_or_default());
                    }
                }
                _ => {
                    // unknown chunk: skip
                }
            }
            // Advance to next chunk boundary.
            self.pos = chunk_start + chunk_size;
        }
        root.ok_or_else(|| AaptError::Parse("no root element in manifest".into()))
    }

    fn read_element(
        &mut self,
        _chunk_start: usize,
        header_size: usize,
        chunk_size: usize,
    ) -> Result<Element> {
        // After 8-byte chunk header: lineNumber(u32), comment(u32),
        // then attrExt ns(u32), name(u32), attrStart(u16), attrCount(u16),
        // idIndex(u16), classIndex(u16), styleIndex(u16).
        let _line_number = self.read_u32()?;
        let _comment = self.read_u32()?;
        let _ns_uri = self.read_u32()?;
        let name_idx = self.read_u32()? as usize;
        let attr_start = self.read_u16()? as usize;
        let attr_count_field = self.read_u16()? as usize;
        let _id_idx = self.read_u16()?;
        let _class_idx = self.read_u16()?;
        let _style_idx = self.read_u16()?;
        let _reserved = self.read_u16()?; // 2-byte padding before attributes

        // Some toolchains write an unreliable attrCount; derive the real
        // count from the bytes remaining in the chunk after the first attribute.
        let first_attr_off = header_size + attr_start;
        let remaining = chunk_size.saturating_sub(first_attr_off);
        let derived = remaining / 20;
        let attr_count = attr_count_field.min(derived);

        let name = self.get_str(name_idx)?;
        let mut attributes = Vec::with_capacity(attr_count);
        for _ in 0..attr_count {
            let a_ns = self.read_u32()?;
            let a_name_idx = self.read_u32()? as usize;
            let a_raw_value = self.read_u32()?; // raw value (string index for type 0x03)
            let _a_size = self.read_u16()?; // Res_value.size
            let _a_res0 = self.read_u8()?; // Res_value.res0
            let a_value_type = self.read_u8()?; // Res_value.dataType
            let a_data = self.read_u32()?; // Res_value.data

            let ns = if a_ns != 0xFFFFFFFF {
                self.namespaces
                    .iter()
                    .find(|(u, _)| *u == a_ns)
                    .map(|(_, s)| s.clone())
            } else {
                None
            };
            let attr_name = self.get_str(a_name_idx)?;

            // For TYPE_STRING (0x03) the string pool index is in `a_data`.
            // For reference/int/bool/color the value is in `a_data`.
            let value = if a_value_type == 0x03 {
                Value::Str(self.get_str(a_data as usize)?)
            } else if a_data == 0xFFFF_FFFF && a_value_type != 0x01 {
                Value::Null
            } else {
                self.decode_attr_value(a_value_type, a_data)
            };
            let _ = (a_raw_value,);
            attributes.push(Attribute {
                namespace: ns,
                name: attr_name,
                value,
            });
        }
        Ok(Element {
            namespace: None,
            name,
            attributes,
            children: Vec::new(),
            text: None,
        })
    }

    fn decode_attr_value(&self, value_type: u8, raw: u32) -> Value {
        match value_type {
            0x01 => Value::Resource(raw),                       // TYPE_REFERENCE
            0x02 => Value::ThemeResource(raw),                  // TYPE_ATTRIBUTE
            0x10 | 0x11 => Value::Int(raw as i32 as i64),       // int dec / hex
            0x12 => Value::Bool(raw != 0),                      // bool
            0x1c => Value::Color(raw),                          // color
            _ => {
                if raw == 0xFFFF_FFFF {
                    Value::Null
                } else {
                    Value::Int(raw as i32 as i64)
                }
            }
        }
    }

    fn decode_typed_value(&self, _data: u32, _type: u16) -> Option<String> {
        // Best-effort: CDATA values are usually strings already indexed; we return
        // the raw string index decode when possible. Kept simple for now.
        None
    }

    fn read_string_pool(&mut self, start: usize, header_size: usize) -> Result<Vec<String>> {
        // Already at offset `start+8` (after type+headersize+chunksize consumed).
        // Pool header fields (from start):
        //  stringCount(4) styleCount(4) flags(4) stringsStart(4) stylesStart(4)
        // We are currently positioned at start+8.
        let string_count = self.read_u32()? as usize;
        let _style_count = self.read_u32()?;
        let flags = self.read_u32()?;
        let is_utf8 = (flags & 0x100) != 0;
        let strings_start = self.read_u32()? as usize; // offset relative to chunk start
        let _styles_start = self.read_u32()?;

        let offsets_base = start + header_size;

        let mut offsets = Vec::with_capacity(string_count);
        for i in 0..string_count {
            let off = u32::from_le_bytes(
                self.buf[offsets_base + i * 4..offsets_base + i * 4 + 4]
                    .try_into()
                    .unwrap(),
            ) as usize;
            offsets.push(off);
        }
        let strings_start_abs = start + strings_start;
        let mut strings = Vec::with_capacity(string_count);
        for off in offsets {
            let p = strings_start_abs + off;
            let s = if is_utf8 {
                // UTF-8: two length fields (char_len, byte_len), then data
                let (_, adv1) = read_utf8_len(self.buf, p)?;
                let (byte_len, adv2) = read_utf8_len(self.buf, p + adv1)?;
                let bytes = &self.buf[p + adv1 + adv2..p + adv1 + adv2 + byte_len];
                String::from_utf8_lossy(bytes).into_owned()
            } else {
                let len = u16::from_le_bytes(self.buf[p..p + 2].try_into().unwrap()) as usize;
                let units = &self.buf[p + 2..p + 2 + len * 2];
                let mut s = String::with_capacity(len);
                for i in (0..units.len()).step_by(2) {
                    s.push(char::from_u32(u16::from_le_bytes([units[i], units[i + 1]]) as u32).unwrap_or('�'));
                }
                s
            };
            strings.push(s);
        }
        Ok(strings)
    }

    /// Read string pool with chunk_size for position advancement.
    fn read_string_pool_with_size(&mut self, start: usize, chunk_size: usize, header_size: usize) -> Result<Vec<String>> {
        let pool = self.read_string_pool(start, header_size)?;
        // Advance position past this pool
        let pool_end = start + chunk_size;
        if pool_end > self.pos {
            self.pos = pool_end;
        }
        Ok(pool)
    }

    fn get_str(&self, idx: usize) -> Result<String> {
        if idx == 0xFFFF_FFFF {
            return Ok(String::new());
        }
        self.strings
            .get(idx)
            .cloned()
            .ok_or_else(|| AaptError::Parse(format!("string index {} out of range", idx)))
    }

    fn read_u8(&mut self) -> Result<u8> {
        if self.pos >= self.buf.len() {
            return Err(AaptError::Parse("unexpected EOF".into()));
        }
        let b = self.buf[self.pos];
        self.pos += 1;
        Ok(b)
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
}

fn read_utf8_len(buf: &[u8], p: usize) -> Result<(usize, usize)> {
    let first = buf[p] as usize;
    if first < 0x80 {
        Ok((first, 1))
    } else {
        let second = buf[p + 1] as usize;
        let len = ((first & 0x7F) << 8) | second;
        Ok((len, 2))
    }
}

fn interpret(root: Element) -> Manifest {
    let mut m = Manifest {
        raw: root.clone(),
        ..Default::default()
    };
    // Manifest element attributes
    if let Some(pkg) = root.attr_value("package").and_then(|v| v.as_str()) {
        m.package = pkg.to_string();
    }
    if let Some(v) = root.attr_value("versionName").and_then(|v| v.as_str()) {
        m.version_name = Some(v.to_string());
    }
    if let Some(v) = root.attr_value("versionCode") {
        m.version_code = Some(int_to_string(v));
    }
    if let Some(v) = root.attr_value("compileSdkVersion") {
        m.compile_sdk = Some(int_val(v) as u32);
    }
    if let Some(v) = root.attr_value("compileSdkVersionCodename").and_then(|v| v.as_str()) {
        m.compile_sdk_codename = Some(v.to_string());
    }
    if let Some(v) = root.attr_value("minSdkVersion") {
        m.min_sdk = Some(int_val(v) as u32);
    }
    if let Some(v) = root.attr_value("targetSdkVersion") {
        m.target_sdk = Some(int_val(v) as u32);
    }
    // Some manifests (notably AAB protobuf manifests) place these on a
    // dedicated <uses-sdk> child element rather than on <manifest> itself.
    if m.min_sdk.is_none() || m.target_sdk.is_none() {
        if let Some(uses_sdk) = root.find("uses-sdk") {
            if m.min_sdk.is_none() {
                if let Some(v) = uses_sdk.attr_value("minSdkVersion") {
                    m.min_sdk = Some(int_val(v) as u32);
                }
            }
            if m.target_sdk.is_none() {
                if let Some(v) = uses_sdk.attr_value("targetSdkVersion") {
                    m.target_sdk = Some(int_val(v) as u32);
                }
            }
        }
    }
    if let Some(v) = root.attr_value("installLocation").and_then(|v| v.as_str()) {
        m.install_location = Some(v.to_string());
    }
    if let Some(v) = root.attr_value("debuggable") {
        m.debuggable = int_val(v) != 0;
    }
    let app = root.find("application");
    let label_src = app
        .and_then(|a| a.attr_value("label"))
        .or_else(|| root.attr_value("label"));
    if let Some(v) = label_src {
        match v {
            Value::Resource(r) => m.label_res = Some(*r),
            Value::Str(s) => m.label_text = Some(s.clone()),
            _ => {}
        }
    }
    let banner_src = root
        .attr_value("banner")
        .or_else(|| app.and_then(|a| a.attr_value("banner")));
    if let Some(v) = banner_src.and_then(|v| v.as_resource()) {
        m.banner_res = Some(v);
    }

    for perm in root.find_all("uses-permission") {
        if let Some(name) = perm.attr_value("name").and_then(|v| v.as_str()) {
            m.permissions.push(name.to_string());
        }
    }
    for lib in root.find_all("uses-library") {
        if let Some(name) = lib.attr_value("name").and_then(|v| v.as_str()) {
            m.uses_libraries.push(name.to_string());
        }
    }
    for feat in root.find_all("uses-feature") {
        let name = feat.attr_value("name").and_then(|v| v.as_str()).map(|s| s.to_string());
        let required = match feat.attr_value("required") {
            Some(Value::Bool(b)) => *b,
            Some(Value::Int(i)) => *i != 0,
            _ => true,
        };
        let gl = feat.attr_value("glEsVersion").and_then(|v| v.as_resource().or(Some(int_val(v) as u32)));
        m.uses_features.push(Feature {
            name,
            required,
            gl_es_version: gl,
        });
    }

    m.activities = collect_components(&root, "activity");
    m.services = collect_components(&root, "service");
    m.receivers = collect_components(&root, "receiver");
    m.providers = collect_components(&root, "provider");

    for meta in root.find_all("meta-data") {
        let name = meta
            .attr_value("name")
            .and_then(|v| v.as_str())
            .unwrap_or("")
            .to_string();
        let value = meta.attr_value("value").and_then(|v| v.as_str()).map(|s| s.to_string());
        let resource = meta.attr_value("resource").and_then(|v| v.as_resource());
        m.metadata.push(MetaEntry { name, value, resource });
    }

    // Determine launcher activity (action MAIN + category LAUNCHER).
    // Launchers are frequently declared via <activity-alias>, so include those
    // as candidates. We keep `m.activities` limited to real <activity> elements
    // (matching aapt) but search aliases too for the launcher.
    let mut launcher_candidates = collect_components(&root, "activity");
    launcher_candidates.extend(collect_components(&root, "activity-alias"));
    for act in &launcher_candidates {
        let has_main = act
            .intent_filters
            .iter()
            .any(|f| f.actions.iter().any(|a| a == "android.intent.action.MAIN"));
        let has_launcher = act
            .intent_filters
            .iter()
            .any(|f| f.categories.iter().any(|c| c == "android.intent.category.LAUNCHER"));
        if has_main && has_launcher {
            m.launcher_activity = Some(act.name.clone());
            break;
        }
    }

    m
}

fn collect_components(root: &Element, tag: &str) -> Vec<Component> {
    root.find_all(tag)
        .into_iter()
        .map(|e| {
            let name = e
                .attr_value("name")
                .and_then(|v| v.as_str())
                .unwrap_or("")
                .to_string();
            let exported = match e.attr_value("exported") {
                Some(Value::Bool(b)) => Some(*b),
                Some(Value::Int(i)) => Some(*i != 0),
                _ => None,
            };
            let enabled = match e.attr_value("enabled") {
                Some(Value::Bool(b)) => Some(*b),
                Some(Value::Int(i)) => Some(*i != 0),
                _ => None,
            };
            let icon_res = e.attr_value("icon").and_then(|v| v.as_resource());
            let label_res = e.attr_value("label").and_then(|v| v.as_resource());
            let permission = e.attr_value("permission").and_then(|v| v.as_str()).map(|s| s.to_string());
            let mut intent_filters = Vec::new();
            for filt in e.find_all("intent-filter") {
                let actions = filt
                    .find_all("action")
                    .into_iter()
                    .filter_map(|a| a.attr_value("name").and_then(|v| v.as_str()).map(|s| s.to_string()))
                    .collect();
                let categories: Vec<String> = filt
                    .find_all("category")
                    .into_iter()
                    .filter_map(|a| a.attr_value("name").and_then(|v| v.as_str()).map(|s| s.to_string()))
                    .collect();
                let data_schemes: Vec<String> = filt
                    .find_all("data")
                    .into_iter()
                    .filter_map(|a| a.attr_value("scheme").and_then(|v| v.as_str()).map(|s| s.to_string()))
                    .collect();
                let browsable = categories.iter().any(|c| c == "android.intent.category.BROWSABLE");
                intent_filters.push(IntentFilter {
                    actions,
                    categories,
                    data_schemes,
                    browsable,
                });
            }
            Component {
                name,
                exported,
                enabled,
                icon_res,
                label_res,
                permission,
                intent_filters,
            }
        })
        .collect()
}

fn int_val(v: &Value) -> i64 {
    match v {
        Value::Int(i) => *i,
        Value::Bool(b) => *b as i64,
        Value::Resource(r) => *r as i64,
        Value::Str(s) => s.trim().parse::<i64>().unwrap_or(0),
        _ => 0,
    }
}

fn int_to_string(v: &Value) -> String {
    match v {
        Value::Int(i) => i.to_string(),
        Value::Bool(b) => b.to_string(),
        Value::Str(s) => s.clone(),
        _ => String::new(),
    }
}

/// Decode a manifest into pretty-printed XML-ish text (single-line per element).
/// Used by the `manifest` CLI / Python API.
pub fn manifest_to_text(m: &Manifest) -> String {
    let mut s = String::new();
    s.push_str(&format!("package: {}\n", m.package));
    if let Some(v) = &m.version_name {
        s.push_str(&format!("versionName: {}\n", v));
    }
    if let Some(v) = &m.version_code {
        s.push_str(&format!("versionCode: {}\n", v));
    }
    if let Some(v) = m.min_sdk {
        s.push_str(&format!("minSdk: {}\n", v));
    }
    if let Some(v) = m.target_sdk {
        s.push_str(&format!("targetSdk: {}\n", v));
    }
    if let Some(v) = m.compile_sdk {
        s.push_str(&format!("compileSdk: {}\n", v));
    }
    if let Some(r) = m.icon_res {
        s.push_str(&format!("icon: @{:#010x}\n", r));
    }
    if let Some(r) = m.round_icon_res {
        s.push_str(&format!("roundIcon: @{:#010x}\n", r));
    }
    s.push_str(&format!("permissions ({}):\n", m.permissions.len()));
    for p in &m.permissions {
        s.push_str(&format!("  - {}\n", p));
    }
    let dump = |label: &str, comps: &[Component]| {
        let mut out = String::new();
        out.push_str(&format!("{} ({}):\n", label, comps.len()));
        for c in comps {
            out.push_str(&format!("  - {} (exported={:?})\n", c.name, c.exported));
            for f in &c.intent_filters {
                out.push_str(&format!(
                    "      filter actions={:?} categories={:?}\n",
                    f.actions, f.categories
                ));
            }
        }
        out
    };
    s.push_str(&dump("activities", &m.activities));
    s.push_str(&dump("services", &m.services));
    s.push_str(&dump("receivers", &m.receivers));
    s.push_str(&dump("providers", &m.providers));
    s
}

// ----------------------------------------------------------------------------
// Protobuf-encoded manifest support (AAB / `aapt2 --proto-format`).
//
// AAB bundles store `base/manifest/AndroidManifest.xml` as a serialized
// `aapt.pb.XmlNode` message rather than the legacy binary XML chunk format.
// The schema (aapt2 `Resources.proto`) is:
//
//   message XmlNode {
//     XmlElement  element   = 1;
//     string      text      = 2;
//     XmlNamespace namespace = 3;
//   }
//   message XmlElement {
//     string name          = 1;
//     string namespace_uri = 2;
//     XmlAttribute attribute = 3;   // repeated
//     XmlNode child         = 4;    // repeated
//   }
//   message XmlAttribute {
//     string name          = 1;
//     string namespace_uri = 2;
//     string value         = 3;
//     uint32 resource_id   = 4;     // varint
//   }
//
// We decode this into the same `Element` tree the binary-XML parser produces so
// the rest of the pipeline (interpret / info) is shared.
// ----------------------------------------------------------------------------

const ANDROID_NS: &str = "http://schemas.android.com/apk/res/android";

fn read_varint(buf: &[u8], pos: &mut usize) -> Result<u64> {
    let mut result: u64 = 0;
    let mut shift = 0u32;
    loop {
        if *pos >= buf.len() {
            return Err(AaptError::Parse("varint past end".into()));
        }
        let b = buf[*pos];
        *pos += 1;
        result |= ((b & 0x7F) as u64) << shift;
        if b & 0x80 == 0 {
            break;
        }
        shift += 7;
        if shift >= 64 {
            return Err(AaptError::Parse("varint too long".into()));
        }
    }
    Ok(result)
}

fn read_len_delimited<'a>(buf: &'a [u8], pos: &mut usize) -> Result<&'a [u8]> {
    let len = read_varint(buf, pos)? as usize;
    if *pos + len > buf.len() {
        return Err(AaptError::Parse("length-delimited past end".into()));
    }
    let data = &buf[*pos..*pos + len];
    *pos += len;
    Ok(data)
}

fn read_string(buf: &[u8], pos: &mut usize) -> Result<String> {
    let data = read_len_delimited(buf, pos)?;
    Ok(String::from_utf8_lossy(data).into_owned())
}

/// Decode a `XmlNode` message body into an `Element`.
fn proto_xml_node(data: &[u8]) -> Result<Element> {
    let mut pos = 0;
    let mut element: Option<Element> = None;
    let mut text: Option<String> = None;
    while pos < data.len() {
        let tag = read_varint(data, &mut pos)? as u32;
        let field = tag >> 3;
        let wire = (tag & 0x7) as u8;
        match (field, wire) {
            (1, 2) => {
                let body = read_len_delimited(data, &mut pos)?;
                element = Some(proto_xml_element(body)?);
            }
            (2, 2) => {
                text = Some(read_string(data, &mut pos)?);
            }
            (3, 2) => {
                // SourcePosition: skip.
                let _ = read_len_delimited(data, &mut pos)?;
            }
            _ => {
                if wire == 0 {
                    let _ = read_varint(data, &mut pos)?;
                } else if wire == 2 {
                    let _ = read_len_delimited(data, &mut pos)?;
                } else if wire == 5 {
                    pos += 4;
                } else if wire == 1 {
                    pos += 8;
                } else {
                    return Err(AaptError::Parse("unknown proto wire type".into()));
                }
            }
        }
    }
    match element {
        Some(e) => Ok(e),
        None => Ok(Element {
            text,
            ..Default::default()
        }),
    }
}

fn proto_xml_element(data: &[u8]) -> Result<Element> {
    let mut pos = 0;
    let mut name = String::new();
    let mut ns_uri = String::new();
    let mut attributes = Vec::new();
    let mut children = Vec::new();
    while pos < data.len() {
        let tag = read_varint(data, &mut pos)? as u32;
        let field = tag >> 3;
        let wire = (tag & 0x7) as u8;
        match (field, wire) {
            (1, 2) => {
                // namespace_declaration (XmlNamespace): skip.
                let _ = read_len_delimited(data, &mut pos)?;
            }
            (2, 2) => ns_uri = read_string(data, &mut pos)?,
            (3, 2) => name = read_string(data, &mut pos)?,
            (4, 2) => {
                let body = read_len_delimited(data, &mut pos)?;
                attributes.push(proto_xml_attribute(body)?);
            }
            (5, 2) => {
                let body = read_len_delimited(data, &mut pos)?;
                children.push(proto_xml_node(body)?);
            }
            _ => {
                if wire == 0 {
                    let _ = read_varint(data, &mut pos)?;
                } else if wire == 2 {
                    let _ = read_len_delimited(data, &mut pos)?;
                } else if wire == 5 {
                    pos += 4;
                } else if wire == 1 {
                    pos += 8;
                } else {
                    return Err(AaptError::Parse("unknown proto wire type".into()));
                }
            }
        }
    }
    let _ = ns_uri;
    Ok(Element {
        name,
        attributes,
        children,
        ..Default::default()
    })
}

fn proto_xml_attribute(data: &[u8]) -> Result<Attribute> {
    let mut pos = 0;
    let mut name = String::new();
    let mut ns_uri = String::new();
    let mut value = String::new();
    let mut res_id = 0u32;
    while pos < data.len() {
        let tag = read_varint(data, &mut pos)? as u32;
        let field = tag >> 3;
        let wire = (tag & 0x7) as u8;
        match (field, wire) {
            (1, 2) => ns_uri = read_string(data, &mut pos)?,
            (2, 2) => name = read_string(data, &mut pos)?,
            (3, 2) => value = read_string(data, &mut pos)?,
            (5, 0) => res_id = read_varint(data, &mut pos)? as u32,
            _ => {
                if wire == 0 {
                    let _ = read_varint(data, &mut pos)?;
                } else if wire == 2 {
                    let _ = read_len_delimited(data, &mut pos)?;
                } else if wire == 5 {
                    pos += 4;
                } else if wire == 1 {
                    pos += 8;
                } else {
                    return Err(AaptError::Parse("unknown proto wire type".into()));
                }
            }
        }
    }
    // Mirror binary-XML naming: android-namespaced attributes become "android:name".
    let prefixed = if ns_uri == ANDROID_NS && !name.starts_with("android:") {
        format!("android:{}", name)
    } else {
        name.clone()
    };
    // Prefer the compiled resource id when present — the text value is merely
    // the source-level representation (e.g. "@mipmap/ic_launcher") while the
    // resource id is what we need for icon/label resolution.
    let value = if res_id != 0 {
        Value::Resource(res_id)
    } else if !value.is_empty() {
        Value::Str(value)
    } else {
        Value::Str(String::new())
    };
    Ok(Attribute {
        namespace: if ns_uri.is_empty() { None } else { Some(ns_uri) },
        name: prefixed,
        value,
    })
}

/// Parse a manifest that may be encoded either as binary XML or as an
/// `aapt.pb.XmlNode` protobuf (AAB). Tries binary XML first and falls back to
/// the protobuf decoder.
pub fn parse_manifest_flexible(buf: &[u8]) -> Result<Manifest> {
    match parse_manifest(buf) {
        Ok(m) => Ok(m),
        Err(AaptError::BadMagic { .. }) => {
            let root = proto_xml_node(buf)?;
            Ok(interpret(root))
        }
        Err(e) => Err(e),
    }
}
