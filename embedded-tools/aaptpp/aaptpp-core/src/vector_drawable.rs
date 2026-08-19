use crate::error::{AaptError, Result};
use crate::manifest::{parse_manifest_flexible, Value};
use flate2::write::ZlibEncoder;
use flate2::Compression;
use std::io::Write;

macro_rules! dbglog {
    ($($arg:tt)*) => {
        if std::env::var("AAPT_DEBUG").is_ok() {
            eprintln!("[DEBUG] {}", format!($($arg)*));
        }
    };
}

// ── Path data types ──────────────────────────────────────────

#[derive(Clone, Debug)]
enum Segment {
    MoveTo(f64, f64),
    LineTo(f64, f64),
    CubicTo(f64, f64, f64, f64, f64, f64),
    QuadTo(f64, f64, f64, f64),
    ArcTo(f64, f64, f64, bool, bool, f64, f64),
    Close,
}

fn parse_svg_path(s: &str) -> Result<Vec<Segment>> {
    let mut segs: Vec<Segment> = Vec::new();
    let bytes = s.as_bytes();
    let len = bytes.len();
    let mut i = 0;
    let mut cur_cmd = 0u8;
    let mut implicit = false;
    let mut last = (0.0f64, 0.0f64);
    let mut start = (0.0f64, 0.0f64);

    while i < len {
        while i < len && bytes[i].is_ascii_whitespace() || bytes[i] == b',' {
            i += 1;
        }
        if i >= len {
            break;
        }
        let b = bytes[i];
        if b.is_ascii_alphabetic() && b != b'e' && b != b'E' {
            cur_cmd = b;
            i += 1;
        } else if !implicit {
            break;
        }

        match cur_cmd {
            b'M' | b'm' => {
                let (x, y) = read_coord_pair(bytes, &mut i)?;
                let rel = cur_cmd == b'm';
                let pt = if rel { (last.0 + x, last.1 + y) } else { (x, y) };
                segs.push(Segment::MoveTo(pt.0, pt.1));
                last = pt;
                start = pt;
                cur_cmd = if rel { b'l' } else { b'L' };
                implicit = true;
            }
            b'L' | b'l' => {
                let (x, y) = read_coord_pair(bytes, &mut i)?;
                let rel = cur_cmd == b'l';
                let pt = if rel { (last.0 + x, last.1 + y) } else { (x, y) };
                segs.push(Segment::LineTo(pt.0, pt.1));
                last = pt;
                implicit = true;
            }
            b'H' | b'h' => {
                let x = read_coord(bytes, &mut i)?;
                let rel = cur_cmd == b'h';
                let pt = if rel { (last.0 + x, last.1) } else { (x, last.1) };
                segs.push(Segment::LineTo(pt.0, pt.1));
                last = pt;
                implicit = true;
            }
            b'V' | b'v' => {
                let y = read_coord(bytes, &mut i)?;
                let rel = cur_cmd == b'v';
                let pt = if rel { (last.0, last.1 + y) } else { (last.0, y) };
                segs.push(Segment::LineTo(pt.0, pt.1));
                last = pt;
                implicit = true;
            }
            b'C' | b'c' => {
                let (x1, y1) = read_coord_pair(bytes, &mut i)?;
                let (x2, y2) = read_coord_pair(bytes, &mut i)?;
                let (x, y) = read_coord_pair(bytes, &mut i)?;
                let rel = cur_cmd == b'c';
                let f = |v: f64, _r: f64| if rel { last.0 + v } else { v };
                let g = |v: f64, _r: f64| if rel { last.1 + v } else { v };
                let pt = (f(x, 0.0), g(y, 0.0));
                segs.push(Segment::CubicTo(f(x1, 0.0), g(y1, 0.0), f(x2, 0.0), g(y2, 0.0), pt.0, pt.1));
                last = pt;
                implicit = true;
            }
            b'S' | b's' => {
                let (x2, y2) = read_coord_pair(bytes, &mut i)?;
                let (x, y) = read_coord_pair(bytes, &mut i)?;
                let rel = cur_cmd == b's';
                let (rx, ry) = reflect_control(last, segs.last());
                let f = |v: f64, _r: f64| if rel { last.0 + v } else { v };
                let g = |v: f64, _r: f64| if rel { last.1 + v } else { v };
                let pt = (f(x, 0.0), g(y, 0.0));
                segs.push(Segment::CubicTo(rx, ry, f(x2, 0.0), g(y2, 0.0), pt.0, pt.1));
                last = pt;
                implicit = true;
            }
            b'Q' | b'q' => {
                let (x1, y1) = read_coord_pair(bytes, &mut i)?;
                let (x, y) = read_coord_pair(bytes, &mut i)?;
                let rel = cur_cmd == b'q';
                let f = |v: f64, _r: f64| if rel { last.0 + v } else { v };
                let g = |v: f64, _r: f64| if rel { last.1 + v } else { v };
                let pt = (f(x, 0.0), g(y, 0.0));
                segs.push(Segment::QuadTo(f(x1, 0.0), g(y1, 0.0), pt.0, pt.1));
                last = pt;
                implicit = true;
            }
            b'T' | b't' => {
                let (x, y) = read_coord_pair(bytes, &mut i)?;
                let rel = cur_cmd == b't';
                let (rx, ry) = reflect_control(last, segs.last());
                let f = |v: f64, _r: f64| if rel { last.0 + v } else { v };
                let g = |v: f64, _r: f64| if rel { last.1 + v } else { v };
                let pt = (f(x, 0.0), g(y, 0.0));
                segs.push(Segment::QuadTo(rx, ry, pt.0, pt.1));
                last = pt;
                implicit = true;
            }
            b'A' | b'a' => {
                let rx = read_coord(bytes, &mut i)?;
                let ry = read_coord(bytes, &mut i)?;
                let rot = read_coord(bytes, &mut i)?;
                let laf = read_flag(bytes, &mut i)?;
                let sf = read_flag(bytes, &mut i)?;
                let (x, y) = read_coord_pair(bytes, &mut i)?;
                let rel = cur_cmd == b'a';
                let pt = if rel { (last.0 + x, last.1 + y) } else { (x, y) };
                segs.push(Segment::ArcTo(rx, ry, rot, laf, sf, pt.0, pt.1));
                last = pt;
                implicit = true;
            }
            b'Z' | b'z' => {
                segs.push(Segment::Close);
                last = start;
                implicit = true;
            }
            _ => break,
        }
    }
    Ok(segs)
}

fn read_coord(bytes: &[u8], i: &mut usize) -> Result<f64> {
    skip_ws_comma(bytes, i);
    if *i >= bytes.len() {
        return Err(AaptError::Parse("unexpected end in path".into()));
    }
    let start = *i;
    if bytes[*i] == b'-' || bytes[*i] == b'+' {
        *i += 1;
    }
    while *i < bytes.len() && (bytes[*i].is_ascii_digit() || bytes[*i] == b'.' || bytes[*i] == b'e' || bytes[*i] == b'E' || bytes[*i] == b'-' || bytes[*i] == b'+') {
        if bytes[*i] == b'-' || bytes[*i] == b'+' {
            if *i > start && bytes[*i - 1] != b'e' && bytes[*i - 1] != b'E' {
                break;
            }
        }
        *i += 1;
    }
    let s = std::str::from_utf8(&bytes[start..*i]).map_err(|_| AaptError::Parse("invalid utf-8 in path".into()))?;
    if s.is_empty() {
        return Err(AaptError::Parse("empty coord in path".into()));
    }
    s.parse::<f64>().map_err(|_| AaptError::Parse(format!("bad coord: {}", s)))
}

fn read_coord_pair(bytes: &[u8], i: &mut usize) -> Result<(f64, f64)> {
    let x = read_coord(bytes, i)?;
    let y = read_coord(bytes, i)?;
    Ok((x, y))
}

fn read_flag(bytes: &[u8], i: &mut usize) -> Result<bool> {
    skip_ws_comma(bytes, i);
    if *i >= bytes.len() {
        return Err(AaptError::Parse("unexpected end for flag".into()));
    }
    let v = bytes[*i] == b'1';
    *i += 1;
    Ok(v)
}

fn skip_ws_comma(bytes: &[u8], i: &mut usize) {
    while *i < bytes.len() && (bytes[*i].is_ascii_whitespace() || bytes[*i] == b',') {
        *i += 1;
    }
}

fn reflect_control(last: (f64, f64), prev: Option<&Segment>) -> (f64, f64) {
    match prev {
        Some(Segment::CubicTo(_, _, x2, y2, _, _)) => (2.0 * last.0 - x2, 2.0 * last.1 - y2),
        Some(Segment::QuadTo(x1, y1, _, _)) => (2.0 * last.0 - x1, 2.0 * last.1 - y1),
        _ => last,
    }
}

// ── Flatten curves to line segments ──────────────────────────

fn flatten(segs: &[Segment], tolerance: f64) -> Vec<(f64, f64)> {
    let mut pts: Vec<(f64, f64)> = Vec::new();
    let mut cx = 0.0;
    let mut cy = 0.0;
    let mut sx = 0.0;
    let mut sy = 0.0;
    let mut first = true;
    for seg in segs {
        match *seg {
            Segment::MoveTo(x, y) => {
                if !first {
                    pts.push((cx, cy));
                }
                pts.push((x, y));
                cx = x;
                cy = y;
                sx = x;
                sy = y;
                first = false;
            }
            Segment::LineTo(x, y) => {
                pts.push((x, y));
                cx = x;
                cy = y;
            }
            Segment::CubicTo(x1, y1, x2, y2, x3, y3) => {
                flatten_cubic(cx, cy, x1, y1, x2, y2, x3, y3, tolerance, &mut pts);
                cx = x3;
                cy = y3;
            }
            Segment::QuadTo(x1, y1, x2, y2) => {
                let (cx1, cy1, cx2, cy2) = quad_to_cubic(cx, cy, x1, y1, x2, y2);
                flatten_cubic(cx, cy, cx1, cy1, cx2, cy2, x2, y2, tolerance, &mut pts);
                cx = x2;
                cy = y2;
            }
            Segment::ArcTo(rx, ry, rot, laf, sf, x, y) => {
                flatten_arc(cx, cy, rx, ry, rot, laf, sf, x, y, tolerance, &mut pts);
                cx = x;
                cy = y;
            }
            Segment::Close => {
                pts.push((sx, sy));
                cx = sx;
                cy = sy;
            }
        }
    }
    pts
}

fn quad_to_cubic(x0: f64, y0: f64, x1: f64, y1: f64, x2: f64, y2: f64) -> (f64, f64, f64, f64) {
    let cx1 = x0 + 2.0 / 3.0 * (x1 - x0);
    let cy1 = y0 + 2.0 / 3.0 * (y1 - y0);
    let cx2 = x2 + 2.0 / 3.0 * (x1 - x2);
    let cy2 = y2 + 2.0 / 3.0 * (y1 - y2);
    (cx1, cy1, cx2, cy2)
}

fn flatten_cubic(
    x0: f64, y0: f64, x1: f64, y1: f64, x2: f64, y2: f64, x3: f64, y3: f64,
    tol: f64, pts: &mut Vec<(f64, f64)>,
) {
    let tol2 = tol * tol;
    let mut stack: Vec<(f64, f64, f64, f64, f64, f64, f64, f64)> = Vec::new();
    stack.push((x0, y0, x1, y1, x2, y2, x3, y3));
    while let Some((x0, y0, x1, y1, x2, y2, x3, y3)) = stack.pop() {
        let dx = x3 - x0;
        let dy = y3 - y0;
        let d2 = ((x1 - x3) * dy - (y1 - y3) * dx).abs();
        let d3 = ((x2 - x3) * dy - (y2 - y3) * dx).abs();
        if (d2 + d3) * (d2 + d3) <= tol2 * (dx * dx + dy * dy) {
            pts.push((x3, y3));
        } else {
            let mx0 = (x0 + x1) * 0.5;
            let my0 = (y0 + y1) * 0.5;
            let mx1 = (x1 + x2) * 0.5;
            let my1 = (y1 + y2) * 0.5;
            let mx2 = (x2 + x3) * 0.5;
            let my2 = (y2 + y3) * 0.5;
            let nx0 = (mx0 + mx1) * 0.5;
            let ny0 = (my0 + my1) * 0.5;
            let nx1 = (mx1 + mx2) * 0.5;
            let ny1 = (my1 + my2) * 0.5;
            let cx = (nx0 + nx1) * 0.5;
            let cy = (ny0 + ny1) * 0.5;
            stack.push((nx0, ny0, nx1, ny1, cx, cy, x3, y3));
            stack.push((x0, y0, mx0, my0, nx0, ny0, cx, cy));
        }
    }
}

fn flatten_arc(
    cx: f64, cy: f64, rx: f64, ry: f64, rot: f64, _laf: bool, _sf: bool, _x: f64, _y: f64,
    _tol: f64, pts: &mut Vec<(f64, f64)>,
) {
    let segments = 16usize;
    let angle_step = std::f64::consts::TAU / segments as f64;
    let cos_r = rot.to_radians().cos();
    let sin_r = rot.to_radians().sin();
    for i in 1..=segments {
        let a = angle_step * i as f64;
        let ex = cx + rx * a.cos() * cos_r - ry * a.sin() * sin_r;
        let ey = cy + rx * a.cos() * sin_r + ry * a.sin() * cos_r;
        pts.push((ex, ey));
    }
}

// ── Scanline rasterizer ──────────────────────────────────────

#[derive(Clone, Default, Debug)]
struct Rgba {
    r: u16, g: u16, b: u16, a: u16,
}

struct Canvas {
    w: usize,
    h: usize,
    buf: Vec<Rgba>,
}

impl Canvas {
    fn new(w: usize, h: usize) -> Self {
        Canvas { w, h, buf: vec![Rgba::default(); w * h] }
    }

    fn fill_path(&mut self, pts: &[(f64, f64)], color: Rgba, viewport_w: f64, viewport_h: f64) {
        if color.a == 0 || pts.len() < 3 {
            return;
        }
        let scale_x = self.w as f64 / viewport_w;
        let scale_y = self.h as f64 / viewport_h;
        let mut sp: Vec<(f64, f64)> = pts.iter().map(|&(x, y)| (x * scale_x, y * scale_y)).collect();
        // Remove trailing closed point if redundant
        if sp.len() > 1 && (sp[0].0 - sp[sp.len() - 1].0).abs() < 1e-6 && (sp[0].1 - sp[sp.len() - 1].1).abs() < 1e-6 {
            sp.pop();
        }
        if sp.len() < 3 {
            return;
        }

        let sub = 8usize;
        let sub_f = sub as f64;
        let mut coverage = vec![0u16; self.w * sub * self.h * sub];

        // Build edge list
        for i in 0..sp.len() {
            let j = (i + 1) % sp.len();
            let (x1, y1) = sp[i];
            let (x2, y2) = sp[j];
            if (y1 - y2).abs() < 1e-9 {
                continue;
            }
            let (x1, y1, x2, y2) = if y1 < y2 { (x1, y1, x2, y2) } else { (x2, y2, x1, y1) };
            let dx = (x2 - x1) / (y2 - y1);
            let _sub_h = (self.h * sub) as f64;

            let y_start = (y1.max(0.0) * sub_f).ceil() as isize;
            let y_end = ((y2.min(self.h as f64)) * sub_f).floor() as isize;
            if y_start >= y_end {
                continue;
            }

            let mut cur_x = x1 + dx * (y_start as f64 / sub_f - y1);
            for sy in y_start..y_end {
                if sy < 0 || sy as usize >= self.h * sub {
                    cur_x += dx / sub_f;
                    continue;
                }
                let next_x = cur_x + dx / sub_f;
                                let sx_start = ((cur_x.min(next_x)).max(0.0) * sub_f).floor() as isize;
                                let sx_end = ((cur_x.max(next_x)).min(self.w as f64) * sub_f).ceil() as isize;
                for sx in sx_start..sx_end {
                    if sx >= 0 && (sx as usize) < self.w * sub {
                        coverage[sy as usize * (self.w * sub) + sx as usize] ^= 1;
                    }
                }
                cur_x = next_x;
            }
        }

        // Resolve coverage to pixels
        if color.a == 65535 {
            for py in 0..self.h {
                for px in 0..self.w {
                    let mut cov = 0u32;
                    for dy in 0..sub {
                        for dx in 0..sub {
                            cov += coverage[(py * sub + dy) * (self.w * sub) + (px * sub + dx)] as u32;
                        }
                    }
                    if cov > 0 {
                        let a = ((cov * 255 + sub as u32 * sub as u32 / 2) / (sub as u32 * sub as u32)) as u16;
                        let idx = py * self.w + px;
                        let src = &color;
                        let dst = &self.buf[idx];
                        let aa = a as u32;
                        let ia = 255 - aa;
                        self.buf[idx] = Rgba {
                            r: ((src.r as u32 * aa + dst.r as u32 * ia) / 255) as u16,
                            g: ((src.g as u32 * aa + dst.g as u32 * ia) / 255) as u16,
                            b: ((src.b as u32 * aa + dst.b as u32 * ia) / 255) as u16,
                            a: ((aa + (dst.a as u32 * ia) / 255).min(255) * 0x0101) as u16,
                        };
                    }
                }
            }
        } else {
            // Non-opaque color
            let src_a = color.a as u32;
            for py in 0..self.h {
                for px in 0..self.w {
                    let mut cov = 0u32;
                    for dy in 0..sub {
                        for dx in 0..sub {
                            cov += coverage[(py * sub + dy) * (self.w * sub) + (px * sub + dx)] as u32;
                        }
                    }
                    if cov > 0 {
                        let cov_norm = ((cov * 255 + sub as u32 * sub as u32 / 2) / (sub as u32 * sub as u32)) as u32;
                        let alpha = (src_a * cov_norm) / 255;
                        let ia = 255 - alpha;
                        let idx = py * self.w + px;
                        let dst = &self.buf[idx];
                        self.buf[idx] = Rgba {
                            r: ((color.r as u32 * alpha + dst.r as u32 * ia) / 255) as u16,
                            g: ((color.g as u32 * alpha + dst.g as u32 * ia) / 255) as u16,
                            b: ((color.b as u32 * alpha + dst.b as u32 * ia) / 255) as u16,
                            a: ((alpha + (dst.a as u32 * ia) / 255).min(255) * 0x0101) as u16,
                        };
                    }
                }
            }
        }
    }

    fn to_rgba8(&self) -> Vec<u8> {
        let mut out = vec![0u8; self.w * self.h * 4];
        for (i, pixel) in self.buf.iter().enumerate() {
            out[i * 4] = (pixel.r >> 8) as u8;
            out[i * 4 + 1] = (pixel.g >> 8) as u8;
            out[i * 4 + 2] = (pixel.b >> 8) as u8;
            out[i * 4 + 3] = (pixel.a >> 8) as u8;
        }
        out
    }
}

fn parse_color(s: &str) -> Option<Rgba> {
    let s = s.trim();
    if s.starts_with('#') {
        let hex = &s[1..];
        let (r, g, b, a) = match hex.len() {
            3 => {
                let r = u8::from_str_radix(&hex[0..1], 16).ok()? * 17;
                let g = u8::from_str_radix(&hex[1..2], 16).ok()? * 17;
                let b = u8::from_str_radix(&hex[2..3], 16).ok()? * 17;
                (r, g, b, 255)
            }
            4 => {
                let r = u8::from_str_radix(&hex[0..1], 16).ok()? * 17;
                let g = u8::from_str_radix(&hex[1..2], 16).ok()? * 17;
                let b = u8::from_str_radix(&hex[2..3], 16).ok()? * 17;
                let a = u8::from_str_radix(&hex[3..4], 16).ok()? * 17;
                (r, g, b, a)
            }
            6 => {
                let r = u8::from_str_radix(&hex[0..2], 16).ok()?;
                let g = u8::from_str_radix(&hex[2..4], 16).ok()?;
                let b = u8::from_str_radix(&hex[4..6], 16).ok()?;
                (r, g, b, 255)
            }
            8 => {
                let r = u8::from_str_radix(&hex[0..2], 16).ok()?;
                let g = u8::from_str_radix(&hex[2..4], 16).ok()?;
                let b = u8::from_str_radix(&hex[4..6], 16).ok()?;
                let a = u8::from_str_radix(&hex[6..8], 16).ok()?;
                (r, g, b, a)
            }
            _ => return None,
        };
        return Some(Rgba { r: (r as u16) * 257u16, g: (g as u16) * 257u16, b: (b as u16) * 257u16, a: (a as u16) * 257u16 })
    } else if let Some(s) = s.strip_prefix("0x").or_else(|| s.strip_prefix("0X")) {
        if let Ok(val) = u32::from_str_radix(s, 16) {
            let a = (val >> 24) as u8;
            let r = (val >> 16) as u8;
            let g = (val >> 8) as u8;
            let b = val as u8;
            return Some(Rgba { r: (r as u16) * 257u16, g: (g as u16) * 257u16, b: (b as u16) * 257u16, a: (a as u16).wrapping_mul(257u16) });
        }
    }
    named_color(s)
}

fn named_color(s: &str) -> Option<Rgba> {
    match s.to_lowercase().as_str() {
        "black" => Some(Rgba { r: 0, g: 0, b: 0, a: 65535 }),
        "white" => Some(Rgba { r: 65535, g: 65535, b: 65535, a: 65535 }),
        "red" => Some(Rgba { r: 65535, g: 0, b: 0, a: 65535 }),
        "green" => Some(Rgba { r: 0, g: 65535, b: 0, a: 65535 }),
        "blue" => Some(Rgba { r: 0, g: 0, b: 65535, a: 65535 }),
        "transparent" => Some(Rgba { r: 0, g: 0, b: 0, a: 0 }),
        _ => None,
    }
}

// ── PNG encoder ──────────────────────────────────────────────

pub(crate) fn encode_png(rgba: &[u8], w: usize, h: usize) -> Result<Vec<u8>> {
    let mut out: Vec<u8> = Vec::new();
    out.extend_from_slice(b"\x89PNG\r\n\x1a\n");
    write_chunk(&mut out, b"IHDR", &{
        let mut hdr = Vec::new();
        hdr.extend_from_slice(&(w as u32).to_be_bytes());
        hdr.extend_from_slice(&(h as u32).to_be_bytes());
        hdr.extend_from_slice(&[8, 6, 0, 0, 0]);
        hdr
    });
    let raw_size = (1 + w * 4) * h;
    let mut raw = vec![0u8; raw_size];
    for y in 0..h {
        raw[y * (1 + w * 4)] = 0;
        let src = &rgba[y * w * 4..(y + 1) * w * 4];
        let dst = &mut raw[y * (1 + w * 4) + 1..(y + 1) * (1 + w * 4)];
        dst.copy_from_slice(src);
    }
    let mut encoder = ZlibEncoder::new(Vec::new(), Compression::default());
    encoder.write_all(&raw).map_err(|e| AaptError::Io(e))?;
    let compressed = encoder.finish().map_err(|e| AaptError::Io(e))?;
    write_chunk(&mut out, b"IDAT", &compressed);
    write_chunk(&mut out, b"IEND", &[]);
    Ok(out)
}

fn write_chunk(out: &mut Vec<u8>, chunk_type: &[u8; 4], data: &[u8]) {
    let len = data.len() as u32;
    out.extend_from_slice(&len.to_be_bytes());
    out.extend_from_slice(chunk_type);
    out.extend_from_slice(data);
    let crc = crc32(chunk_type, data);
    out.extend_from_slice(&crc.to_be_bytes());
}

fn crc32(typ: &[u8; 4], data: &[u8]) -> u32 {
    let mut c = 0xFFFFFFFFu32;
    for &b in typ.iter().chain(data.iter()) {
        c = CRC_TABLE[(c as u8 ^ b) as usize] ^ (c >> 8);
    }
    c ^ 0xFFFFFFFF
}

const CRC_TABLE: [u32; 256] = {
    let mut table = [0u32; 256];
    let mut i = 0;
    while i < 256 {
        let mut c = i as u32;
        let mut j = 0;
        while j < 8 {
            if c & 1 != 0 {
                c = 0xEDB88320 ^ (c >> 1);
            } else {
                c >>= 1;
            }
            j += 1;
        }
        table[i] = c;
        i += 1;
    }
    table
};

// ── Vector drawable XML parser ───────────────────────────────

struct VectorDrawable {
    viewport_w: f64,
    viewport_h: f64,
    width: f64,
    height: f64,
    paths: Vec<PathDef>,
}

struct PathDef {
    segments: Vec<Segment>,
    fill: Option<Rgba>,
    stroke: Option<Rgba>,
    stroke_width: f64,
}

fn parse_axml_root_with_resolver(
    root: &Element,
    resolver: &mut dyn FnMut(u32) -> Option<String>,
    drawable_loader: &mut Option<&mut dyn FnMut(u32) -> Option<Vec<u8>>>,
    inline_bag_loader: &mut Option<&mut dyn FnMut(u32, &mut VectorDrawable)>,
) -> Result<VectorDrawable> {
    let mut vd = VectorDrawable {
        viewport_w: 100.0,
        viewport_h: 100.0,
        width: 48.0,
        height: 48.0,
        paths: Vec::new(),
    };

    let root_name = root.name.to_lowercase();
    if root_name == "vector" {
        parse_vector_attrs(root, &mut vd);
        parse_children_with_resolver(root, &mut vd, resolver)?;
    } else if root_name == "adaptive-icon" {
        vd.viewport_w = 108.0;
        vd.viewport_h = 108.0;
        vd.width = 108.0;
        vd.height = 108.0;
        for child in &root.children {
            let cname = child.name.to_lowercase();
            if cname == "background" || cname == "foreground" {
                let mut child_rendered = false;
                for grandchild in &child.children {
                    let gcname = grandchild.name.to_lowercase();
                    if gcname == "vector" || gcname == "group" || gcname == "path" {
                        parse_axml_node(grandchild, &mut vd, resolver)?;
                        child_rendered = true;
                    }
                }
                if !child_rendered {
                    if let Some(drawable_attr) = child.attr("drawable")
                        .or_else(|| child.attr("android:drawable"))
                    {
                        if matches!(drawable_attr.value, Value::Resource(_)) || matches!(drawable_attr.value, Value::ThemeResource(_)) {
                            let rid = match &drawable_attr.value {
                                Value::Resource(r) => *r,
                                Value::ThemeResource(r) => *r,
                                _ => unreachable!(),
                            };
                            dbglog!("adaptive-icon drawable rid=0x{:08x}", rid);
                            if let Some(color_str) = resolver(rid) {
                                dbglog!("resolver returned '{}'", color_str);
                                if let Some(color) = parse_color(&color_str) {
                                    let inset = 0.001;
                                    let rect = format!(
                                        "M{il},{il} L{w},{il} L{w},{ih} L{il},{ih} Z",
                                        il = inset, w = vd.viewport_w - inset, ih = vd.viewport_h - inset
                                    );
                                    if let Ok(segs) = parse_svg_path(&rect) {
                                        vd.paths.push(PathDef {
                                            segments: segs,
                                            fill: Some(color),
                                            stroke: None,
                                            stroke_width: 0.0,
                                        });
                                    }
                                    child_rendered = true;
                                }
                            }
                            if !child_rendered {
                                if let Some(ref mut loader) = drawable_loader {
                                    dbglog!("calling drawable_loader with 0x{:08x}", rid);
                                    if let Some(xml_bytes) = loader(rid) {
                                        dbglog!("drawable_loader returned {} bytes", xml_bytes.len());
                                        if let Ok(sub_manifest) = parse_manifest_flexible(&xml_bytes) {
                                            dbglog!("parsed sub-manifest root: {}", sub_manifest.raw.name);
                                            if let Ok(sub_vd) = parse_axml_root_with_resolver(
                                                &sub_manifest.raw,
                                                resolver,
                                                drawable_loader,
                                                inline_bag_loader,
                                            ) {
                                                vd.paths.extend(sub_vd.paths);
                                                child_rendered = true;
                                            }
                                        }
                                    }
                                }
                            }
                            if !child_rendered {
                                if let Some(ref mut bag_loader) = inline_bag_loader {
                                    bag_loader(rid, &mut vd);
                                    child_rendered = true;
                                }
                            }
                        }
                    }
                }
            }
        }
    } else {
        return Err(AaptError::Parse(format!("unknown root: {}", root_name)));
    }

    Ok(vd)
}

fn parse_axml_node(
    elem: &Element,
    vd: &mut VectorDrawable,
    resolver: &mut dyn FnMut(u32) -> Option<String>,
) -> Result<()> {
    let name = elem.name.to_lowercase();
    if name == "vector" {
        parse_vector_attrs(elem, vd);
        parse_children_with_resolver(elem, vd, resolver)?;
    } else if name == "group" {
        parse_children_with_resolver(elem, vd, resolver)?;
    } else if name == "path" {
        if let Some(path) = parse_path_elem_with_resolver(elem, resolver)? {
            vd.paths.push(path);
        }
    }
    Ok(())
}

fn parse_vector_attrs(elem: &Element, vd: &mut VectorDrawable) {
    for attr in &elem.attributes {
        let aname = resolve_attr_name(&attr.name);
        match aname.as_str() {
            "viewportwidth" => vd.viewport_w = attr_val_float(attr),
            "viewportheight" => vd.viewport_h = attr_val_float(attr),
            "width" => vd.width = dp_to_px(&attr.value),
            "height" => vd.height = dp_to_px(&attr.value),
            _ => {}
        }
    }
}

fn resolve_attr_name(name: &str) -> String {
    name.trim_start_matches("android:").to_lowercase()
}

fn attr_val_float(attr: &Attribute) -> f64 {
    match &attr.value {
        Value::Str(s) => s.parse().unwrap_or(0.0),
        Value::Int(i) => *i as f64,
        _ => 0.0,
    }
}

fn dp_to_px(v: &Value) -> f64 {
    match v {
        Value::Str(s) => {
            let s = s.trim();
            let num: f64 = s.trim_end_matches("dp").trim_end_matches("dip").trim_end_matches("px").trim().parse().unwrap_or(48.0);
            num
        }
        Value::Int(i) => *i as f64,
        _ => 48.0,
    }
}

fn parse_children_with_resolver(
    elem: &Element,
    vd: &mut VectorDrawable,
    resolver: &mut dyn FnMut(u32) -> Option<String>,
) -> Result<()> {
    for child in &elem.children {
        let cname = resolve_attr_name(&child.name);
        if cname == "path" {
            if let Some(path) = parse_path_elem_with_resolver(child, resolver)? {
                vd.paths.push(path);
            }
        } else if cname == "group" {
            parse_children_with_resolver(child, vd, resolver)?;
        }
    }
    Ok(())
}

fn parse_path_elem_with_resolver(
    elem: &Element,
    resolver: &mut dyn FnMut(u32) -> Option<String>,
) -> Result<Option<PathDef>> {
    let mut path_data = String::new();
    let mut fill_color = String::new();
    let mut stroke_color = String::new();
    let mut stroke_width = 0.0;
    let mut fill_res_id = None;
    let mut stroke_res_id = None;

    for attr in &elem.attributes {
        let aname = resolve_attr_name(&attr.name);
        match aname.as_str() {
            "pathdata" => path_data = attr_str(&attr.value),
            "fillcolor" => {
                fill_color = attr_str(&attr.value);
                if let Value::Resource(r) | Value::ThemeResource(r) = &attr.value {
                    fill_res_id = Some(*r);
                }
            }
            "strokecolor" => {
                stroke_color = attr_str(&attr.value);
                if let Value::Resource(r) | Value::ThemeResource(r) = &attr.value {
                    stroke_res_id = Some(*r);
                }
            }
            "strokewidth" => stroke_width = attr_val_float(attr),
            _ => {}
        }
    }

    if path_data.is_empty() {
        return Ok(None);
    }

    let segments = parse_svg_path(&path_data)?;

    let fill = resolve_color(&fill_color, fill_res_id, resolver);
    let stroke = resolve_color(&stroke_color, stroke_res_id, resolver);

    Ok(Some(PathDef { segments, fill, stroke, stroke_width }))
}

fn resolve_color(
    raw: &str,
    res_id: Option<u32>,
    resolver: &mut dyn FnMut(u32) -> Option<String>,
) -> Option<Rgba> {
    if raw == "none" || raw == "@android:color/transparent" {
        return None;
    }
    if let Some(id) = res_id {
        if let Some(resolved) = resolver(id) {
            if let Some(color) = parse_color(&resolved) {
                return Some(color);
            }
        }
    }
    if raw.is_empty() {
        // Android defaults to black when fillColor is absent
        return Some(Rgba { r: 0, g: 0, b: 0, a: 65535 });
    }
    parse_color(raw)
}

fn attr_str(v: &Value) -> String {
    match v {
        Value::Str(s) => s.clone(),
        Value::Resource(r) | Value::ThemeResource(r) => format!("@0x{:08x}", r),
        _ => "?".to_string(),
    }
}

// ── Main entry point ─────────────────────────────────────────

pub fn render_vector_icon(axml_bytes: &[u8], target_size: Option<u32>) -> Result<Vec<u8>> {
    let mut none_loader: Option<&mut dyn FnMut(u32) -> Option<Vec<u8>>> = None;
    render_vector_icon_with_resolver(axml_bytes, target_size, &mut |_| None, &mut none_loader, &mut None)
}

pub fn render_vector_icon_from_apk<R: std::io::Read + std::io::Seek>(
    axml_bytes: &[u8],
    entries: &[String],
    za: &mut crate::archive::ZipArchive<R>,
    target_size: Option<u32>,
) -> Result<Vec<u8>> {
    let arsc = if entries.iter().any(|e| e == "resources.arsc") {
        if let Ok(buf) = za.read_entry("resources.arsc") {
            crate::resources::parse_resources(&buf).ok()
        } else {
            None
        }
    } else {
        None
    };

    // Read theme from AndroidManifest.xml
    let theme_id = if entries.iter().any(|e| e == "AndroidManifest.xml") {
        if let Ok(manifest_buf) = za.read_entry("AndroidManifest.xml") {
            if let Ok(manifest) = crate::manifest::parse_manifest_flexible(&manifest_buf) {
                manifest.raw.attr_value("theme")
                    .or_else(|| {
                        manifest.raw.find("application")
                            .and_then(|a| a.attr_value("theme"))
                    })
                    .and_then(|v| v.as_resource())
            } else {
                None
            }
        } else {
            None
        }
    } else {
        None
    };

    let arsc_ref = &arsc;
    let theme_ref = &theme_id;
    let arsc_ref2 = &arsc;
    let theme_ref2 = &theme_id;
    let mut resolver = |res_id: u32| -> Option<String> {
        let table = arsc_ref2.as_ref()?;
        let (val, _key) = crate::resources::resolve_resource_value(table, res_id)?;
        match val {
            crate::resources::ResValue::String(s) => Some(s),
            crate::resources::ResValue::Int(c) => {
                // Android Res_value stores colors as 0xAARRGGBB in the u32.
                // parse_color expects #RRGGBBAA for 8-digit hex, so reorder.
                let r = ((c >> 16) & 0xFF) as u8;
                let g = ((c >> 8) & 0xFF) as u8;
                let b = (c & 0xFF) as u8;
                let a = ((c >> 24) & 0xFF) as u8;
                Some(format!("#{:02x}{:02x}{:02x}{:02x}", r, g, b, a))
            }
            crate::resources::ResValue::Attribute(attr_id) => {
                if let Some(theme) = theme_ref2 {
                    if let Some(attr_val) = crate::resources::resolve_theme_attr_value(table, *theme, attr_id) {
                        match attr_val {
                            crate::resources::ResValue::String(s) => Some(s),
                            crate::resources::ResValue::Int(c) => {
                                let r = ((c >> 16) & 0xFF) as u8;
                                let g = ((c >> 8) & 0xFF) as u8;
                                let b = (c & 0xFF) as u8;
                                let a = ((c >> 24) & 0xFF) as u8;
                                Some(format!("#{:02x}{:02x}{:02x}{:02x}", r, g, b, a))
                            }
                            crate::resources::ResValue::Reference(r) => {
                                if let Some((v, _)) = crate::resources::resolve_resource_value(table, r) {
                                    match v {
                                        crate::resources::ResValue::String(s) => Some(s),
                                        crate::resources::ResValue::Int(c) => {
                                            let r = ((c >> 16) & 0xFF) as u8;
                                            let g = ((c >> 8) & 0xFF) as u8;
                                            let b = (c & 0xFF) as u8;
                                            let a = ((c >> 24) & 0xFF) as u8;
                                            Some(format!("#{:02x}{:02x}{:02x}{:02x}", r, g, b, a))
                                        }
                                        _ => None,
                                    }
                                } else {
                                    None
                                }
                            }
                            _ => None,
                        }
                    } else {
                        None
                    }
                } else {
                    None
                }
            }
            _ => None,
        }
    };

    // Build a drawable loader that resolves resource IDs to XML bytes from the archive
    // This handles adaptive-icon android:drawable references.
    // The drawable entry's VALUE (not key) contains the actual file path, e.g. String("res/abc.xml").
    let drawable_loader_entries = entries.clone();
    let mut drawable_loader = |res_id: u32| -> Option<Vec<u8>> {
        let table = arsc_ref.as_ref()?;
        // Get the resource value (follows reference chains to the final value)
        let resolved = crate::resources::resolve_resource_value(table, res_id);
        if resolved.is_none() {
            dbglog!("drawable_loader: resolve_resource_value for 0x{:08x} returned None", res_id);
            return None;
        }
        let (val, _key) = resolved.unwrap();
        dbglog!("drawable_loader: resolved 0x{:08x} -> {:?}", res_id, val);
        // The value should be a String containing the actual file path in the archive
        if let crate::resources::ResValue::String(path) = &val {
            dbglog!("drawable_loader: trying to read '{}' from archive", path);
            if let Ok(bytes) = za.read_entry(&path) {
                dbglog!("drawable_loader: read {} bytes, magic={:02x}{:02x}", bytes.len(), bytes[0], bytes[1]);
                if bytes.len() >= 8 && bytes[0] == 0x03 && bytes[1] == 0x00 {
                    return Some(bytes);
                }
            } else {
                dbglog!("drawable_loader: failed to read '{}' from archive", path);
            }
        }
        // Fallback: try resolve_resource_key to search by symbolic name
        let key = crate::resources::resolve_resource_key(table, res_id);
        let key = match key {
            Some(k) => k,
            None => {
                dbglog!("drawable_loader: resolve_resource_key for 0x{:08x} returned None", res_id);
                return None;
            }
        };
        let key_lc = key.to_lowercase();
        for entry in drawable_loader_entries.iter() {
            let el = entry.to_lowercase();
            if !el.ends_with(".xml") {
                continue;
            }
            let file_stem = std::path::Path::new(entry)
                .file_stem()
                .map(|s| s.to_string_lossy().to_lowercase())
                .unwrap_or_default();
            if file_stem == key_lc {
                if let Ok(bytes) = za.read_entry(entry) {
                    if bytes.len() >= 8 && bytes[0] == 0x03 && bytes[1] == 0x00 {
                        return Some(bytes);
                    }
                }
            }
        }
        None
    };

    // Build an inline bag loader that resolves resource IDs to vector drawable paths
    // from resources.arsc complex entries (inline bags, no separate XML files)
    let mut inline_bag_loader = |res_id: u32, vd: &mut VectorDrawable| {
        let table = match arsc_ref.as_ref() {
            Some(t) => t,
            None => return,
        };
        let map_entries = match crate::resources::resolve_resource_map_entries(table, res_id) {
            Some(e) => e,
            None => return,
        };
        let mut path_data = String::new();
        let mut fill_color = String::new();
        let mut stroke_color = String::new();
        let mut stroke_width = 0.0f64;

        for (name_id, val) in map_entries {
            let name = crate::resources::resolve_resource_key(table, *name_id)
                .unwrap_or_default()
                .to_lowercase();
            match name.as_str() {
                "pathdata" => {
                    if let crate::resources::ResValue::String(s) = val {
                        path_data = s.clone();
                    }
                }
                "fillcolor" => {
                    fill_color = resolve_color_from_value(table, val, theme_ref);
                }
                "strokecolor" => {
                    stroke_color = resolve_color_from_value(table, val, theme_ref);
                }
                "strokewidth" => {
                    if let crate::resources::ResValue::Int(c) = val {
                        stroke_width = *c as f64;
                    }
                }
                _ => {}
            }
        }

        if !path_data.is_empty() {
            if let Ok(segments) = parse_svg_path(&path_data) {
                let fill = parse_color(&fill_color);
                let stroke = parse_color(&stroke_color);
                vd.paths.push(PathDef {
                    segments,
                    fill,
                    stroke,
                    stroke_width,
                });
            }
        }
    };

    render_vector_icon_with_resolver(axml_bytes, target_size, &mut resolver, &mut Some(&mut drawable_loader), &mut Some(&mut inline_bag_loader))
}

/// Resolve a color from a ResValue, following references and theme attributes.
fn resolve_color_from_value(
    table: &crate::resources::ResourceTable,
    val: &crate::resources::ResValue,
    theme_id: &Option<u32>,
) -> String {
    match val {
        crate::resources::ResValue::String(s) => s.clone(),
        crate::resources::ResValue::Int(c) => format!("#{:08x}", c),
        crate::resources::ResValue::Reference(r) => {
            if let Some((v, _)) = crate::resources::resolve_resource_value(table, *r) {
                match v {
                    crate::resources::ResValue::String(s) => s,
                    crate::resources::ResValue::Int(c) => format!("#{:08x}", c),
                    _ => String::new(),
                }
            } else {
                String::new()
            }
        }
        crate::resources::ResValue::Attribute(a) => {
            if let Some(theme) = theme_id {
                if let Some(attr_val) = crate::resources::resolve_theme_attr_value(table, *theme, *a) {
                    resolve_color_from_value(table, &attr_val, theme_id)
                } else {
                    String::new()
                }
            } else {
                String::new()
            }
        }
        _ => String::new(),
    }
}

fn render_vector_icon_with_resolver(
    axml_bytes: &[u8],
    target_size: Option<u32>,
    resolver: &mut dyn FnMut(u32) -> Option<String>,
    drawable_loader: &mut Option<&mut dyn FnMut(u32) -> Option<Vec<u8>>>,
    inline_bag_loader: &mut Option<&mut dyn FnMut(u32, &mut VectorDrawable)>,
) -> Result<Vec<u8>> {
    let manifest = parse_manifest_flexible(axml_bytes)?;
    let root = &manifest.raw;

    let vd = parse_axml_root_with_resolver(root, resolver, drawable_loader, inline_bag_loader)?;

    let render_size = target_size.unwrap_or_else(|| vd.width.max(vd.height) as u32).max(16).min(1024) as usize;

    let mut canvas = Canvas::new(render_size, render_size);

    for path in &vd.paths {
        let pts = flatten(&path.segments, 0.5);
        if let Some(ref fill) = path.fill {
            canvas.fill_path(&pts, fill.clone(), vd.viewport_w, vd.viewport_h);
        }
        if let Some(ref stroke) = path.stroke {
            if path.stroke_width > 0.0 {
                let stroked = stroke_path(&pts, path.stroke_width);
                canvas.fill_path(&stroked, stroke.clone(), vd.viewport_w, vd.viewport_h);
            }
        }
    }

        let rgba = canvas.to_rgba8();
        if rgba.chunks_exact(4).all(|p| p[3] == 0) {
            dbglog!("vector rendering produced all-transparent image ({}x{})", render_size, render_size);
            return Err(AaptError::NotFound("vector rendering produced all-transparent image".into()));
        }
        encode_png(&rgba, render_size, render_size)
}

// ── Stroke (simplified outline via Minkowski-ish expansion) ──

fn stroke_path(pts: &[(f64, f64)], width: f64) -> Vec<(f64, f64)> {
    if pts.len() < 2 || width <= 0.0 {
        return Vec::new();
    }
    let hw = width * 0.5;
    let mut result = Vec::new();

    for i in 0..(pts.len() - 1) {
        let (x1, y1) = pts[i];
        let (x2, y2) = pts[i + 1];
        let dx = x2 - x1;
        let dy = y2 - y1;
        let len = (dx * dx + dy * dy).sqrt();
        if len < 1e-9 {
            continue;
        }
        let nx = -dy / len * hw;
        let ny = dx / len * hw;

        result.push((x1 + nx, y1 + ny));
        result.push((x2 + nx, y2 + ny));
        result.push((x2 - nx, y2 - ny));
        result.push((x1 - nx, y1 - ny));
        // Close this segment
        result.push((x1 + nx, y1 + ny));
    }

    result
}

// ── XML → SVG export ─────────────────────────────────────────

/// Convert a parsed VectorDrawable to SVG string.
fn segments_to_svg_path_data(segs: &[Segment]) -> String {
    let mut s = String::new();
    for seg in segs {
        match seg {
            Segment::MoveTo(x, y) => s.push_str(&format!("M{} {} ", x, y)),
            Segment::LineTo(x, y) => s.push_str(&format!("L{} {} ", x, y)),
            Segment::CubicTo(x1, y1, x2, y2, x3, y3) => s.push_str(&format!("C{} {} {} {} {} {} ", x1, y1, x2, y2, x3, y3)),
            Segment::QuadTo(x1, y1, x2, y2) => s.push_str(&format!("Q{} {} {} {} ", x1, y1, x2, y2)),
            Segment::ArcTo(rx, ry, rot, laf, sf, x, y) => s.push_str(&format!("A{} {} {} {} {} {} {} ", rx, ry, rot, *laf as u8, *sf as u8, x, y)),
            Segment::Close => s.push_str("Z "),
        }
    }
    s
}

fn rgba_to_svg_color(c: &Rgba) -> String {
    let r = (c.r >> 8) as u8;
    let g = (c.g >> 8) as u8;
    let b = (c.b >> 8) as u8;
    let a = (c.a as f64) / 65535.0;
    if (a - 1.0).abs() < 0.01 {
        format!("#{:02x}{:02x}{:02x}", r, g, b)
    } else {
        format!("rgba({},{},{},{})", r, g, b, format!("{:.2}", a).trim_end_matches('0').trim_end_matches('.'))
    }
}

pub fn vector_to_svg(vd: &VectorDrawable) -> String {
    let mut svg = format!(
        r#"<svg xmlns="http://www.w3.org/2000/svg" width="{}" height="{}" viewBox="0 0 {} {}">"#,
        vd.width, vd.height, vd.viewport_w, vd.viewport_h
    );
    for path in &vd.paths {
        let d = segments_to_svg_path_data(&path.segments);
        let fill = path.fill.as_ref().map(|c| rgba_to_svg_color(c)).unwrap_or_else(|| "none".into());
        let stroke = path.stroke.as_ref().map(|c| rgba_to_svg_color(c)).unwrap_or_else(|| "none".into());
        let sw = if path.stroke_width > 0.0 { format!(" stroke-width=\"{}\"", path.stroke_width) } else { String::new() };
        svg.push_str(&format!(r#"<path d="{}" fill="{}" stroke="{}"{} />"#, d, fill, stroke, sw));
    }
    svg.push_str("</svg>");
    svg
}

/// Convert Android binary XML vector drawable bytes to SVG string.
pub fn xml_to_svg(axml_bytes: &[u8]) -> Result<String> {
    let mut none_loader: Option<&mut dyn FnMut(u32) -> Option<Vec<u8>>> = None;
    let manifest = parse_manifest_flexible(axml_bytes)?;
    let root = &manifest.raw;
    let vd = parse_axml_root_with_resolver(root, &mut |_| None, &mut none_loader, &mut None)?;
    Ok(vector_to_svg(&vd))
}

// ── SVG import (parse SVG → rasterize) ───────────────────────

/// Minimal SVG parser: extract viewport and path data from SVG string.
struct SvgDoc {
    viewport_w: f64,
    viewport_h: f64,
    paths: Vec<(String, Option<Rgba>, Option<Rgba>, f64)>, // (d, fill, stroke, stroke_width)
}

fn parse_svg_attr_val(s: &str, attr: &str) -> Option<String> {
    let needle = format!("{}=\"", attr);
    let start = s.find(&needle)? + needle.len();
    let end = s[start..].find('"')?;
    Some(s[start..start + end].to_string())
}

fn parse_svg_num(s: &str, attr: &str) -> Option<f64> {
    parse_svg_attr_val(s, attr)?.parse().ok()
}

fn parse_svg_color(s: &str) -> Option<Rgba> {
    if s == "none" || s.is_empty() { return None; }
    parse_color(s)
}

fn parse_svg_file(svg_data: &str) -> Result<SvgDoc> {
    let mut doc = SvgDoc {
        viewport_w: 24.0,
        viewport_h: 24.0,
        paths: Vec::new(),
    };

    // Extract viewport from <svg> tag
    if let Some(svg_tag_end) = svg_data.find('>') {
        let svg_tag = &svg_data[..svg_tag_end];
        if let Some(w) = parse_svg_num(svg_tag, "width") { doc.viewport_w = w; }
        if let Some(h) = parse_svg_num(svg_tag, "height") { doc.viewport_h = h; }
        if let Some(viewBox) = parse_svg_attr_val(svg_tag, "viewBox") {
            let nums: Vec<f64> = viewBox.split_whitespace().filter_map(|s| s.parse().ok()).collect();
            if nums.len() >= 4 {
                doc.viewport_w = nums[2];
                doc.viewport_h = nums[3];
            }
        }
    }

    // Extract <path> elements
    let mut pos = 0;
    while let Some(start) = svg_data[pos..].find("<path") {
        let abs_start = pos + start;
        if let Some(tag_end) = svg_data[abs_start..].find('>') {
            let tag = &svg_data[abs_start..abs_start + tag_end + 1];
            let d = parse_svg_attr_val(tag, "d").unwrap_or_default();
            let fill = parse_svg_attr_val(tag, "fill").and_then(|s| parse_svg_color(&s));
            let stroke = parse_svg_attr_val(tag, "stroke").and_then(|s| parse_svg_color(&s));
            let sw = parse_svg_num(tag, "stroke-width").unwrap_or(0.0);
            doc.paths.push((d, fill, stroke, sw));
            pos = abs_start + tag_end + 1;
        } else {
            break;
        }
    }

    Ok(doc)
}

/// Parse SVG bytes and rasterize to RGBA pixels.
pub fn svg_to_rgba(svg_data: &[u8], target_size: u32) -> Result<(Vec<u8>, usize, usize)> {
    let svg_str = std::str::from_utf8(svg_data)
        .map_err(|_| AaptError::Parse("invalid UTF-8 in SVG".into()))?;
    let doc = parse_svg_file(svg_str)?;

    let render_size = target_size as usize;
    let mut canvas = Canvas::new(render_size, render_size);

    for (d, fill, stroke, sw) in &doc.paths {
        if d.is_empty() { continue; }
        let segs = parse_svg_path(d)?;
        let pts = flatten(&segs, 0.5);
        if let Some(ref fill_color) = fill {
            canvas.fill_path(&pts, fill_color.clone(), doc.viewport_w, doc.viewport_h);
        }
        if let Some(ref stroke_color) = stroke {
            if *sw > 0.0 {
                let stroked = stroke_path(&pts, *sw);
                canvas.fill_path(&stroked, stroke_color.clone(), doc.viewport_w, doc.viewport_h);
            }
        }
    }

    let rgba = canvas.to_rgba8();
    Ok((rgba, render_size, render_size))
}

// Re-exports for use in icon.rs
use crate::manifest::{Attribute, Element};
