use std::ptr;

type PCWSTR = *const u16;
type HKEY = *mut core::ffi::c_void;
type HANDLE = *mut core::ffi::c_void;
type HWND = *mut core::ffi::c_void;
type BOOL = i32;
type SOCKET = usize;

const HKEY_LOCAL_MACHINE: HKEY = -2147483646_isize as *mut core::ffi::c_void;
const KEY_READ: u32 = 0x20019;
const KEY_WRITE: u32 = 0x20006;
const REG_SZ: u32 = 1;
const INVALID_SOCKET: SOCKET = !0usize;
const AF_INET: i32 = 2;
const SOCK_STREAM: i32 = 1;
const IPPROTO_TCP: i32 = 6;

const PROVIDER_NAME: &str = "WSANetProvider";
const DEFAULT_WEBDAV_PORT: u16 = 8088;

extern "system" {
    fn RegOpenKeyExW(hkey: HKEY, sub: PCWSTR, r: u32, s: u32, out: *mut HKEY) -> i32;
    fn RegSetValueExW(hkey: HKEY, name: PCWSTR, r: u32, t: u32, data: *const u8, len: u32) -> i32;
    fn RegQueryValueExW(hkey: HKEY, name: PCWSTR, r: *mut u32, t: *mut u32, data: *mut u8, len: *mut u32) -> i32;
    fn RegCreateKeyExW(hkey: HKEY, sub: PCWSTR, r: *mut u16, c: *mut u16, o: u32, s: u32, sa: *mut u8, out: *mut HKEY, disp: *mut u32) -> i32;
    fn RegCloseKey(hkey: HKEY) -> i32;
    fn GetModuleFileNameW(h: HANDLE, buf: *mut u16, size: u32) -> u32;
    fn CreateProcessW(app: PCWSTR, cmd: PCWSTR, pa: *mut u8, ta: *mut u8, inh: i32, flags: u32, env: *mut u8, dir: PCWSTR, si: *mut u8, pi: *mut u8) -> i32;
    fn CloseHandle(h: HANDLE) -> i32;
    fn Sleep(ms: u32);

    fn WSAStartup(w: u16, d: *mut u8) -> i32;
    fn WSACleanup() -> i32;
    fn socket(af: i32, st: i32, pr: i32) -> SOCKET;
    fn connect(s: SOCKET, name: *const u8, len: i32) -> i32;
    fn closesocket(s: SOCKET) -> i32;
}

#[repr(C)]
struct WSAData {
    w_version: u16,
    w_high_version: u16,
    i_max_sockets: u8,
    i_max_udg_dg: u8,
    lp_vendor_info: *mut u8,
    sz_description: [u8; 257],
    sz_system_status: [u8; 129],
    sa: [u16; 8],
}

#[repr(C)]
struct SockAddrIn {
    sin_family: u16,
    sin_port: u16,
    sin_addr: u32,
    sin_zero: [u8; 8],
}

#[repr(C)]
struct STARTUPINFOW {
    cb: u32,
    _r1: *mut u8, _r2: *mut u16, _r3: *mut u16,
    _r4: u32, _r5: u32, _r6: u32, _r7: u32,
    _r8: u32, _r9: u32, _r10: u32, _r11: u32,
    _r12: u32, _r13: u32, _r14: *mut u16,
    h_std_input: HANDLE, h_std_output: HANDLE, h_std_error: HANDLE,
}

#[repr(C)]
struct PROCESS_INFORMATION {
    h_process: HANDLE,
    h_thread: HANDLE,
    dw_process_id: u32,
    dw_thread_id: u32,
}

unsafe fn to_wide(s: &str) -> Vec<u16> {
    s.encode_utf16().chain(std::iter::once(0)).collect()
}

unsafe fn read_pwstr(ptr: PCWSTR, max_len: usize) -> String {
    if ptr.is_null() { return String::new(); }
    let slice = std::slice::from_raw_parts(ptr, max_len);
    let len = slice.iter().position(|&c| c == 0).unwrap_or(max_len);
    String::from_utf16_lossy(&slice[..len])
}

fn wide_to_string(wide: &[u16]) -> String {
    let len = wide.iter().position(|&c| c == 0).unwrap_or(wide.len());
    String::from_utf16_lossy(&wide[..len])
}

fn is_wsa_unc(path: &str) -> bool {
    let lower = path.to_lowercase();
    lower.starts_with("\\\\wsa.localhost\\") || lower.starts_with("//wsa.localhost/")
}

fn translate_unc_to_webdav(unc_path: &str, port: u16) -> Option<String> {
    let lower = unc_path.to_lowercase();
    let relative = if let Some(pos) = lower.find("\\\\wsa.localhost\\") {
        &unc_path[pos + 17..]
    } else if let Some(pos) = lower.find("//wsa.localhost/") {
        &unc_path[pos + 16..]
    } else {
        return None;
    };
    let relative = if let Some(rest) = relative.strip_prefix("davwwwroot/") { rest }
        else if let Some(rest) = relative.strip_prefix("DavWWWRoot\\") { rest }
        else if let Some(rest) = relative.strip_prefix("davwwwroot\\") { rest }
        else { relative };
    let relative = relative.trim_end_matches('\\').trim_end_matches('/');
    let base = format!("http://127.0.0.1:{}", port);
    if relative.is_empty() {
        Some(format!("{}/", base))
    } else {
        Some(format!("{}/{}/", base, relative))
    }
}

// ── TCP check ──────────────────────────────────────────────────────────────

unsafe fn tcp_check(port: u16) -> bool {
    let mut wsa_data: WSAData = std::mem::zeroed();
    if WSAStartup(0x0202, &mut wsa_data as *mut _ as *mut u8) != 0 {
        return false;
    }
    let s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if s == INVALID_SOCKET {
        WSACleanup();
        return false;
    }
    let mut addr: SockAddrIn = std::mem::zeroed();
    addr.sin_family = AF_INET as u16;
    addr.sin_port = port.to_be();
    addr.sin_addr = 0x0100007F; // 127.0.0.1 little-endian
    let rc = connect(s, &addr as *const _ as *const u8, std::mem::size_of::<SockAddrIn>() as i32);
    closesocket(s);
    WSACleanup();
    rc == 0
}

// ── Path helpers ───────────────────────────────────────────────────────────

unsafe fn get_dll_dir() -> String {
    let mut buf = [0u16; 4096];
    let len = GetModuleFileNameW(ptr::null_mut(), buf.as_mut_ptr(), 4096);
    let path = wide_to_string(&buf[..len as usize]);
    std::path::Path::new(&path)
        .parent()
        .map(|p| p.to_string_lossy().to_string())
        .unwrap_or_default()
}

unsafe fn find_pythonw(dll_dir: &str) -> Option<String> {
    let base = std::path::Path::new(dll_dir).parent()?;
    // 1. Frozen: <base>/_internal/pythonw.exe
    let frozen = base.join("_internal").join("pythonw.exe");
    if frozen.exists() {
        return Some(frozen.to_string_lossy().to_string());
    }
    // 2. Dev: <base>/venv/Scripts/pythonw.exe
    let dev = base.join("venv").join("Scripts").join("pythonw.exe");
    if dev.exists() {
        return Some(dev.to_string_lossy().to_string());
    }
    // 3. Dev (assets beside project): <base>/../venv/Scripts/pythonw.exe
    let dev2 = base.join("..").join("venv").join("Scripts").join("pythonw.exe");
    if dev2.exists() {
        return Some(dev2.canonicalize().ok()?.to_string_lossy().to_string());
    }
    None
}

// ── Read webdav_port from wsa_init.cfg ─────────────────────────────────────

unsafe fn read_webdav_port(dll_dir: &str) -> u16 {
    let cfg_path = format!("{}\\wsa_init.cfg", dll_dir);
    let path_w = to_wide(&cfg_path);
    let h = create_file_w_simple(path_w.as_ptr());
    if h == ptr::null_mut() { return DEFAULT_WEBDAV_PORT; }
    let mut bytes_read = 0u32;
    let mut data = [0u8; 1024];
    read_file_simple(h, &mut data, &mut bytes_read);
    CloseHandle(h);
    let text = String::from_utf8_lossy(&data[..bytes_read as usize]);
    for line in text.lines() {
        if line.starts_with("webdav_port=") {
            if let Some(v) = line.splitn(2, '=').nth(1) {
                if let Ok(p) = v.trim().parse::<u16>() {
                    return p;
                }
            }
        }
    }
    DEFAULT_WEBDAV_PORT
}

unsafe fn create_file_w_simple(path: *const u16) -> HANDLE {
    extern "system" {
        fn CreateFileW(lp: PCWSTR, acc: u32, sh: u32, sa: *mut u8, cr: u32, fl: u32, tm: HANDLE) -> HANDLE;
    }
    CreateFileW(path, 0x00000001, 1, ptr::null_mut(), 3, 0x80, ptr::null_mut())
}

unsafe fn read_file_simple(h: HANDLE, buf: &mut [u8], bytes: &mut u32) {
    extern "system" {
        fn ReadFile(h: HANDLE, buf: *mut u8, to_read: u32, read: *mut u32, ov: *mut u8) -> i32;
    }
    ReadFile(h, buf.as_mut_ptr(), buf.len() as u32, bytes, ptr::null_mut());
}

// ── Spawn helper ───────────────────────────────────────────────────────────

unsafe fn spawn_init(pythonw: &str, assets_dir: &str) {
    let cmd = format!(
        "\"{}\" -c \"import sys;sys.path.insert(0,r'{}');import wsa_init;wsa_init.main()\"",
        pythonw, assets_dir
    );
    let cmd_w = to_wide(&cmd);
    let mut si: STARTUPINFOW = std::mem::zeroed();
    si.cb = std::mem::size_of::<STARTUPINFOW>() as u32;
    let mut pi: PROCESS_INFORMATION = std::mem::zeroed();
    CreateProcessW(
        ptr::null(),
        cmd_w.as_ptr(),
        ptr::null_mut(), ptr::null_mut(),
        0, 0x08000000, // CREATE_NO_WINDOW
        ptr::null_mut(), ptr::null_mut(),
        &mut si as *mut _ as *mut u8,
        &mut pi as *mut _ as *mut u8,
    );
    if !pi.h_process.is_null() { CloseHandle(pi.h_process); }
    if !pi.h_thread.is_null() { CloseHandle(pi.h_thread); }
}

// ── Ensure WebDAV alive ────────────────────────────────────────────────────

unsafe fn ensure_webdav_alive() -> bool {
    let dll_dir = get_dll_dir();
    let port = read_webdav_port(&dll_dir);

    if tcp_check(port) { return true; }

    let pythonw = match find_pythonw(&dll_dir) {
        Some(p) => p,
        None => return false,
    };

    spawn_init(&pythonw, &dll_dir);

    for _ in 0..60 {
        Sleep(1000);
        if tcp_check(port) { return true; }
    }
    false
}

// ── WNet exports ───────────────────────────────────────────────────────────

#[no_mangle]
pub unsafe extern "system" fn WNetGetUniversalNameW(
    lplocalpath: PCWSTR,
    _dwinfobufferlength: u32,
    lpbuffer: *mut u8,
    lpnneededlength: *mut u32,
) -> u32 {
    let path = read_pwstr(lplocalpath, 260);
    if !is_wsa_unc(&path) { return 1208; }

    ensure_webdav_alive();

    let dll_dir = get_dll_dir();
    let port = read_webdav_port(&dll_dir);

    match translate_unc_to_webdav(&path, port) {
        Some(url) => {
            let wide: Vec<u16> = url.encode_utf16().chain(std::iter::once(0)).collect();
            let needed = (wide.len() * 2) as u32;
            if !lpnneededlength.is_null() { *lpnneededlength = needed; }
            if lpbuffer.is_null() { return 122; }
            ptr::copy_nonoverlapping(wide.as_ptr(), lpbuffer as *mut u16, wide.len());
            0
        }
        None => 1208,
    }
}

#[no_mangle]
pub unsafe extern "system" fn WNetGetConnectionW(
    _lplocalname: PCWSTR, _lpremotoname: *mut u16, _lpnlength: *mut u32,
) -> u32 { 1208 }

#[no_mangle]
pub unsafe extern "system" fn WNetCancelConnection2W(
    _lpname: PCWSTR, _dwflags: u32, _fforce: BOOL,
) -> u32 { 0 }

#[no_mangle]
pub unsafe extern "system" fn WNetGetCapsW(_ndev: u32) -> u32 { 0 }

#[no_mangle]
pub unsafe extern "system" fn WNetGetProviderNameW(
    _nettype: u32, lpprovidername: *mut u16, lpbufferlength: *mut u32,
) -> u32 {
    let name_w: Vec<u16> = PROVIDER_NAME.encode_utf16().chain(std::iter::once(0)).collect();
    let needed = (name_w.len() * 2) as u32;
    if !lpbufferlength.is_null() {
        let have = *lpbufferlength;
        *lpbufferlength = needed;
        if have < needed { return 122; }
    }
    if !lpprovidername.is_null() {
        ptr::copy_nonoverlapping(name_w.as_ptr(), lpprovidername, name_w.len());
    }
    0
}

#[no_mangle]
pub unsafe extern "system" fn WNetOpenEnumW(
    _scope: u32, _type: u32, _usage: u32, _nr: *const u8, _handle: *mut HANDLE,
) -> u32 { 50 }

#[no_mangle]
pub unsafe extern "system" fn WNetEnumResourceW(
    _handle: HANDLE, _count: *mut u32, _buf: *mut u8, _size: *mut u32,
) -> u32 { 259 }

#[no_mangle]
pub unsafe extern "system" fn WNetCloseEnumW(_handle: HANDLE) -> u32 { 0 }

#[no_mangle]
pub unsafe extern "system" fn WNetAddConnection2W(
    _nr: *const u8, _pw: PCWSTR, _user: PCWSTR, _flags: u32,
) -> u32 { 0 }

#[no_mangle]
pub unsafe extern "system" fn WNetAddConnection3W(
    _hwnd: HWND, _nr: *const u8, _pw: PCWSTR, _user: PCWSTR, _flags: u32,
) -> u32 { 0 }

#[no_mangle]
pub unsafe extern "system" fn WNetConnectionDialog1W(_info: *mut u8) -> u32 { 1208 }

#[no_mangle]
pub unsafe extern "system" fn WNetDisconnectDialog1W(_info: *mut u8) -> u32 { 1208 }

#[no_mangle]
pub unsafe extern "system" fn WNetUseConnectionW(
    _hwnd: HWND, _nr: *const u8, _user: PCWSTR, _pw: PCWSTR, _flags: u32,
    lpuseinfo: *mut u8, lpusestr: *mut u32,
) -> u32 {
    if !lpuseinfo.is_null() {
        let pname: Vec<u16> = PROVIDER_NAME.encode_utf16().chain(std::iter::once(0)).collect();
        ptr::copy_nonoverlapping(pname.as_ptr(), lpuseinfo as *mut u16, pname.len().min(80));
    }
    if !lpusestr.is_null() { *lpusestr = 0; }
    0
}

// ── Provider registration ──────────────────────────────────────────────────

unsafe fn register_provider() {
    let order_key = to_wide("SYSTEM\\CurrentControlSet\\Control\\NetworkProvider\\Order");
    let provider_val = to_wide("Provider");
    let mut hkey: HKEY = ptr::null_mut();
    let mut current_order = String::new();

    if RegOpenKeyExW(HKEY_LOCAL_MACHINE, order_key.as_ptr(), 0, KEY_READ, &mut hkey) == 0 {
        let mut buf = [0u16; 1024];
        let mut buf_len = (buf.len() * 2) as u32;
        let mut reg_type = 0u32;
        if RegQueryValueExW(hkey, provider_val.as_ptr(), ptr::null_mut(), &mut reg_type, buf.as_mut_ptr() as *mut u8, &mut buf_len) == 0 {
            current_order = wide_to_string(&buf);
        }
        RegCloseKey(hkey);
    }

    if !current_order.to_lowercase().contains("wsanetprovider") {
        let new_order = if current_order.is_empty() {
            PROVIDER_NAME.to_string()
        } else {
            format!("{},{}", current_order, PROVIDER_NAME)
        };
        let new_order_w = to_wide(&new_order);
        if RegOpenKeyExW(HKEY_LOCAL_MACHINE, order_key.as_ptr(), 0, KEY_WRITE, &mut hkey) == 0 {
            RegSetValueExW(hkey, provider_val.as_ptr(), 0, REG_SZ, new_order_w.as_ptr() as *const u8, (new_order_w.len() * 2) as u32);
            RegCloseKey(hkey);
        }
    }

    let svc_key = to_wide("SYSTEM\\CurrentControlSet\\Services\\WSAProvider\\NetworkProvider");
    let mut disp: u32 = 0;
    if RegCreateKeyExW(HKEY_LOCAL_MACHINE, svc_key.as_ptr(), ptr::null_mut(), ptr::null_mut(), 0, KEY_WRITE, ptr::null_mut(), &mut hkey, &mut disp) == 0 {
        RegSetValueExW(hkey, to_wide("DeviceName").as_ptr(), 0, REG_SZ, to_wide("\\Device\\WSAProvider").as_ptr() as *const u8, 18 * 2);
        RegSetValueExW(hkey, to_wide("DisplayName").as_ptr(), 0, REG_SZ, to_wide("WSA Network Provider").as_ptr() as *const u8, 20 * 2);
        RegCloseKey(hkey);
    }
}

#[no_mangle]
pub unsafe extern "system" fn DllMain(_hinst: usize, reason: u32, _reserved: usize) -> BOOL {
    if reason == 1 { register_provider(); }
    1
}
