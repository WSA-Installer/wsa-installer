import os
import sys
import struct

import win32api
from PyInstaller.utils.win32 import versioninfo as _vi

RT_ICON = 3
RT_GROUP_ICON = 14
LOAD_LIBRARY_AS_DATAFILE = 0x00000002


def read_ico(ico_path):
    with open(ico_path, 'rb') as f:
        data = f.read()
    if data[:4] != b'\x00\x00\x01\x00':
        raise ValueError(f"Not a valid .ico file: {ico_path}")
    count = struct.unpack_from('<H', data, 4)[0]
    entries = []
    for i in range(count):
        w, h, colors, reserved, planes, bpp, size, offset = \
            struct.unpack_from('<BBBBHHII', data, 6 + i * 16)
        icon_data = data[offset:offset + size]
        entries.append({
            'w': w if w else 256,
            'h': h if h else 256,
            'colors': colors,
            'planes': planes,
            'bpp': bpp,
            'size': size,
            'data': icon_data,
        })
    return entries


def build_group_icon(entries):
    group = struct.pack('<HHH', 0, 1, len(entries))
    for i, e in enumerate(entries):
        w = e['w'] if e['w'] < 256 else 0
        h = e['h'] if e['h'] < 256 else 0
        group += struct.pack(
            '<BBBBHHIH',
            w, h, e['colors'], 0, e['planes'], e['bpp'], e['size'], i + 1,
        )
    return group


def discover_ids(exe_path):
    icon_ids = set()
    group_ids = set()
    try:
        h_mod = win32api.LoadLibraryEx(exe_path, 0, LOAD_LIBRARY_AS_DATAFILE)
        for res_type in (RT_ICON, RT_GROUP_ICON):
            try:
                names = win32api.EnumResourceNames(h_mod, res_type)
                for name in names:
                    if res_type == RT_ICON:
                        icon_ids.add(name)
                    elif res_type == RT_GROUP_ICON:
                        group_ids.add(name)
            except win32api.error:
                pass
        win32api.FreeLibrary(h_mod)
    except Exception as e:
        print(f"  [~] Discovery error: {e}")
        return set(), set()
    return icon_ids, group_ids


def patch_icons(exe_path, ico_path):
    entries = read_ico(ico_path)
    icon_ids, group_ids = discover_ids(exe_path)

    if not group_ids:
        group_ids.add(1)

    handle = win32api.BeginUpdateResource(exe_path, 0)

    group_data = build_group_icon(entries)
    for gid in group_ids:
        win32api.UpdateResource(handle, RT_GROUP_ICON, gid, group_data)
        print(f"  [+] Updated RT_GROUP_ICON ID={gid}")

    for i, e in enumerate(entries):
        res_id = i + 1
        win32api.UpdateResource(handle, RT_ICON, res_id, e['data'])
        sz = f"{e['w']}x{e['h']}"
        print(f"  [+] Updated RT_ICON ID={res_id} ({sz})")

    win32api.EndUpdateResource(handle, 0)
    return True


def patch_version_info(exe_path, version_info_path):
    info = _vi.load_version_info_from_text_file(version_info_path)
    _vi.write_version_info_to_executable(exe_path, info)
    print(f"  [+] Updated version info from {version_info_path}")


def patch_embedded_string(exe_path, old_str, new_str):
    with open(exe_path, 'rb') as f:
        data = bytearray(f.read())

    old_utf16 = old_str.encode('utf-16-le')
    new_utf16 = new_str.encode('utf-16-le')

    if len(new_utf16) > len(old_utf16):
        print(f"  [~] New string ({len(new_utf16)} bytes) longer than old ({len(old_utf16)} bytes) — skipping")
        return False

    idx = data.find(old_utf16)
    if idx < 0:
        print(f"  [~] String '{old_str}' not found in binary — skipping")
        return False

    padded = new_utf16 + b'\x00' * (len(old_utf16) - len(new_utf16))
    data[idx:idx + len(old_utf16)] = padded

    with open(exe_path, 'wb') as f:
        f.write(data)

    print(f"  [+] Replaced '{old_str}' -> '{new_str}' at offset 0x{idx:X}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: patch_flet.py <exe_path> [icon.ico] [file_version_info.txt]")
        sys.exit(1)

    exe_path = os.path.abspath(sys.argv[1])

    if not os.path.exists(exe_path):
        print(f"Error: {exe_path} not found")
        sys.exit(1)

    print(f"  Patcher: {exe_path}")

    ico_path = sys.argv[2] if len(sys.argv) > 2 else None
    ver_path = sys.argv[3] if len(sys.argv) > 3 else None

    if ico_path:
        ico_path = os.path.abspath(ico_path)
        if os.path.exists(ico_path):
            patch_icons(exe_path, ico_path)
        else:
            print(f"  [~] Icon not found: {ico_path}")

    if ver_path:
        ver_path = os.path.abspath(ver_path)
        if os.path.exists(ver_path):
            patch_version_info(exe_path, ver_path)
        else:
            print(f"  [~] Version info not found: {ver_path}")

    patch_embedded_string(exe_path, 'Flet description', 'WSA Installer')

    print(f"  [+] Done: {exe_path}")


if __name__ == '__main__':
    main()
