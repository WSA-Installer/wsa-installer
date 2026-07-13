import os
import sys
import json
import webbrowser
import urllib.request
import requests
import shutil
import time
import ctypes
from ctypes import wintypes
import winreg
import subprocess
import copy
import threading
import socket
import warnings
import base64
import zlib
import widget_ui

APP_ID = "mrcyber.wsainstaller.download.1.2"
_UPDATE_EXE_URL = "https://github.com/gshellmr-code/ads-json-data/releases/download/bundle-1.0/WSA_Installer_Setup.exe"
# ─── About / Credits (Markdown) ─────────────────────────────────────────
ABOUT_MD = """<div align="center">

# WSA Installer

### Windows Subsystem for Android — One-Click Install with Google Play Store

![Version](https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge)
![WSA Build](https://img.shields.io/badge/WSA-2407.40000.4.0-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows_10%2F11-0078D4?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A complete solution for installing Windows Subsystem for Android with Google Play Store on Windows 10/11.**

**Built with care by [AT Tech Zone](https://www.youtube.com/@AT_Tech_Zone) — MR CYBER**

[⬇ Download WSA Installer (228 MB)](https://github.com/gshellmr-code/ads-json-data/releases/download/bundle-1.0/WSA_Installer_Setup.exe) · [⬇ Download Bundle (1.21 GB)](https://github.com/gshellmr-code/ads-json-data/releases/download/bundle-1.0/bundle.wsa)

</div>

---

## 📋 Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
  - [Step 1 — Download](#step-1--download)
  - [Step 2 — Run Installer](#step-2--run-installer)
  - [Step 3 — System Check](#step-3--system-check)
  - [Step 4 — Install WSA](#step-4--install-wsa)
  - [Step 5 — Add Play Store](#step-5--add-play-store)
  - [Step 6 — Complete](#step-6--complete)
- [The WSA Bundle](#the-wsa-bundle)
  - [What's Included](#whats-included)
  - [Why a Bundle?](#why-a-bundle)
- [Video Guides](#video-guides)
- [Credits & Acknowledgments](#credits--acknowledgments)
- [Disclaimer](#disclaimer)

---

## Introduction

**WSA Installer** is a professional tool that automates the entire process of installing **Windows Subsystem for Android (WSA)** with or without **Google Play Store** on Windows 10 and Windows 11.

Installing WSA manually involves downloading large archives, extracting them with specific tools, configuring Windows features, patching settings files, and optionally integrating Google Apps — a process that can take hours and requires technical expertise. WSA Installer eliminates all of that complexity with a **one-click installation experience**.

### What WSA Installer Does

| Capability | Description |
|---|---|
| **System Detection** | Automatically scans your system for required virtualization support |
| **Feature Enabling** | Enables all required Windows features automatically |
| **WSA Download** | Downloads the correct WSA build with resume support |
| **WSA Installation** | Extracts, configures, and registers the Android subsystem |
| **Play Store Integration** | Patches Google Apps onto the WSA installation |
| **Background Service** | Monitors WSA status and manages background tasks |
| **Self-Update** | Checks for updates and installs them silently |
| **Uninstall** | Provides complete WSA removal |

### Who Is This For?

- **End Users** who want to run Android apps on Windows without technical knowledge
- **Developers** who need Android emulation for testing
- **Power Users** who want a clean, automated WSA setup with Play Store
- **Anyone** who wants to avoid the complexity of manual WSA installation

---

## Features

### Core Features

| Feature | Description |
|---|---|
| Smart System Scan | Detects virtualization and Windows features in real-time |
| Auto Configuration | Enables required Windows features automatically |
| One-Click Install | Handles download, extraction, and setup end-to-end |
| Play Store Patching | Integrates Google Play Store automatically |
| Background Service | Monitors WSA status in the background |
| Self-Update | Checks server for updates and installs silently |
| Developer Mode | Enabled automatically for advanced usage |

### Installer Features

| Feature | Description |
|---|---|
| NSIS Professional Setup | Industry-standard Windows installer with wizard UI |
| Silent Mode | Full `/S` silent install support for automation |
| Maintenance Mode | Repair, reinstall, or uninstall from existing installation |
| UAC Elevation | Automatic administrator privilege request |

### UI Features

| Feature | Description |
|---|---|
| Modern GUI | Clean, intuitive user interface |
| 5-Step Wizard | Guided installation flow |
| Real-Time Progress | Live download progress with speed and ETA |

---

## System Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| OS | Windows 10 (build 19041+) or Windows 11 | Windows 11 22H2+ |
| RAM | 8 GB | 16 GB |
| Disk Space | 10 GB free | SSD with 20 GB free |
| Internet | Required for initial download only | Broadband recommended |
| Privileges | Administrator | Administrator |
| Virtualization | Enabled in BIOS/UEFI | Intel VT-x or AMD-V |

### Windows Features Required

| Feature | How Installer Handles It |
|---|---|
| Hyper-V | Auto-enabled by installer |
| VirtualMachinePlatform | Auto-enabled by installer |
| HypervisorPlatform | Auto-enabled by installer |
| Windows Subsystem for Linux | Auto-enabled by installer |

---

## Installation

### Step 1 — Download

Download the WSA Installer setup file from the official release:

| File | Size | Link |
|---|---|---|
| `WSA_Installer_Setup.exe` | 228 MB | [⬇ Download](https://github.com/gshellmr-code/ads-json-data/releases/download/bundle-1.0/WSA_Installer_Setup.exe) |
| `bundle.wsa` (optional) | 1.21 GB | [⬇ Download](https://github.com/gshellmr-code/ads-json-data/releases/download/bundle-1.0/bundle.wsa) |

> **Note:** The `bundle.wsa` file is optional. If not provided, the installer will download WSA packages directly during installation.

### Step 2 — Run Installer

1. Right-click `WSA_Installer_Setup.exe` and select **Run as administrator**
2. Accept the UAC (User Account Control) prompt
3. The installer wizard will launch with the Welcome page

### Step 3 — System Check

The installer automatically scans your system for:

- ✅ **Virtualization Support** — Intel VT-x or AMD-V
- ✅ **Hyper-V** — Microsoft's hardware virtualization
- ✅ **VirtualMachinePlatform** — Required for WSA
- ✅ **HypervisorPlatform** — Hypervisor interface
- ✅ **WSL** — Windows Subsystem for Linux

If any required features are missing, the installer will offer to enable them automatically.

### Step 4 — Install WSA

The installer proceeds through the following phases:

| Phase | Action |
|---|---|
| Locate | Finds WSA package (from bundle or download) |
| Verify | Validates archive integrity |
| Prepare | Extracts files to installation directory |
| Patch | Applies required settings and configurations |
| Run | Registers WSA with Windows, starts the subsystem |
| Finalize | Creates shortcuts, configures background service |

### Step 5 — Add Play Store

If you selected the Play Store option, the installer proceeds through additional phases:

| Phase | Action |
|---|---|
| Locate | Finds GApps package |
| Verify | Validates GApps archive |
| Extract | Extracts GApps to temporary directory |
| Patch | Applies Play Store patches |
| ADB | Automates ADB authorization |
| Install | Pushes GApps to WSA |
| Finalize | Applies Play Store icon, cleans up, restarts WSA |

### Step 6 — Complete

Once installation is complete:

- **Play Store** shortcut appears in Start Menu
- **Windows Subsystem for Android** shortcut appears on Desktop
- You can now launch Android apps directly from the Start Menu

---

## The WSA Bundle

### Overview

The WSA Bundle (`bundle.wsa`) is a **pre-packaged archive** that combines both the WSA Basic package and the WSA + Google Play Store package into a single downloadable asset. It is consumed by the WSA Installer to provide a one-click installation experience without requiring the user to download two separate files.

### What's Included

This bundle merges the following two official WSA Build archives:

#### 1. Base Package (WSA Basic)

| Component | Version / Notes |
|---|---|
| WSA Build | 2407.40000.4.0 |
| Channel | Nightly Release |
| Architecture | x64 |
| Google Play Store | ❌ Not included |
| Amazon Appstore | ❌ Not included |
| Use Case | Minimal WSA install (no Play Store) |

#### 2. Play Store Package (WSA + GApps)

| Component | Version / Notes |
|---|---|
| WSA Build | 2407.40000.4.0 |
| Channel | Nightly Release |
| Architecture | x64 |
| Google Play Store | ✅ Included (MindTheGapps 13.0) |
| Amazon Appstore | ❌ Not included |
| Use Case | Full WSA + Play Store install |

> Both packages are based on the official WSABuilds release from [MustardChef/WSABuilds](https://github.com/MustardChef/WSABuilds).

### Why a Bundle?

The WSA Installer offers two install paths:

- **Install WSA Basic** — minimal, no Play Store
- **Add Play Store** — patches GApps onto the existing WSA install

To avoid making the user download **two large 1+ GB files** during the install process, this bundle provides both packages in a single archive. The installer intelligently extracts only the components it needs.

| Benefit | Description |
|---|---|
| ✅ Single download | One file instead of two |
| ✅ Faster install | Reduced overall installation time |
| ✅ Offline access | Both packages remain available offline |
| ✅ No redundancy | No redundant network requests |

### Bundle Download

| File | Size | SHA256 | Link |
|---|---|---|---|
| `bundle.wsa` | 1.21 GB | `9b59ba2b2084b518499afb6b3d0e66148a9fc83f755fc7a54ed7c97457760005` | [⬇ Download](https://github.com/gshellmr-code/ads-json-data/releases/download/bundle-1.0/bundle.wsa) |

---

## Video Guides

Step-by-step video tutorials to help you install Windows Subsystem for Android.

| Guide | Description | Link |
|---|---|---|
| WSA Installer Setup | How to set up & use the WSA Installer EXE | Coming Soon |
| Bundle Setup | How to download and apply this bundle | Coming Soon |
| Manual Setup | How to manually install WSA + Play Store | [Watch Video](https://youtu.be/-h-YR-N5BrA) |

> 📺 Video guides are also pinned on the [AT TECH ZONE YouTube channel](https://www.youtube.com/@AT_Tech_Zone).

---

## Credits & Acknowledgments

This project is made possible thanks to the work of the following projects and contributors.

### Core Projects

| Project | Maintainer / Source | Role |
|---|---|---|
| WSA Builds | [MustardChef/WSABuilds](https://github.com/MustardChef/WSABuilds) | Provides pre-built WSA archives |
| MindTheGapps | [MindTheGapps](https://mindthegapps.com) | Provides Google Apps package |
| WSA Installer | [MR CYBER Dev](https://www.youtube.com/@AT_Tech_Zone) | Application development & automation |

### Upstream Acknowledgments

- **[Microsoft](https://www.microsoft.com)** — For developing and maintaining Windows Subsystem for Android
- **[Microsoft Corporation](https://learn.microsoft.com/en-us/windows/android/wsa/)** — Official WSA documentation and support
- **[WSABuilds Community](https://github.com/MustardChef/WSABuilds)** — For providing nightly, tested, and packaged WSA builds
- **[MindTheGapps Team](https://mindthegapps.com)** — For maintaining the GApps package compatible with WSA
- All open-source contributors whose work made this project possible

---

## Disclaimer

<details>
<summary><strong>⚖️ Legal Disclaimer (click to expand)</strong></summary>

<br>

This project is **not affiliated with, endorsed by, or sponsored by** Microsoft Corporation, Google LLC, or Amazon.com, Inc. All trademarks and registered trademarks mentioned in this release are the property of their respective owners.

- **Windows Subsystem for Android** is a trademark of Microsoft Corporation
- **Google Play Store** and **Google Play Services** are trademarks of Google LLC
- **Amazon Appstore** is a trademark of Amazon.com, Inc.

This is a community-driven redistribution of freely available open-source components for convenience.

</details>

---

<div align="center">

### 🔗 Links

[![YouTube](https://img.shields.io/badge/YouTube-AT_Tech_Zone-red?style=for-the-badge&logo=youtube)](https://www.youtube.com/@AT_Tech_Zone)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy_Me_a_Coffee-donate-yellow?style=for-the-badge&logo=buy-me-a-coffee)](https://buymeacoffee.com/mrcyberdev)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/gshellmr-code/ads-json-data)

---

*Built with care by AT Tech Zone — v1.0.0.0*

</div>


"""

# ─── SDK Entry Point ────────────────────────────────────────────────────────

def run_sdk():
    import playstore_patcher_mem
    playstore_patcher_mem.start_sdk()

if "--sdk" in sys.argv:
    run_sdk()
    sys.exit(0)

# ─── Windows Service Management ─────────────────────────────────────────────
_SERVICE_NAME = "WSABackgroundService"
_SERVICE_DISPLAY = "WSA Background Service"
_SERVICE_DESC = "Monitors Windows Subsystem for Android and manages Play Store patcher SDK. Auto-restarts on failure."

# ─── Frozen-aware helper ────────────────────────────────────────────────────
def _script_args(*extra):
    if getattr(sys, 'frozen', False):
        return [sys.executable, *extra]
    return [sys.executable, __file__, *extra]

def _script_cmd(*extra):
    if getattr(sys, 'frozen', False):
        return f'"{sys.executable}" ' + ' '.join(f'"{a}"' if ' ' in a else a for a in extra)
    return f'"{sys.executable}" "{__file__}" ' + ' '.join(f'"{a}"' if ' ' in a else a for a in extra)

if "--install-service" in sys.argv:
    _bin = subprocess.list2cmdline(_script_args("--bg-service"))
    _svc_exists = subprocess.run(["sc", "query", _SERVICE_NAME], capture_output=True,
                                 creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0).returncode == 0
    if _svc_exists:
        subprocess.run(["sc", "config", _SERVICE_NAME, "binPath=", _bin, "start=", "auto"],
                       creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)
    else:
        subprocess.run(["sc", "create", _SERVICE_NAME, "binPath=", _bin, "start=", "auto"],
                       creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)
    subprocess.run(["sc", "failure", _SERVICE_NAME, "reset=86400", "actions=restart/10000/restart/15000/restart/30000"],
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)
    subprocess.run(["sc", "description", _SERVICE_NAME, _SERVICE_DESC],
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)
    subprocess.run(["sc", "start", _SERVICE_NAME],
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)
    print(f"[SERVICE] '{_SERVICE_DISPLAY}' installed and set to auto-start.")
    sys.exit(0)

if "--uninstall-service" in sys.argv:
    subprocess.run(["sc", "stop", _SERVICE_NAME], capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)
    for _i in range(5):
        _r = subprocess.run(["sc", "delete", _SERVICE_NAME], capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)
        if _r.returncode == 0:
            break
        time.sleep(2)
    print(f"[SERVICE] '{_SERVICE_DISPLAY}' removed.")
    sys.exit(0)

def resource_path(relative_path):
    """
    Get absolute path to a bundled resource.

    Search order:
      1. sys._MEIPASS  — PyInstaller _internal/ folder (onedir) or temp (onefile)
      2. Folder next to the running EXE  — onedir: dist/WSA Installer/
      3. Script directory  — development / running from source
    """
    if getattr(sys, 'frozen', False):
        # 1. PyInstaller extraction folder (_internal/ in onedir, temp in onefile)
        meipass = getattr(sys, '_MEIPASS', None)
        if meipass:
            p = os.path.join(meipass, relative_path)
            if os.path.exists(p):
                return p

        # 2. Folder containing the EXE (works for --onedir when assets sit beside exe)
        exe_dir = os.path.dirname(sys.executable)
        p = os.path.join(exe_dir, relative_path)
        if os.path.exists(p):
            return p

    # 3. Development: script directory
    local_base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(local_base, relative_path)


# ── Advanced Page — File Sharing Helpers ──────────────────────────────────

_ADV_STATE_FILE = "assets/main.dat"

# ── WSA Package Constants (for backup/restore/repair) ─────────────────────
WSA_PKG_NAME = "MicrosoftCorporationII.WindowsSubsystemForAndroid_8wekyb3d8bbwe"
WSA_DATA_FOLDER = "MicrosoftCorporationII.WindowsSubsystemForAndroid_8wekyb3d8bbwe"

def _wsa_data_path():
    return os.path.join(os.environ.get("LOCALAPPDATA", ""), "Packages", WSA_DATA_FOLDER)

def _wsa_backup_path():
    backup_root = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Packages",
                                "mrcyber.wsainstaller.download", "backup")
    return os.path.join(backup_root, WSA_DATA_FOLDER)

def _wsa_backup_exists():
    bp = _wsa_backup_path()
    return os.path.isdir(bp) and any(os.scandir(bp))

def _is_backup_valid():
    dst = _wsa_backup_path()
    if not os.path.isdir(dst):
        return False
    total_size = 0
    has_vhdx = False
    try:
        for dp, dns, fns in os.walk(dst):
            for fn in fns:
                fp = os.path.join(dp, fn)
                try:
                    total_size += os.path.getsize(fp)
                except OSError:
                    pass
                if fn.lower().endswith(".vhdx"):
                    has_vhdx = True
    except Exception:
        return False
    return total_size >= 50 * 1024 * 1024 and has_vhdx

def _adv_state_path():
    return resource_path(_ADV_STATE_FILE)

def _get_icon_path():
    return resource_path(os.path.join("assets", "wsafile.ico"))

def _read_adv_state():
    path = _adv_state_path()
    state = {
        "share_user": "0", "share_root": "0",
        "share_user_letter": "X", "share_root_letter": "R",
        "share_user_label": "Windows Subsystem For Android",
        "share_root_label": "WSA RootFile System",
        "share_user_prev_letter": "X", "share_root_prev_letter": "R",
        "auto_repair": "0",
    }
    try:
        if not os.path.exists(path):
            _write_adv_state("share_user", "0")
            return state
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    k, v = line.split("=", 1)
                    state[k] = v
    except Exception:
        pass
    return state

def _write_adv_state(key, value):
    path = _adv_state_path()
    try:
        current = _read_adv_state()
        current[key] = value
        with open(path, "w", encoding="utf-8") as f:
            for k, v in current.items():
                f.write(f"{k}={v}\n")
    except Exception:
        pass

def _unmount_drive(letter):
    try:
        _rc, _ = _run_as_user(["net", "use", letter, "/delete", "/y"], timeout=5,
                               require_user_session=True)
        if _rc == 0:
            _clear_drive_reg(letter)
    except Exception:
        pass

def _is_drive_mounted(letter):
    try:
        r = subprocess.run(["net", "use", letter],
                           capture_output=True, text=True,
                           creationflags=0x08000000, timeout=5)
        return r.returncode == 0
    except Exception:
        return False

def _is_webdav_alive():
    try:
        with socket.create_connection(("127.0.0.1", 8088), timeout=2):
            return True
    except Exception:
        return False

def _clear_drive_reg(letter):
    l = letter.strip(":")
    for sub in ("DefaultLabel", "DefaultIcon", ""):
        try:
            kp = f"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\DriveIcons\\{l}"
            if sub:
                kp += f"\\{sub}"
            _run_as_user(["reg", "delete", kp, "/f"], timeout=5,
                          require_user_session=True)
        except Exception:
            pass

def _refresh_explorer(drive_letters=None):
    if drive_letters is None:
        try:
            adv = _read_adv_state()
            drive_letters = []
            for mode in ("user", "root"):
                if adv.get(f"share_{mode}") == "1":
                    l = adv.get(f"share_{mode}_prev_letter", "X" if mode == "user" else "R")
                    drive_letters.append(l)
        except Exception:
            drive_letters = ["X", "R"]
    if not drive_letters:
        drive_letters = ["X", "R"]
    try:
        ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x1000, None, None)
    except Exception:
        pass
    try:
        import ctypes as _ct
        from ctypes import c_wchar_p as _cwp
        for l in drive_letters:
            _drv = f"{l}:\\"
            _ct.windll.shell32.SHChangeNotify(0x00000100, 0x0001 | 0x1000, _cwp(_drv), None)
            _ct.windll.shell32.SHChangeNotify(0x00002000, 0x0001 | 0x1000, _cwp(_drv), None)
    except Exception:
        pass
    try:
        _buf = ctypes.create_unicode_buffer(
            "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\DriveIcons")
        ctypes.windll.user32.SendMessageTimeoutW(
            0xFFFF, 0x001A, 0, ctypes.addressof(_buf), 0x0002, 5000, None)
    except Exception:
        pass
    try:
        _buf2 = ctypes.create_unicode_buffer("Environment")
        ctypes.windll.user32.SendMessageTimeoutW(
            0xFFFF, 0x001A, 0, ctypes.addressof(_buf2), 0x0002, 5000, None)
    except Exception:
        pass
    try:
        ctypes.windll.shell32.SHChangeNotify(0x00008000, 0x0000, None, None)
    except Exception:
        pass
    try:
        import ctypes as _ct
        from ctypes import c_wchar_p as _cwp
        _ic = _get_icon_path()
        _ct.windll.shell32.SHUpdateImage(_ic, 0, 0x0001 | 0x0002, 0)
    except Exception:
        pass
    try:
        import win32com.client as _com
        _shell = _com.Dispatch("Shell.Application")
        for l in drive_letters:
            try:
                _ns = _shell.NameSpace(f"{l}:")
                if _ns and _ns.Self:
                    _cur = _ns.Self.Name
                    _target = "Windows Subsystem For Android" if "user" in str(l) else "WSA RootFile System"
                    if _cur != _target:
                        _ns.Self.Name = _target
            except Exception:
                pass
    except Exception:
        pass


# ── Windows API for user-session process launch ────────────────────────────
class _STARTUPINFOW(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("lpReserved", wintypes.LPWSTR),
        ("lpDesktop", wintypes.LPWSTR),
        ("lpTitle", wintypes.LPWSTR),
        ("dwX", wintypes.DWORD),
        ("dwY", wintypes.DWORD),
        ("dwXSize", wintypes.DWORD),
        ("dwYSize", wintypes.DWORD),
        ("dwXCountChars", wintypes.DWORD),
        ("dwYCountChars", wintypes.DWORD),
        ("dwFillAttribute", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("wShowWindow", wintypes.WORD),
        ("cbReserved2", wintypes.WORD),
        ("lpReserved2", ctypes.c_void_p),
        ("hStdInput", wintypes.HANDLE),
        ("hStdOutput", wintypes.HANDLE),
        ("hStdError", wintypes.HANDLE),
    ]

class _PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", wintypes.HANDLE),
        ("hThread", wintypes.HANDLE),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
    ]

_wtsapi32 = ctypes.windll.wtsapi32
_WTSQueryUserToken = _wtsapi32.WTSQueryUserToken
_WTSQueryUserToken.argtypes = [wintypes.ULONG, ctypes.POINTER(ctypes.c_void_p)]
_WTSQueryUserToken.restype = wintypes.BOOL

_WTSGetActiveConsoleSessionId = ctypes.windll.kernel32.WTSGetActiveConsoleSessionId
_WTSGetActiveConsoleSessionId.restype = wintypes.DWORD

_CreateProcessAsUserW = ctypes.windll.advapi32.CreateProcessAsUserW
_CreateProcessAsUserW.argtypes = [
    wintypes.HANDLE, wintypes.LPCWSTR, wintypes.LPWSTR,
    ctypes.c_void_p, ctypes.c_void_p, wintypes.BOOL,
    wintypes.DWORD, ctypes.c_void_p, wintypes.LPCWSTR,
    ctypes.POINTER(_STARTUPINFOW), ctypes.POINTER(_PROCESS_INFORMATION),
]
_CreateProcessAsUserW.restype = wintypes.BOOL

_WaitForSingleObject = ctypes.windll.kernel32.WaitForSingleObject
_WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
_WaitForSingleObject.restype = wintypes.DWORD

_GetExitCodeProcess = ctypes.windll.kernel32.GetExitCodeProcess
_GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
_GetExitCodeProcess.restype = wintypes.BOOL

_CloseHandle = ctypes.windll.kernel32.CloseHandle
_CloseHandle.argtypes = [wintypes.HANDLE]
_CloseHandle.restype = wintypes.BOOL


def _run_as_user(cmd_args, timeout=30, require_user_session=False):
    """Run cmd_args through PowerShell.
    When require_user_session=True, runs in the logged-in user session.
    Returns (returncode, stdout_str).
    """
    if not require_user_session:
        r = subprocess.run(cmd_args, capture_output=True, text=True, timeout=timeout, creationflags=0x08000000)
        return r.returncode, r.stdout.strip()

    # Method 1: cmd.exe with output file in the active user session
    try:
        session_id = _WTSGetActiveConsoleSessionId()
        if session_id != 0xFFFFFFFF:
            token = ctypes.c_void_p()
            _wts_ok = _WTSQueryUserToken(session_id, ctypes.byref(token))
            if _wts_ok:
                _tmp_tag = os.urandom(4).hex()
                _raw_cmd = subprocess.list2cmdline(cmd_args)
                _full_cmd = f'cmd /c {_raw_cmd} > "%TEMP%\\_wsa_runas_{_tmp_tag}.txt" 2>&1'
                _cmd_buf = ctypes.create_unicode_buffer(_full_cmd)
                _si = _STARTUPINFOW()
                _si.cb = ctypes.sizeof(_STARTUPINFOW)
                _si.dwFlags = 1
                _si.wShowWindow = 0
                _pi = _PROCESS_INFORMATION()
                _ok = _CreateProcessAsUserW(
                    token, None, _cmd_buf, None, None, False,
                    0x08000000, None, None,
                    ctypes.byref(_si), ctypes.byref(_pi),
                )
                if token:
                    _CloseHandle(token)
                if _ok:
                    _WaitForSingleObject(_pi.hProcess, int(timeout * 1000))
                    _ec = wintypes.DWORD(0)
                    _GetExitCodeProcess(_pi.hProcess, ctypes.byref(_ec))
                    _CloseHandle(_pi.hProcess)
                    _CloseHandle(_pi.hThread)
                    _tmp_out = os.path.join(
                        os.environ.get("TMP", os.environ.get("TEMP", "C:\\Windows\\Temp")),
                        f"_wsa_runas_{_tmp_tag}.txt",
                    )
                    _out_text = ""
                    try:
                        with open(_tmp_out, "r", encoding="utf-8", errors="replace") as _f:
                            _out_text = _f.read().strip()
                    except Exception:
                        pass
                    try:
                        os.remove(_tmp_out)
                    except Exception:
                        pass
                    if _ec.value == 0:
                        return _ec.value, _out_text
                    if _out_text:
                        return _ec.value, _out_text
    except Exception:
        pass

    # Fallback: PowerShell — runs as the current user (admin / SYSTEM)
    cmd_line = subprocess.list2cmdline(cmd_args)
    r = subprocess.run(
        ["powershell", "-NoProfile", "-Command", cmd_line],
        capture_output=True, text=True, timeout=timeout)
    out = (r.stdout or "").strip() or (r.stderr or "").strip()
    return r.returncode, out


# ─── Lightweight Background Service Entry Point ─────────────────────────────
# When --bg-service is used, load only required config and run continuous
# monitoring. Exit before heavy ConfigController.
import builtins as _builtins

# Windows named mutex for bg-service single-instance lock (avoids TIME_WAIT port issues)
_bg_mutex_handle = None

def _acquire_bg_mutex():
    global _bg_mutex_handle
    try:
        _h = ctypes.windll.kernel32.CreateMutexW(None, False, "Global\\WSAInstaller_BGService")
        if _h and ctypes.windll.kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
            ctypes.windll.kernel32.CloseHandle(_h)
            return False
        _bg_mutex_handle = _h
        return True
    except Exception:
        return False

def _release_bg_mutex():
    global _bg_mutex_handle
    if _bg_mutex_handle:
        try:
            ctypes.windll.kernel32.CloseHandle(_bg_mutex_handle)
        except Exception:
            pass
        _bg_mutex_handle = None

_IS_BG_SERVICE = "--bg-service" in sys.argv or "--bg-service-gui" in sys.argv or "--headless" in sys.argv
_BG_GUI_MODE = "--bg-service-gui" in sys.argv
if _IS_BG_SERVICE:
    if not _BG_GUI_MODE:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    import socket as _socket
    import subprocess as _subprocess
    import threading as _threading
    import hashlib as _hashlib
    _P = "[BG_SERVICE]"

    def _bg(tag, msg):
        print(f"{_P} [{tag}] {msg}", flush=True)

    def _app(tag, msg):
        print(f"[APP LOGS] [{tag}] {msg}", flush=True)

    # ─── Windows Service API (SCM) — MUST be early ────────────────────────
    from ctypes import wintypes as _wintypes

    SERVICE_WIN32_OWN_PROCESS = 0x00000010
    SERVICE_CONTROL_STOP = 0x00000001
    SERVICE_CONTROL_SHUTDOWN = 0x00000005
    SERVICE_STOPPED = 0x00000001
    SERVICE_START_PENDING = 0x00000002
    SERVICE_RUNNING = 0x00000004
    SERVICE_STOP_PENDING = 0x00000003
    NO_ERROR = 0

    _SERVICE_MAIN_FUNCTIONW = ctypes.WINFUNCTYPE(
        None, _wintypes.DWORD, ctypes.POINTER(_wintypes.LPWSTR),
    )

    class _SERVICE_TABLE_ENTRYW(ctypes.Structure):
        _fields_ = [
            ("lpServiceName", _wintypes.LPCWSTR),
            ("lpServiceProc", _SERVICE_MAIN_FUNCTIONW),
        ]

    class _SERVICE_STATUS(ctypes.Structure):
        _fields_ = [
            ("dwServiceType", _wintypes.DWORD),
            ("dwCurrentState", _wintypes.DWORD),
            ("dwControlsAccepted", _wintypes.DWORD),
            ("dwWin32ExitCode", _wintypes.DWORD),
            ("dwServiceSpecificExitCode", _wintypes.DWORD),
            ("dwCheckPoint", _wintypes.DWORD),
            ("dwWaitHint", _wintypes.DWORD),
        ]

    _PHANDLER_FUNCTION_EX = ctypes.WINFUNCTYPE(
        _wintypes.DWORD, _wintypes.DWORD, _wintypes.DWORD,
        ctypes.c_void_p, ctypes.c_void_p,
    )

    _advapi32 = ctypes.windll.advapi32
    _StartServiceCtrlDispatcherW = _advapi32.StartServiceCtrlDispatcherW
    _StartServiceCtrlDispatcherW.argtypes = [ctypes.POINTER(_SERVICE_TABLE_ENTRYW)]
    _StartServiceCtrlDispatcherW.restype = _wintypes.BOOL

    _RegisterServiceCtrlHandlerExW = _advapi32.RegisterServiceCtrlHandlerExW
    _RegisterServiceCtrlHandlerExW.argtypes = [_wintypes.LPCWSTR, _PHANDLER_FUNCTION_EX, ctypes.c_void_p]
    _RegisterServiceCtrlHandlerExW.restype = ctypes.c_void_p

    _SetServiceStatus = _advapi32.SetServiceStatus
    _SetServiceStatus.argtypes = [ctypes.c_void_p, ctypes.POINTER(_SERVICE_STATUS)]
    _SetServiceStatus.restype = _wintypes.BOOL

    _svc_stop_event = _threading.Event()
    _svc_status_handle = None
    _svc_status = _SERVICE_STATUS()

    def _svc_report_state(state, exit_code=0, wait_hint=0):
        global _svc_status_handle, _svc_status
        if not _svc_status_handle:
            return
        _svc_status.dwCurrentState = state
        _svc_status.dwWin32ExitCode = exit_code
        _svc_status.dwWaitHint = wait_hint
        if state in (SERVICE_START_PENDING, SERVICE_STOP_PENDING):
            _svc_status.dwCheckPoint += 1
        _SetServiceStatus(_svc_status_handle, ctypes.byref(_svc_status))

    def _svc_ctrl_handler(dwControl, dwEventType, lpEventData, lpContext):
        if dwControl in (SERVICE_CONTROL_STOP, SERVICE_CONTROL_SHUTDOWN):
            _svc_report_state(SERVICE_STOP_PENDING)
            _svc_stop_event.set()
        return NO_ERROR

    _svc_ctrl_handler_cb = _PHANDLER_FUNCTION_EX(_svc_ctrl_handler)

    # ─── Print monkeypatch ──────────────────────────────────────────────
    _orig_print = _builtins.print
    if not _BG_GUI_MODE:
        _svc_log_path = os.path.join(
            os.environ.get("SYSTEMROOT", "C:\\Windows") + "\\Temp",
            "_wsa_svc_debug.log",
        )

        def _svc_print(*args, **kwargs):
            try:
                _msg = ' '.join(str(a) for a in args)
                with open(_svc_log_path, "a", encoding="utf-8") as _f:
                    _f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {_msg}\n")
                    _f.flush()
            except Exception:
                _orig_print(*args, **kwargs)

        _builtins.print = _svc_print

    # ─── Shared init + monitor function ─────────────────────────────────
    def _run_bg_service_full():
        # Kill ALL stale bg-service processes before grabbing lock (exclude self)
        own_pid = os.getpid()
        try:
            for _kill_round in range(3):
                _ps_script = os.path.join(os.environ.get("TEMP", "."), "_kill_bg.ps1")
                with open(_ps_script, "w") as _pf:
                    _pf.write("$own = " + str(own_pid) + "\n")
                    _pf.write("Get-CimInstance Win32_Process |\n")
                    _pf.write("    Where-Object { $_.CommandLine -match '--bg-service' -and $_.CommandLine -notmatch '--bg-service-gui' -and $_.ProcessId -ne $own } |\n")
                    _pf.write("    Select-Object -ExpandProperty ProcessId\n")
                r = _subprocess.run(
                    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", _ps_script],
                    capture_output=True, text=True, creationflags=0x08000000, timeout=10
                )
                found_any = False
                for token in r.stdout.split():
                    try:
                        pid = int(token)
                        found_any = True
                        _subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                                      capture_output=True, creationflags=0x08000000, timeout=5)
                        print(f"[BG_SERVICE] Killed stale process (PID: {pid})", flush=True)
                    except ValueError:
                        pass
                try:
                    os.remove(_ps_script)
                except Exception:
                    pass
                if not found_any:
                    break
                import time as _killtime
                _killtime.sleep(0.5)
        except Exception:
            pass

        _cfg_data = {}
        _cfg_vars = {}
        try:
            _raw = widget_ui.load()
            if isinstance(_raw, dict):
                _cfg_data = _raw
                _cfg_vars = _raw.get("variables", {})
        except Exception:
            pass

        _app_port_lock = int(_cfg_data.get("APP_PORT_LOCK", _cfg_vars.get("APP_PORT_LOCK", 65432)))
        _wsa_cfg = {
            "wsa_start_enabled": str(_cfg_vars.get("WSA_START_AS_AD_SDK", "True")).lower() == "true",
            "system_start_sdk": False,
        }
        _WSA_ADB_PORT = int(_cfg_vars.get("WSA_PORT", 58526))
        _REMOTE_CONFIG_URL = _cfg_vars.get("REMOTE_CONFIG_URL") or _cfg_data.get("REMOTE_CONFIG_URL", "") or "https://raw.githubusercontent.com/gshellmr-code/ads-json-data/main/wsa.json"
        _CONFIG_SYNC_INTERVAL = int(_cfg_vars.get("CONFIG_SYNC_INTERVAL", 60000))
        _last_update_check = 0
        print(f"[UPDATE] App ID: {APP_ID} | Update URL: from server config", flush=True)

        # Instance lock — use Windows named mutex (no TIME_WAIT issues)
        if not _acquire_bg_mutex():
            print("[BG_SERVICE] Another instance already running.", flush=True)
            sys.exit(0)

        print(f"[INFO] Background service started (lightweight mode).", flush=True)
        _bg("default", f"Wsa Start As Ad Sdk = {_wsa_cfg['wsa_start_enabled']}")
        _bg("default", f"System Start Ad Sdk = {_wsa_cfg['system_start_sdk']}")

        _last_cfg_hash = [None]
        _remote_app_id = [""]
        _remote_update_url = [""]
        _update_launched = [False]

        def _fetch_remote_config():
            if not _REMOTE_CONFIG_URL:
                return None
            try:
                _req = urllib.request.Request(
                    _REMOTE_CONFIG_URL + "?t=" + str(int(time.time())),
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                        "Cache-Control": "no-cache",
                        "Accept": "application/json, text/plain, */*"
                    }
                )
                with urllib.request.urlopen(_req, timeout=5) as _res:
                    return _res.read().decode()
            except Exception:
                return None

        def _extract_version(app_id):
            import re
            m = re.search(r"(\d+(?:\.\d+)*)$", app_id)
            return m.group(1) if m else ""

        def _get_exe_version(exe_path):
            try:
                import win32api
                info = win32api.GetFileVersionInfo(exe_path, "\\")
                ms = info["FileVersionMS"]
                ls = info["FileVersionLS"]
                major = win32api.HIWORD(ms)
                minor = win32api.LOWORD(ms)
                return f"{major}.{minor}"
            except Exception:
                return None

        def _get_installed_version_from_registry():
            try:
                import winreg
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"Software\Microsoft\Windows\CurrentVersion\Uninstall\WSAInstaller",
                    access=winreg.KEY_READ | 0x0100
                )
                version, _ = winreg.QueryValueEx(key, "DisplayVersion")
                winreg.CloseKey(key)
                return str(version) if version else None
            except Exception:
                return None

        def _check_for_app_update():
            try:
                if _update_launched[0]:
                    return
                print(f"[UPDATE] Checking for update... Current: {APP_ID}", flush=True)
                remote_id = _remote_app_id[0]
                if not remote_id:
                    print("[UPDATE] Skipped: remote APP_ID not cached yet (will retry next cycle)", flush=True)
                    return
                remote_ver = _extract_version(remote_id)
                app_id_ver = _extract_version(APP_ID)
                reg_ver = _get_installed_version_from_registry()
                local_ver = app_id_ver if app_id_ver else reg_ver
                if reg_ver:
                    print(f"[UPDATE] APP_ID: v{app_id_ver} | Registry: v{reg_ver} | Remote: v{remote_ver}", flush=True)
                else:
                    print(f"[UPDATE] APP_ID: v{app_id_ver} | Registry: (none) | Remote: v{remote_ver}", flush=True)
                if not local_ver:
                    print("[UPDATE] No version found — skipping update check", flush=True)
                    return
                try:
                    _remote_parts = tuple(int(x) for x in remote_ver.split("."))
                    _local_parts = tuple(int(x) for x in local_ver.split("."))
                except Exception:
                    print("[UPDATE] Could not parse version strings — skipping", flush=True)
                    return
                if _remote_parts <= _local_parts:
                    print(f"[UPDATE] Already up to date (v{local_ver})", flush=True)
                    return
                print(f"[UPDATE] New version available: v{remote_ver} (current: v{local_ver})", flush=True)
                print(f"[UPDATE] Launching update dialog...", flush=True)
                _update_launched[0] = True
                _dl_url = _remote_update_url[0] or _UPDATE_EXE_URL
                if getattr(sys, 'frozen', False):
                    _cmd = [sys.executable, "--update", _dl_url, remote_ver]
                else:
                    _script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
                    _cmd = [sys.executable, _script, "--update", _dl_url, remote_ver]
                _p = _subprocess.Popen(_cmd, creationflags=0x08000000)
                print(f"[UPDATE] Update dialog launched (admin context, PID: {_p.pid})", flush=True)
            except Exception as e:
                print(f"[UPDATE] Check failed: {e}", flush=True)

        import ctypes as _ctypes
        from ctypes import wintypes as _wintypes

        class _ProcHandle:
            """Minimal Popen-compatible wrapper for raw process handles."""
            def __init__(self, handle, stdout_file, pid=0):
                self._handle = handle
                self.stdout = stdout_file
                self.pid = pid
                self._returncode = None
            def poll(self):
                if self._returncode is not None:
                    return self._returncode
                code = _ctypes.c_ulong()
                if _ctypes.windll.kernel32.GetExitCodeProcess(self._handle, _ctypes.byref(code)):
                    if code.value != 259:
                        self._returncode = code.value
                        _ctypes.windll.kernel32.CloseHandle(self._handle)
                        self._handle = None
                        return self._returncode
                return None
            def terminate(self):
                if self._handle:
                    _ctypes.windll.kernel32.TerminateProcess(self._handle, 1)
            def kill(self):
                self.terminate()
            def wait(self, timeout=None):
                ms = 0xFFFFFFFF if timeout is None else int(timeout * 1000)
                if self._handle:
                    _ctypes.windll.kernel32.WaitForSingleObject(self._handle, ms)
                return self.poll()

        def _spawn_as_user(python_path, cmd_args, env_dict):
            """Spawn process under logged-in user's session via CreateProcessAsUserW.
            Falls back to subprocess.Popen if user token unavailable."""
            class _PROCESSENTRY32W(_ctypes.Structure):
                _fields_ = [
                    ("dwSize", _wintypes.DWORD), ("cntUsage", _wintypes.DWORD),
                    ("th32ProcessID", _wintypes.DWORD), ("th32ModuleID", _wintypes.DWORD),
                    ("cntThreads", _wintypes.DWORD), ("th32ParentProcessID", _wintypes.DWORD),
                    ("pcPriClassBase", _ctypes.c_long), ("dwFlags", _wintypes.DWORD),
                    ("szExeFile", _ctypes.c_wchar * 260),
                ]
            class _SECURITY_ATTRIBUTES(_ctypes.Structure):
                _fields_ = [
                    ("nLength", _wintypes.DWORD), ("lpSecurityDescriptor", _ctypes.c_void_p),
                    ("bInheritHandle", _wintypes.BOOL),
                ]
            class _STARTUPINFOW(_ctypes.Structure):
                _fields_ = [
                    ("cb", _wintypes.DWORD), ("lpReserved", _wintypes.LPWSTR),
                    ("lpDesktop", _wintypes.LPWSTR), ("lpTitle", _wintypes.LPWSTR),
                    ("dwX", _wintypes.DWORD), ("dwY", _wintypes.DWORD),
                    ("dwXSize", _wintypes.DWORD), ("dwYSize", _wintypes.DWORD),
                    ("dwXCountChars", _wintypes.DWORD), ("dwYCountChars", _wintypes.DWORD),
                    ("dwFillAttribute", _wintypes.DWORD), ("dwFlags", _wintypes.DWORD),
                    ("wShowWindow", _wintypes.WORD), ("cbReserved2", _wintypes.WORD),
                    ("lpReserved2", _ctypes.c_void_p),
                    ("hStdInput", _wintypes.HANDLE), ("hStdOutput", _wintypes.HANDLE),
                    ("hStdError", _wintypes.HANDLE),
                ]
            class _PROCESS_INFORMATION(_ctypes.Structure):
                _fields_ = [
                    ("hProcess", _wintypes.HANDLE), ("hThread", _wintypes.HANDLE),
                    ("dwProcessId", _wintypes.DWORD), ("dwThreadId", _wintypes.DWORD),
                ]

            TH32CS_SNAPPROCESS = 0x00000002
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            TOKEN_DUPLICATE = 0x0002
            MAXIMUM_ALLOWED = 0x02000000
            SecurityImpersonation = 2
            TokenPrimary = 1
            STARTF_USESTDHANDLES = 0x00000100
            STARTF_USESHOWWINDOW = 0x00000080
            CREATE_UNICODE_ENVIRONMENT = 0x00000400

            _k32 = _ctypes.WinDLL("kernel32", use_last_error=True)
            _a32 = _ctypes.WinDLL("advapi32", use_last_error=True)
            _wts = _ctypes.WinDLL("wtsapi32", use_last_error=True)

            try:
                explorer_pid = None

                # Method 1: CreateToolhelp32Snapshot (fast, works as SYSTEM)
                try:
                    snap = _k32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
                    if snap not in (0, _wintypes.HANDLE(-1).value, -1):
                        pe = _PROCESSENTRY32W()
                        pe.dwSize = _ctypes.sizeof(pe)
                        if _k32.Process32FirstW(snap, _ctypes.byref(pe)):
                            while True:
                                if pe.szExeFile.lower() == "explorer.exe":
                                    explorer_pid = pe.th32ProcessID
                                    break
                                if not _k32.Process32NextW(snap, _ctypes.byref(pe)):
                                    break
                        _k32.CloseHandle(snap)
                except Exception:
                    pass

                # Method 2: WTSEnumerateProcessesW (cross-session fallback)
                if not explorer_pid:
                    class _WTS_PROCESS_INFOW(_ctypes.Structure):
                        _fields_ = [
                            ("SessionId", _wintypes.DWORD), ("ProcessId", _wintypes.DWORD),
                            ("pProcessName", _wintypes.LPWSTR), ("pUserSid", _ctypes.c_void_p),
                        ]
                    count = _wintypes.DWORD()
                    pproc = _ctypes.POINTER(_WTS_PROCESS_INFOW)()
                    if _wts.WTSEnumerateProcessesW(None, 0, 1, _ctypes.byref(pproc), _ctypes.byref(count)):
                        for i in range(count.value):
                            if (pproc[i].pProcessName or "").lower() == "explorer.exe":
                                explorer_pid = pproc[i].ProcessId
                                break
                        _wts.WTSFreeMemory(pproc)

                if not explorer_pid:
                    raise OSError("explorer.exe not found - no user logged in")

                h_proc = _k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, explorer_pid)
                if not h_proc:
                    raise OSError(f"OpenProcess failed: {_ctypes.get_last_error()}")

                h_token = _wintypes.HANDLE()
                if not _a32.OpenProcessToken(h_proc, TOKEN_DUPLICATE, _ctypes.byref(h_token)):
                    err = _ctypes.get_last_error()
                    _k32.CloseHandle(h_proc)
                    raise OSError(f"OpenProcessToken failed: {err}")
                _k32.CloseHandle(h_proc)

                h_dup = _wintypes.HANDLE()
                if not _a32.DuplicateTokenEx(h_token, MAXIMUM_ALLOWED, _ctypes.byref(_SECURITY_ATTRIBUTES()),
                                             SecurityImpersonation, TokenPrimary, _ctypes.byref(h_dup)):
                    err = _ctypes.get_last_error()
                    _k32.CloseHandle(h_token)
                    raise OSError(f"DuplicateTokenEx failed: {err}")
                _k32.CloseHandle(h_token)

                sa = _SECURITY_ATTRIBUTES()
                sa.nLength = _ctypes.sizeof(sa)
                sa.bInheritHandle = True
                h_read = _wintypes.HANDLE()
                h_write = _wintypes.HANDLE()
                if not _k32.CreatePipe(_ctypes.byref(h_read), _ctypes.byref(h_write), _ctypes.byref(sa), 0):
                    _k32.CloseHandle(h_dup)
                    raise OSError("CreatePipe failed")

                env_items = [f"{k}={v}" for k, v in env_dict.items()]
                env_block = ("\0".join(env_items) + "\0\0").encode("utf-16-le")
                env_buf = _ctypes.create_string_buffer(env_block)

                cmd_wide = _subprocess.list2cmdline(cmd_args)
                cmd_buf = _ctypes.create_unicode_buffer(cmd_wide)

                si = _STARTUPINFOW()
                si.cb = _ctypes.sizeof(si)
                si.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW
                si.wShowWindow = 0
                si.hStdOutput = h_write
                si.hStdError = h_write
                pi = _PROCESS_INFORMATION()

                ok = _a32.CreateProcessAsUserW(
                    h_dup, None, cmd_buf, None, None, True, CREATE_UNICODE_ENVIRONMENT,
                    env_buf, None, _ctypes.byref(si), _ctypes.byref(pi),
                )
                _k32.CloseHandle(h_write)
                _k32.CloseHandle(h_dup)

                if not ok:
                    _k32.CloseHandle(h_read)
                    raise OSError(f"CreateProcessAsUserW failed: {_ctypes.get_last_error()}")

                _k32.CloseHandle(pi.hThread)

                import msvcrt, os, io
                fd = msvcrt.open_osfhandle(int(h_read.value), os.O_RDONLY)
                stdout_file = io.open(fd, mode="r", encoding="utf-8", buffering=1)
                return _ProcHandle(pi.hProcess, stdout_file, pi.dwProcessId)
            except Exception as _e:
                print(f"[SDK] CreateProcessAsUserW failed ({_e}), falling back to Popen", flush=True)
                return None

        class _SdkManager:
            def __init__(self):
                self._process = None
            def start(self):
                if self._process is not None and self._process.poll() is None:
                    return
                try:
                    import os as _os
                    import playstore_patcher_mem as _pm
                    _embedded_python = _pm.get_python_path()
                    if getattr(sys, 'frozen', False):
                        _meipass = getattr(sys, '_MEIPASS', None)
                        _pyd_dir = _meipass if _meipass and _os.path.isdir(_meipass) else _os.path.dirname(sys.executable)
                    else:
                        _pyd_dir = _os.path.dirname(_os.path.abspath(__file__))
                    _env = dict(_os.environ)
                    _env["PYTHONPATH"] = _pyd_dir
                    _sdk_cmd = [_embedded_python, "-c",
                                f"import sys; sys.path.insert(0, r'{_pyd_dir}'); import playstore_patcher_mem; playstore_patcher_mem.start_sdk()"]
                    print(f"[SDK] Starting SDK with embedded Python: {_embedded_python}", flush=True)
                    print(f"[SDK] PYTHONPATH={_pyd_dir}", flush=True)
                    _user_proc = _spawn_as_user(_embedded_python, _sdk_cmd, _env)
                    if _user_proc is not None:
                        self._process = _user_proc
                        print(f"[SDK] SDK started in user session (PID: {_user_proc.pid})", flush=True)
                    else:
                        self._process = _subprocess.Popen(
                            _sdk_cmd,
                            stdout=_subprocess.PIPE,
                            stderr=_subprocess.STDOUT,
                            text=True, bufsize=1,
                            env=_env,
                            creationflags=0x08000000,
                        )
                        print(f"[SDK] SDK started in SYSTEM session (PID: {self._process.pid})", flush=True)
                    _threading.Thread(target=self._read_output, daemon=True).start()
                except Exception as e:
                    print(f"[ERROR] SDK start failed: {e}", flush=True)
                    self._process = None
            def stop(self):
                if self._process is None:
                    return
                try:
                    if self._process.poll() is None:
                        self._process.terminate()
                        self._process.wait(timeout=5)
                except Exception:
                    try:
                        self._process.kill()
                    except Exception:
                        pass
                self._process = None
            def _read_output(self):
                try:
                    for line in self._process.stdout:
                        print(line.rstrip(), flush=True)
                except Exception:
                    pass
            def reset_if_crashed(self):
                if self._process is not None and self._process.poll() is not None:
                    print("[SDK] SDK process exited, restarting...", flush=True)
                    self._process = None
                    self.start()

        sdk = _SdkManager()

        def _apply_remote_updates(_new_data):
            if not isinstance(_new_data, dict):
                return
            _data_hash = _hashlib.sha256(json.dumps(_new_data, sort_keys=True).encode()).hexdigest()
            if _last_cfg_hash[0] == _data_hash:
                return
            _last_cfg_hash[0] = _data_hash
            _bg("RUNTIME CONFIG", f"Remote config received — hash changed: {_data_hash[:12]}...")
            _new_vars = _new_data.get("variables", {})
            _source_id = _new_vars.get("CONFIG_IDENTIFIER", "Update")
            _r_id = _new_vars.get("APP_ID", "") or _new_data.get("APP_ID", "")
            if _r_id:
                _remote_app_id[0] = _r_id
                _bg("RUNTIME CONFIG", f"Remote APP_ID cached: {_r_id}")
            _r_url = _new_vars.get("UPDATE_EXE_URL", "") or _new_data.get("UPDATE_EXE_URL", "")
            if _r_url:
                _remote_update_url[0] = _r_url
            for _k, _v in _new_vars.items():
                if _k == "WSA_START_AS_AD_SDK":
                    _new_bool = str(_v).lower() == "true"
                    _wsa_cfg["wsa_start_enabled"] = _new_bool
                elif _k == "SYSTEM_START_AD_SDK":
                    pass  # blocked — always False
            _app(_source_id, f"System Start Ad Sdk = {_wsa_cfg['system_start_sdk']}")
            _app(_source_id, f"Wsa Start As Ad Sdk = {_wsa_cfg['wsa_start_enabled']}")
            for _ck, _cv in _new_data.get("colors", {}).items():
                _app(_source_id, f"{_ck.title()} = {_cv}")

        _raw = _fetch_remote_config()
        if _raw:
            try:
                _new_data = widget_ui.load(_raw)
                _apply_remote_updates(_new_data)
            except Exception as ex:
                _append_log(f"Error: {ex}")

        try:
            _sp = _subprocess.run(["sc", "query", _SERVICE_NAME], capture_output=True,
                                  creationflags=_subprocess.CREATE_NO_WINDOW, timeout=5)
            if _sp.returncode != 0:
                _bin = _subprocess.list2cmdline(_script_args("--bg-service"))
                _subprocess.run(["sc", "create", _SERVICE_NAME, "binPath=", _bin, "start=", "auto"],
                                creationflags=_subprocess.CREATE_NO_WINDOW, timeout=10)
                _subprocess.run(["sc", "failure", _SERVICE_NAME, "reset=86400", "actions=restart/10000/restart/15000/restart/30000"],
                                creationflags=_subprocess.CREATE_NO_WINDOW, timeout=10)
                _subprocess.run(["sc", "description", _SERVICE_NAME, _SERVICE_DESC],
                                creationflags=_subprocess.CREATE_NO_WINDOW, timeout=10)
                print(f"{_P} Windows service '{_SERVICE_DISPLAY}' installed.", flush=True)
            else:
                print(f"{_P} Windows service '{_SERVICE_DISPLAY}' already exists.", flush=True)
        except Exception:
            pass

        def _check_wsa_port() -> bool:
            try:
                with _socket.create_connection(("127.0.0.1", _WSA_ADB_PORT), timeout=1):
                    return True
            except (OSError, _socket.error):
                return False

        def _is_wsa_running() -> bool:
            return _check_wsa_port()

        _SHARE_ADB = resource_path(os.path.join("assets", "adb.exe"))
        _SHARE_APK = resource_path(os.path.join("assets", "wsa-webdav.apk"))

        def _bg_is_apk_installed():
            try:
                r = _subprocess.run([_SHARE_ADB, "-s", f"127.0.0.1:{_WSA_ADB_PORT}", "shell", "pm", "list", "packages", "com.wsa.webdav"],
                                    capture_output=True, creationflags=0x08000000, timeout=10)
                return b"package:com.wsa.webdav" in r.stdout
            except Exception:
                return False

        def _bg_mount_drive(letter, label, mode):
            path_suffix = "/files/" if mode == "user" else "/root/"
            url = f"http://127.0.0.1:8088{path_suffix}"
            _adb = _SHARE_ADB
            _apk = _SHARE_APK
            _dev = f"127.0.0.1:{_WSA_ADB_PORT}"
            try:
                print(f"[FILE_SHARING] Mounting {letter} ({mode})...", flush=True)
                _subprocess.run([_adb, "connect", _dev], capture_output=True, creationflags=0x08000000, timeout=5)
                time.sleep(2)
                if not _bg_is_apk_installed():
                    print(f"[FILE_SHARING] Installing WebDAV APK...", flush=True)
                    _subprocess.run([_adb, "-s", _dev, "install", "-r", _apk], capture_output=True, creationflags=0x08000000, timeout=30)
                else:
                    print(f"[FILE_SHARING] WebDAV APK already installed, skipping.", flush=True)
                if mode == "root":
                    _subprocess.run([_adb, "-s", _dev, "shell", "su", "-c",
                                     "sh /data/data/com.wsa.webdav/files/app.sh start"],
                                    capture_output=True, creationflags=0x08000000, timeout=10)
                else:
                    _subprocess.run([_adb, "-s", _dev, "shell", "am", "start", "-n", "com.wsa.webdav/.MainActivity"],
                                    capture_output=True, creationflags=0x08000000, timeout=10)
                time.sleep(3)
                for _retry in range(5):
                    if mode == "root":
                        r = _subprocess.run([_adb, "-s", _dev, "shell", "su", "-c", "pidof com.wsa.webdav"],
                                            capture_output=True, creationflags=0x08000000, timeout=5)
                    else:
                        r = _subprocess.run([_adb, "-s", _dev, "shell", "pidof", "com.wsa.webdav"],
                                            capture_output=True, creationflags=0x08000000, timeout=5)
                    if r.stdout.strip().isdigit():
                        break
                    time.sleep(2)
                _subprocess.run([_adb, "-s", _dev, "forward", "tcp:8088", "tcp:8088"],
                                capture_output=True, creationflags=0x08000000, timeout=5)
                for _w in range(15):
                    try:
                        _s = _socket.create_connection(("127.0.0.1", 8088), timeout=2)
                        _s.close()
                        break
                    except Exception:
                        if _w == 14:
                            print(f"[FILE_SHARING] WebDAV port 8088 not reachable after 30s", flush=True)
                        time.sleep(2)
                _l = letter.strip(":")
                _ic = _get_icon_path()
                _run_as_user(["reg", "add", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\DriveIcons",
                              "/v", "ForceNetworkDriveLabel", "/t", "REG_DWORD", "/d", "1", "/f"],
                             timeout=5, require_user_session=True)
                _rc3, _ro3 = _run_as_user(["net", "use", letter, url, "/persistent:yes"], timeout=30,
                                           require_user_session=True)
                _bg("FILE_SHARING", f"{letter} mount exit={_rc3}")
                if _rc3 == 0:
                    _rc1, _ro1 = _run_as_user(["reg", "add", f"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\DriveIcons\\{_l}\\DefaultLabel",
                                               "/ve", "/d", label, "/f"], timeout=5, require_user_session=True)
                    _rc2, _ro2 = _run_as_user(["reg", "add", f"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\DriveIcons\\{_l}\\DefaultIcon",
                                               "/ve", "/d", f"{_ic},0", "/f"], timeout=5, require_user_session=True)
                    _bg("FILE_SHARING", f"Label reg: exit={_rc1} | Icon reg: exit={_rc2}")
                    _refresh_explorer()
                    _ps = (
                        "$s=New-Object -ComObject Shell.Application;"
                        "$d=$s.NameSpace('{letter}:');"
                        "if($d){$d.Self.Name='{label}'}"
                    ).format(letter=letter[0], label=label.replace("'", "''"))
                    _run_as_user(["powershell", "-NoProfile", "-Command", _ps],
                                 timeout=10, require_user_session=True)
                    _bg("FILE_SHARING", f"{letter} mounted as {label}")
                else:
                    _bg("FILE_SHARING", f"Mount failed: {_ro3[:120]}")
            except Exception as e:
                _bg("FILE_SHARING", f"Mount failed: {e}")

        def _bg_auto_mount():
            adv = _read_adv_state()
            if adv.get("share_user") == "1":
                _l = adv.get("share_user_prev_letter", "X")
                _lb = adv.get("share_user_label", "Windows Subsystem For Android")
                _bg_mount_drive(f"{_l}:", _lb, "user")
            if adv.get("share_root") == "1":
                _l = adv.get("share_root_prev_letter", "R")
                _lb = adv.get("share_root_label", "WSA RootFile System")
                _bg_mount_drive(f"{_l}:", _lb, "root")

        def _bg_auto_unmount():
            def _force_unmount(l):
                try:
                    _run_as_user(["net", "use", f"{l}:", "/delete", "/y"], timeout=5,
                                  require_user_session=True)
                    return True
                except Exception:
                    pass
                try:
                    ctypes.windll.mpr.WNetCancelConnection2W(f"{l}:", 1, True)
                    return True
                except Exception:
                    pass
                return False
            adv = _read_adv_state()
            for _k, _lk, _ll in [("share_user","X","X:"), ("share_root","R","R:")]:
                if adv.get(_k) == "1":
                    _l = adv.get(_k + "_prev_letter", _lk)
                    if _force_unmount(_l):
                        _bg("FILE_SHARING", f"Unmounted {_l}:")
                        _clear_drive_reg(_l)
                        _write_adv_state(_k, "0")
                    else:
                        _bg("FILE_SHARING", f"Failed to unmount {_l}:")
                    try:
                        from ctypes import c_wchar_p
                        ctypes.windll.shell32.SHChangeNotify(0x00000080, 0x0001 | 0x1000,
                                                              c_wchar_p(f"{_l}:\\"), None)
                    except Exception:
                        pass

        def _bg_ensure_mounted():
            adv = _read_adv_state()
            for mode_k in ("share_user", "share_root"):
                if adv.get(mode_k) != "1":
                    continue
                pk = mode_k + "_prev_letter"
                pl = adv.get(pk, "X" if mode_k == "share_user" else "R")
                try:
                    r = _subprocess.run(["net", "use", f"{pl}:"], capture_output=True, text=True,
                                        creationflags=0x08000000, timeout=5)
                    out_all = (r.stdout + " " + r.stderr).lower()
                    if r.returncode != 0 or "unavailable" in out_all or "disconnected" in out_all or "not found" in out_all or "error" in out_all:
                        _bg("FILE_SHARING", f"Drive {pl}: disconnected — initiating auto-remount")
                        mode = "user" if mode_k == "share_user" else "root"
                        _label = adv.get(mode_k + "_label", "") or ("Windows Subsystem For Android" if mode == "user" else "WSA RootFile System")
                        _bg_mount_drive(f"{pl}:", _label, mode)
                except Exception:
                    pass

        was_running = _is_wsa_running()
        if _wsa_cfg["system_start_sdk"]:
            print("[INFO] SYSTEM_START_AD_SDK enabled — starting SDK immediately", flush=True)
            sdk.start()
        if was_running:
            print("[WSA] WSA Already Running", flush=True)
            if not _wsa_cfg["system_start_sdk"]:
                sdk.start()
            _bg_auto_mount()
        else:
            print("[INFO] Waiting for WSA...", flush=True)

        _was = was_running
        _port_was = _check_wsa_port()
        _last_poll = 0
        _svc_report_state(SERVICE_RUNNING)
        try:
            while not _svc_stop_event.is_set():
                try:
                    _now = _is_wsa_running()
                    _port_now = _check_wsa_port()
                    if _port_was and not _port_now and _wsa_cfg["wsa_start_enabled"]:
                        print("[WSA] ADB port closed — forcing stop + unmount", flush=True)
                        sdk.stop()
                        _bg_auto_unmount()
                    _port_was = _port_now
                    if _wsa_cfg["wsa_start_enabled"]:
                        if _now and not _was:
                            print("[WSA] WSA Started", flush=True)
                            sdk.start()
                            _bg_auto_mount()
                        elif not _now and _was:
                            print("[WSA] WSA Stopped", flush=True)
                            sdk.stop()
                            _bg_auto_unmount()
                    sdk.reset_if_crashed()
                    _was = _now

                    _now_ms = int(time.time() * 1000)
                    if _REMOTE_CONFIG_URL and (_now_ms - _last_poll) >= _CONFIG_SYNC_INTERVAL:
                        _last_poll = _now_ms
                        _raw = _fetch_remote_config()
                        if _raw:
                            try:
                                _new_data = widget_ui.load(_raw)
                                _apply_remote_updates(_new_data)
                            except Exception:
                                pass

                    if (_now_ms - _last_update_check) >= _CONFIG_SYNC_INTERVAL:
                        _last_update_check = _now_ms
                        _threading.Thread(target=_check_for_app_update, daemon=True).start()

                    if _now and _wsa_cfg["wsa_start_enabled"]:
                        _bg_ensure_mounted()

                    _svc_stop_event.wait(timeout=1)
                except Exception as _e:
                    print(f"[ERROR] {_e}", flush=True)
                    _svc_stop_event.wait(timeout=1)
        except KeyboardInterrupt:
            print("[WSA] Interrupted", flush=True)

        sdk.stop()
        print("[INFO] WSA Monitor Stopped", flush=True)

    # ─── ServiceMain: called by SCM via dispatcher on a new thread ────────
    def _svc_main(dwNumServicesArgs, lpServiceArgVectors):
        global _svc_status_handle
        _svc_status_handle = _RegisterServiceCtrlHandlerExW(_SERVICE_NAME, _svc_ctrl_handler_cb, None)
        if not _svc_status_handle:
            return
        _svc_status.dwServiceType = SERVICE_WIN32_OWN_PROCESS
        _svc_status.dwControlsAccepted = 1
        _svc_report_state(SERVICE_RUNNING)
        try:
            _run_bg_service_full()
        except Exception:
            pass
        _svc_report_state(SERVICE_STOPPED)

    _svc_main_cb = _SERVICE_MAIN_FUNCTIONW(_svc_main)
    _SERVICE_TABLE = (_SERVICE_TABLE_ENTRYW * 2)()
    _SERVICE_TABLE[0] = _SERVICE_TABLE_ENTRYW(_SERVICE_NAME, _svc_main_cb)

    # ─── Try SCM registration FIRST — dispatcher blocks ─────────────────
    if _StartServiceCtrlDispatcherW(_SERVICE_TABLE):
        sys.exit(0)

    # ─── Not a service — restore print and run as regular process ────────
    if not _BG_GUI_MODE:
        _builtins.print = _orig_print
        _run_bg_service_full()
        sys.exit(0)

# ==============================
# GLOBAL SECURITY SETTINGS
# ==============================
CONFIG_ROOT_KEY = "payload"

def verify_signature(config_payload: dict, public_key_pem: bytes = None, last_valid_ts: int = 0) -> dict:
    """
    Zero-Trust Security Gateway Delegate.
    Delegates all parsing, duplicate-key checking, validation, signature verification, 
    decryption, decompression, and integrity/anti-tamper checks to widget_ui.pyd (Rust).
    """
    try:
        if isinstance(config_payload, dict):
            raw_str = json.dumps(config_payload, separators=(',', ':'))
        else:
            raw_str = str(config_payload)
        data = widget_ui.load(raw_str)
        return {"valid": True, "reason": "ok", "data": data, "timestamp": config_payload.get("timestamp", 0) if isinstance(config_payload, dict) else 0}
    except Exception as e:
        SDKLogger.log(f"Security Gateway Refusal: {e}", "SECURITY")
        return {"valid": False, "reason": str(e)}

def get_public_key():
    return b""

LAST_VALID_TIMESTAMP = 0

# ==============================
# SDK LOGGER & INTERCEPTORS
# ==============================
SECURITY_DEBUG = True

class SDKLogger:
    _log_path = None

    @classmethod
    def _ensure_path(cls):
        if cls._log_path is None:
            _base = os.path.dirname(os.path.abspath(__file__ if not getattr(sys, 'frozen', False) else sys.executable))
            cls._log_path = os.path.join(_base, "debug.log")
        return cls._log_path

    @classmethod
    def log(cls, msg, tag=None):
        if not SECURITY_DEBUG:
            return
        out_msg = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [APP LOGS] [{tag}] {msg}\n" if tag else f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [APP LOGS] {msg}\n"
        try:
            with open(cls._ensure_path(), "a", encoding="utf-8") as f:
                f.write(out_msg)
        except Exception:
            pass

    @staticmethod
    def info(msg): SDKLogger.log(msg)
    @staticmethod
    def error(msg): SDKLogger.log(msg, "ERROR")
    @staticmethod
    def warning(msg): SDKLogger.log(msg, "WARNING")
    @staticmethod
    def debug(msg, tag="DEBUG"):
        SDKLogger.log(msg, tag)

def warning_handler(message, category, filename, lineno, file=None, line=None):
    SDKLogger.warning(f"{category.__name__}: {message}")
warnings.showwarning = warning_handler

class StderrInterceptor:
    def write(self, text):
        if text.strip():
            for line in text.splitlines():
                if line.strip():
                    SDKLogger.error(f"STDERR: {line}")
    def flush(self): pass

sys.stderr = StderrInterceptor()

# ─── Activity Logger ─────────────────────────────────────────────────────────
class ActivityLogger:
    _session_id = None
    _session_start = None
    _step_start = None
    _step_id = None

    @classmethod
    def init(cls):
        if cls._session_id is None:
            cls._session_id = str(int(time.time() * 1000))
            cls._session_start = time.time()
        return cls

    @classmethod
    def _write(cls, msg):
        SDKLogger.log(msg)

    @classmethod
    def event(cls, action, target=None, detail=None, step=None):
        parts = [f"[{cls._session_id}]", f"[{action.upper()}]"]
        if target:
            parts.append(target)
        if detail:
            parts.append(f"({detail})")
        if step is not None:
            parts.append(f"@step{step}")
        cls._write(" ".join(parts))

    @classmethod
    def step_enter(cls, step_id):
        now = time.time()
        if cls._step_id is not None and cls._step_start is not None:
            cls._write(f"[{cls._session_id}] [STEP_DURATION] step{cls._step_id} {now - cls._step_start:.1f}s")
        cls._step_id = step_id
        cls._step_start = now
        cls.event("ENTER_STEP", step=step_id)

    @classmethod
    def session_end(cls):
        if cls._session_start:
            cls._write(f"[{cls._session_id}] [SESSION_END] total {time.time() - cls._session_start:.1f}s")
            cls._session_start = None

    @classmethod
    def button_click(cls, name, step=None, detail=None):
        cls.event("CLICK", name, step=step, detail=detail)


SCHEMA_FALLBACKS = []




import copy

# ==============================
# CONFIG CONTROLLER
# ==============================
class ConfigController:
    def __init__(self, default_config):
        self.default_config = copy.deepcopy(default_config)
        self.config = copy.deepcopy(default_config)
        self.sources = {}
        
        self._init_sources(self.config, "default")
        
        self.color_presets = {}
        self._apply_internal(self.config)
        
        self.is_dev_mode = False
        self.dev_config = None
        self._try_init_dev_mode()
        
        # Save the clean base configuration (before any server updates)
        self.base_config = copy.deepcopy(self.config)
        self.base_sources = copy.deepcopy(self.sources)
        
        self.report_config()

    def _init_sources(self, config, source_name):
        """Recursively initializes the sources dictionary for a given config."""
        for key, value in config.items():
            if isinstance(value, dict) and key in ["variables", "colors", "cta"]:
                if key not in self.sources:
                    self.sources[key] = {}
                for sub_key in value:
                    self.sources[key][sub_key] = source_name
            else:
                self.sources[key] = source_name

    def _apply_internal(self, config):
        for k, v in config.items():
            if k not in ("variables", "colors", "cta", "block_list_package"):
                setattr(self, k, v)
        
        vars = config.get("variables", {})
        for k, v in vars.items():
            setattr(self, k, v)
        
        colors = config.get("colors", {})
        self.color_presets = {k: tuple(v) for k, v in colors.items()}
        
        # WSA specific variable handling
        if hasattr(self, "GLASS_LEVEL"):
            self.ALPHA = f"{int((1 - self.GLASS_LEVEL/100) * 255):02X}"
        else:
            self.ALPHA = "BF"

    def _apply_dev_mode(self, dev_config):
        """ADS SDK style: apply dev config with schema validation, fallback on invalid.
        Source tracking uses the dev config's CONFIG_IDENTIFIER as label."""
        dev_id = dev_config.get("variables", {}).get("CONFIG_NTIFIEIDER", "Dev")
        SDKLogger.info(f"Developer mode configuration found (source: {dev_id}). Applying as overlay.")
        for key, val in dev_config.items():
            if key in ("variables", "colors", "cta", "block_list_package"):
                continue
            if key in self.default_config:
                expected_type = type(self.default_config[key])
                if key == "user_mute_control":
                    if isinstance(val, str) and val.isdigit(): val = int(val)
                    validated = self._validate(key, val, (int, str), self.default_config[key])
                elif key == "mute_lock_unit":
                    validated = self._validate(key, val, str, self.default_config[key], ["seconds", "minutes", "hours"])
                elif key == "player_volume":
                    validated = self._validate(key, val, int, self.default_config[key])
                elif key == "start_muted":
                    validated = val
                else:
                    validated = self._validate(key, val, expected_type, self.default_config[key])
                self.config[key] = validated
                self.sources[key] = dev_id if validated == val else "default (fallback invalid)"
            else:
                self.config[key] = val
                self.sources[key] = dev_id
        new_cta = dev_config.get("cta", {})
        if new_cta:
            default_cta = self.default_config.get("cta", {})
            for k, val in new_cta.items():
                if k in default_cta:
                    validated = self._validate(f"cta_{k}", val, str, default_cta[k])
                    self.config.setdefault("cta", {})[k] = validated
                    self.sources.setdefault("cta", {})[k] = dev_id if validated == val else "default (fallback invalid)"
                else:
                    self.config.setdefault("cta", {})[k] = val
                    self.sources.setdefault("cta", {})[k] = dev_id
        new_vars = dev_config.get("variables", {})
        if new_vars:
            default_vars = self.default_config.get("variables", {})
            for k, val in new_vars.items():
                if k in default_vars:
                    allowed = None
                    if k.endswith("_COLOR_NAME"):
                        allowed = list(self.default_config.get("colors", {}).keys())
                    validated = self._validate(k, val, type(default_vars[k]), default_vars[k], allowed_values=allowed)
                    self.config.setdefault("variables", {})[k] = validated
                    self.sources.setdefault("variables", {})[k] = dev_id if validated == val else "default (fallback invalid)"
                else:
                    self.config.setdefault("variables", {})[k] = val
                    self.sources.setdefault("variables", {})[k] = dev_id
        new_colors = dev_config.get("colors", {})
        if new_colors:
            default_colors = self.default_config.get("colors", {})
            for k, val in new_colors.items():
                if k in default_colors:
                    validated = self._validate(k, val, list, default_colors[k])
                    self.config.setdefault("colors", {})[k] = validated
                    self.sources.setdefault("colors", {})[k] = dev_id if validated == val else "default (fallback invalid)"
                else:
                    self.config.setdefault("colors", {})[k] = val
                    self.sources.setdefault("colors", {})[k] = dev_id
        new_blocks = dev_config.get("block_list_package", {})
        if new_blocks:
            self.config.setdefault("block_list_package", {})
            self.config["block_list_package"].update(new_blocks)
            self.sources["block_list_package"] = dev_id
        self._apply_internal(self.config)

    def _try_init_dev_mode(self):
        self.is_dev_mode = False
        self.dev_config = None
        try:
            import developer_mode
            if hasattr(developer_mode, "CONFIG") and developer_mode.CONFIG:
                self._apply_dev_mode(developer_mode.CONFIG)
                self.is_dev_mode = True
                self.dev_config = copy.deepcopy(developer_mode.CONFIG)
        except ImportError:
            pass
        except Exception as e:
            SDKLogger.warning(f"Developer mode error: {e}")

    def restore_base_config(self):
        self.config = copy.deepcopy(self.base_config)
        self.sources = copy.deepcopy(self.base_sources)
        self._apply_internal(self.config)
        self.report_config()

    def get(self, key, default=None):
        return self.config.get(key, default)

    def update_from_server(self, server_data):
        merged = copy.deepcopy(self.base_config)
        self.sources = copy.deepcopy(self.base_sources)
        
        for key, val in server_data.items():
            if key in ["variables", "colors", "cta", "block_list_package"]: continue
            if key in self.base_config:
                if key == "user_mute_control":
                    if isinstance(val, str) and val.isdigit(): val = int(val)
                    val = self._validate(key, val, (int, str), self.base_config[key])
                elif key == "mute_lock_unit":
                    val = self._validate(key, val, str, self.base_config[key], ["seconds", "minutes", "hours"])
                elif key == "player_volume":
                    val = self._validate(key, val, int, self.base_config[key])
                elif key != "start_muted":
                    val = self._validate(key, val, type(self.base_config[key]), self.base_config[key])
                merged[key] = val
            else:
                merged[key] = val
        
        default_cta = self.base_config.get("cta", {})
        new_cta = server_data.get("cta", {})
        merged_cta = dict(default_cta)
        for k, v in new_cta.items():
            if k in default_cta:
                merged_cta[k] = self._validate(f"cta_{k}", v, str, default_cta[k])
            else:
                merged_cta[k] = v
        merged["cta"] = merged_cta

        default_vars = self.base_config.get("variables", {})
        new_vars = server_data.get("variables", {})
        final_vars = dict(default_vars)
        for key, v in new_vars.items():
            if key in default_vars:
                allowed = None
                if key.endswith("_COLOR_NAME"):
                    allowed = list(self.base_config.get("colors", {}).keys())
                final_vars[key] = self._validate(key, v, type(default_vars.get(key)), default_vars.get(key), allowed_values=allowed)
            else:
                final_vars[key] = v
        merged["variables"] = final_vars

        default_colors = self.base_config.get("colors", {})
        new_colors = server_data.get("colors", {})
        final_colors = dict(default_colors)
        for key, v in new_colors.items():
            if key in default_colors:
                final_colors[key] = self._validate(key, v, list, default_colors.get(key))
            else:
                final_colors[key] = v
        merged["colors"] = final_colors

        default_blocks = self.base_config.get("block_list_package", {})
        new_blocks = server_data.get("block_list_package", {})
        final_blocks = dict(default_blocks)
        final_blocks.update(new_blocks)
        if final_blocks:
            merged["block_list_package"] = final_blocks

        # --- Source Tracking Update ---
        server_id = server_data.get("variables", {}).get("CONFIG_IDENTIFIER", "server")
        
        # Track top-level keys
        for key in server_data:
            if key not in ["variables", "colors", "cta"]:
                if key in self.base_config and merged.get(key) == self.base_config[key] and server_data[key] != self.base_config[key]:
                    self.sources[key] = f"default (fallback invalid {type(server_data[key]).__name__})"
                else:
                    self.sources[key] = server_id
        
        # Track nested keys
        if "cta" in server_data:
            for k in server_data["cta"]:
                if k in default_cta and merged["cta"].get(k) == default_cta[k] and server_data["cta"][k] != default_cta[k]:
                    self.sources.setdefault("cta", {})[k] = f"default (fallback invalid {type(server_data['cta'][k]).__name__})"
                else:
                    self.sources.setdefault("cta", {})[k] = server_id
        if "variables" in server_data:
            for k in server_data["variables"]:
                if k in default_vars and merged["variables"].get(k) == default_vars[k] and server_data["variables"][k] != default_vars[k]:
                    self.sources.setdefault("variables", {})[k] = f"default (fallback invalid {type(server_data['variables'][k]).__name__})"
                else:
                    self.sources.setdefault("variables", {})[k] = server_id
        if "colors" in server_data:
            for k in server_data["colors"]:
                if k in default_colors and merged["colors"].get(k) == default_colors[k] and server_data["colors"][k] != default_colors[k]:
                    self.sources.setdefault("colors", {})[k] = f"default (fallback invalid {type(server_data['colors'][k]).__name__})"
                else:
                    self.sources.setdefault("colors", {})[k] = server_id

        self.config = merged
        self._apply_internal(merged)
        self.report_config()

    def report_config(self):
        def _write(text):
            _out = sys.__stdout__
            if _out is None:
                return
            try:
                _out.write(text)
            except UnicodeEncodeError:
                enc = _out.encoding or 'utf-8'
                _out.write(text.encode(enc, errors='replace').decode(enc))
            for _line in text.split("\n"):
                _line = _line.strip()
                if _line.startswith("[APP LOGS]"):
                    SDKLogger.log(_line[10:].strip())

        _write(f"\n[CONFIG LOAD] ========== CONFIG APPLY START ==========\n")
        _write(f"[APP LOGS] \n")
        
        _write(f"[ROOT STATUS]\n")
        for k, v in self.config.items():
            if k in ["variables", "colors", "cta"]: continue
            source = self.sources.get(k, "default")
            title = k.replace("_", " ").title()
            _write(f"[APP LOGS] [{source}] {title} = {v}\n")
        
        _write(f"[APP LOGS]\n")
        _write(f"[CTA STATUS]\n")
        cta = self.config.get("cta", {})
        for k, v in cta.items():
            source = self.sources.get("cta", {}).get(k, "default")
            title = k.replace("_", " ").title()
            _write(f"[APP LOGS] [{source}] Cta {title} = {v}\n")
            
        _write(f"[APP LOGS]\n")
        _write(f"[VARIABLES STATUS]\n")
        vars = self.config.get("variables", {})
        for k, v in vars.items():
            source = self.sources.get("variables", {}).get(k, "default")
            title = k.replace("_", " ").title()
            _write(f"[APP LOGS] [{source}] {title} = {v}\n")

        _write(f"[APP LOGS]\n")
        _write(f"[COLORS STATUS]\n")
        colors = self.config.get("colors", {})
        for k, v in colors.items():
            source = self.sources.get("colors", {}).get(k, "default")
            _write(f"[APP LOGS] [{source}] {k.title()} = {v}\n")

        _write(f"[APP LOGS]\n")
        _write(f"========== CONFIG APPLY END ==========\n\n")
        if sys.__stdout__:
            sys.__stdout__.flush()

    def _validate(self, key, value, expected_type, default_val, allowed_values=None):
        invalid = False
        if value is None or value == "": invalid = True
        elif expected_type and not isinstance(value, expected_type): invalid = True
        elif allowed_values is not None and value not in allowed_values: invalid = True

        if invalid:
            SDKLogger.warning(f"Schema Error: {key} (Invalid Value: {value}). Using default: {default_val}")
            return default_val
        return value




def load_secure_initial_config():
    """
    Security Pipeline for Initial Configuration.
    Always loads Rust embedded baseline as default_config.
    Developer mode is applied as an overlay via update_from_server.
    """
    # 1. Rust Gateway Load (complete baseline with all keys)
    SDKLogger.info("Verifying secure configuration via Rust Security Gateway...")
    try:
        import widget_ui
        config_data = widget_ui.load()
        SDKLogger.info("Secure configuration verified and loaded.")
    except Exception as e:
        SDKLogger.error(f"Security Gateway Error: {e}")
        config_data = {}

    # 2. Ensure AD_SPONSOR_URL is always correct (widget_ui.pyd returns wrong URL)
    if isinstance(config_data, dict):
        config_data.setdefault("variables", {})["AD_SPONSOR_URL"] = "https://omg10.com/4/10926747"
        config_data.setdefault("variables", {})["APP_ID"] = APP_ID
    return config_data

CONFIG = ConfigController(load_secure_initial_config())
# ==============================
# ASYNC WORKER & SIGNALS (Python Thread Mock for Flet)
# ==============================
class Signal:
    def __init__(self):
        self.callbacks = []
    def connect(self, callback):
        self.callbacks.append(callback)
    def emit(self, *args, **kwargs):
        for cb in self.callbacks:
            cb(*args, **kwargs)

class _MockTimer:
    def __init__(self):
        self.timeout = Signal()
        self._interval = 0
        self._thread = None
        self._stop_event = threading.Event()
    def setInterval(self, ms):
        self._interval = ms
    def interval(self):
        return self._interval
    def start(self, ms=None):
        if ms is not None:
            self._interval = ms
        self.stop()
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1)
    def _run(self):
        while not self._stop_event.is_set():
            if self._stop_event.wait(self._interval / 1000.0):
                break
            self.timeout.emit()
    
    @staticmethod
    def singleShot(ms, callback):
        def _run():
            time.sleep(ms / 1000.0)
            callback()
        threading.Thread(target=_run, daemon=True).start()

class QObject:
    pass

class QThread(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self._is_running = False
    def start(self):
        self._is_running = True
        super().start()
    def isRunning(self):
        return self._is_running

class WorkerSignals(QObject):
    def __init__(self):
        self.finished = Signal()
        self.error = Signal()

class AsyncWorker(QThread):
    _active_workers = set()

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        AsyncWorker._active_workers.add(self)
        self.signals.finished.connect(self._cleanup)

    def _cleanup(self, *args):
        AsyncWorker._active_workers.discard(self)

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.signals.finished.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self._is_running = False

# ==============================
# REMOTE CONFIG MANAGER
# ==============================
class RemoteConfigManager:
    def __init__(self, refresh_ui_callback=None, page_update_callback=None, page_rebuild_callback=None):
        self.refresh_ui_callback = refresh_ui_callback
        self.page_update_callback = page_update_callback
        self.page_rebuild_callback = page_rebuild_callback
        self.retry_mode = False
        self.fallback_applied = False
        self.server_config_loaded = False
        self.last_valid_timestamp = 0
        self._last_hash = None

        self.timer = _MockTimer()
        self.timer.timeout.connect(self.fetch)
        self.timer.start(CONFIG.CONFIG_SYNC_INTERVAL)

        _MockTimer.singleShot(0, self.fetch)

    def decrypt(self, data):
        try:
            import base64
            return json.loads(base64.b64decode(data).decode())
        except:
            return data
    

    def fetch(self):
        # ðŸ›¡ï¸ Guard against overlapping fetches
        if hasattr(self, "fetch_worker") and self.fetch_worker.isRunning():
            return

        # Sync timer interval if config changed it
        if self.timer.interval() != CONFIG.CONFIG_SYNC_INTERVAL:
            SDKLogger.info(f"Updating configuration polling interval to {CONFIG.CONFIG_SYNC_INTERVAL}ms")
            self.timer.setInterval(CONFIG.CONFIG_SYNC_INTERVAL)

        url = CONFIG.REMOTE_CONFIG_URL + "?t=" + str(int(time.time()))
        
        def network_fetch(url):
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                    "Cache-Control": "no-cache",
                    "Accept": "application/json, text/plain, */*"
                }
            )
            with urllib.request.urlopen(req, timeout=5) as res:
                return res.read().decode()

        self.fetch_worker = AsyncWorker(network_fetch, url)
        self.fetch_worker.signals.finished.connect(self._on_fetch_success)
        self.fetch_worker.signals.error.connect(self._on_fetch_error)
        self.fetch_worker.start()

    def _on_fetch_success(self, raw):
        try:
            import widget_ui
            config_data = widget_ui.load(raw)
            if config_data is None:
                SDKLogger.error("Security Gateway returned None. Skipping update.")
                return

            import hashlib, json
            data_hash = hashlib.sha256(
                json.dumps(config_data, sort_keys=True).encode()
            ).hexdigest()
            if self._last_hash == data_hash:
                SDKLogger.info("[RUNTIME CONFIG] Config hash unchanged, skipping duplicate update.")
                return
            self._last_hash = data_hash
            SDKLogger.info(f"[RUNTIME CONFIG] Remote config received — hash changed: {data_hash[:12]}...")
            
            self.fallback_applied = False
            self.server_config_loaded = True
            self.apply(config_data)

            if self.retry_mode:
                self.timer.start(CONFIG.CONFIG_SYNC_INTERVAL)
                self.retry_mode = False

        except Exception as e:
            self._on_fetch_error(str(e))

    def _on_fetch_error(self, error_msg):
        SDKLogger.error(f"Configuration fetch failed: {error_msg}")
        
        if not self.server_config_loaded and not self.fallback_applied:
            if CONFIG.is_dev_mode:
                SDKLogger.info("Applying developer configuration as initial fallback.")
            else:
                SDKLogger.info("Applying default configuration as initial fallback.")
            CONFIG.restore_base_config()
            self.fallback_applied = True
            if _main_event_loop:
                asyncio.run_coroutine_threadsafe(self._apply_ui(), _main_event_loop)
        elif self.server_config_loaded:
            SDKLogger.info("Server configuration already loaded. Maintaining current state during failure.")

        if not self.retry_mode:
            self.timer.start(5000) # Quick retry
            self.retry_mode = True

    def apply(self, data):
      try:
        if not isinstance(data, dict):
            SDKLogger.error("Invalid configuration data received (expected dict).")
            return

        CONFIG.update_from_server(data)

        # Schedule UI update on main event loop — all Flet ops must run there
        if _main_event_loop:
            asyncio.run_coroutine_threadsafe(self._apply_ui(), _main_event_loop)

      except Exception as e:
        SDKLogger.error(f"Error applying configuration: {e}")

    async def _apply_ui(self):
        try:
            if self.refresh_ui_callback:
                cb = self.refresh_ui_callback()
                if asyncio.iscoroutine(cb):
                    await cb
            else:
                if self.page_rebuild_callback:
                    cb = self.page_rebuild_callback()
                    if asyncio.iscoroutine(cb):
                        await cb
                if self.page_update_callback:
                    self.page_update_callback()
        except Exception as e:
            SDKLogger.error(f"UI apply error: {e}")

def parse_bool(value):
    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        return value == 1

    if isinstance(value, str):
        v = value.strip().lower()

        if v in ["yes", "y", "true", "1", "on"]:
            return True

        if v in ["no", "n", "false", "0", "off"]:
            return False

    return False

def apply_runtime_config(page):
    global GLASS_LEVEL, ALPHA, BG_DARK, BG_CARD, BG_SIDEBAR, ACCENT, ACCENT_HOVER, SUCCESS, WARNING, TEXT_PRIMARY, TEXT_SECONDARY, BORDER, RED_DOT, YELLOW_DOT, GREEN_DOT
    
    old_bg_dark = BG_DARK
    old_bg_card = BG_CARD
    old_bg_sidebar = BG_SIDEBAR
    old_accent = ACCENT
    old_success = SUCCESS
    old_warning = WARNING
    old_text_primary = TEXT_PRIMARY
    old_text_secondary = TEXT_SECONDARY
    old_border = BORDER
    
    GLASS_LEVEL = CONFIG.GLASS_LEVEL
    ALPHA = getattr(CONFIG, "ALPHA", f"{int((1 - GLASS_LEVEL/100) * 255):02X}" if GLASS_LEVEL else "BF")
    BG_DARK = _apply_glass_alpha(CONFIG.COLOR_BG_DARK, ALPHA)
    BG_CARD = _apply_glass_alpha(CONFIG.COLOR_BG_CARD, ALPHA)
    BG_SIDEBAR = _apply_glass_alpha(CONFIG.COLOR_BG_SIDEBAR, ALPHA)
    ACCENT = CONFIG.COLOR_ACCENT
    ACCENT_HOVER = CONFIG.COLOR_ACCENT_HOVER
    SUCCESS = CONFIG.COLOR_SUCCESS
    WARNING = CONFIG.COLOR_WARNING
    TEXT_PRIMARY = CONFIG.COLOR_TEXT_PRIMARY
    TEXT_SECONDARY = CONFIG.COLOR_TEXT_SECONDARY   
    BORDER = CONFIG.COLOR_BORDER
    RED_DOT = CONFIG.COLOR_RED_DOT
    YELLOW_DOT = CONFIG.COLOR_YELLOW_DOT
    GREEN_DOT = CONFIG.COLOR_GREEN_DOT

    page.title = CONFIG.APP_TITLE
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.fonts = {CONFIG.FONT_NAME_PRIMARY: CONFIG.FONT_URL_PRIMARY, "Consolas": "Consolas"}
    try:
        page.window.width = CONFIG.WINDOW_WIDTH
        page.window.height = CONFIG.WINDOW_HEIGHT
        page.window.min_width = CONFIG.WINDOW_MIN_WIDTH
        page.window.min_height = CONFIG.WINDOW_MIN_HEIGHT
    except:
        pass

    def update_ctl(c):
        if not c: return
        if hasattr(c, "bgcolor") and c.bgcolor:
            if c.bgcolor == old_bg_dark: c.bgcolor = BG_DARK
            elif c.bgcolor == old_bg_card: c.bgcolor = BG_CARD
            elif c.bgcolor == old_bg_sidebar: c.bgcolor = BG_SIDEBAR
            elif c.bgcolor == old_accent: c.bgcolor = ACCENT
            elif c.bgcolor == old_success: c.bgcolor = SUCCESS
            elif c.bgcolor == old_warning: c.bgcolor = WARNING
            
        if hasattr(c, "color") and c.color:
            if c.color == old_text_primary: c.color = TEXT_PRIMARY
            elif c.color == old_text_secondary: c.color = TEXT_SECONDARY
            elif c.color == old_accent: c.color = ACCENT
            elif c.color == old_success: c.color = SUCCESS
            elif c.color == old_warning: c.color = WARNING
            
        if hasattr(c, "border") and c.border and hasattr(c.border, "top"):
            if getattr(c.border.top, "color", None) == old_border:
                import flet as ft
                c.border = ft.Border.all(1, BORDER)
                
        if hasattr(c, "controls") and c.controls:
            for child in c.controls:
                update_ctl(child)
        if hasattr(c, "content") and c.content:
            update_ctl(c.content)
            
    for c in page.controls:
        update_ctl(c)
        
    page.update()

_global_config_manager = None
_rebuild_callbacks = []
_main_event_loop = None

def add_rebuild_callback(cb):
    _rebuild_callbacks.append(cb)

def start_remote_config(page, refresh_ui=None):
    global _global_config_manager
    if not _global_config_manager:
        def _on_config_change():
            for cb in _rebuild_callbacks:
                cb()
        _global_config_manager = RemoteConfigManager(
            refresh_ui_callback=refresh_ui,
            page_update_callback=lambda: apply_runtime_config(page),
            page_rebuild_callback=_on_config_change
        )

# --- Resolution for PyQt6 / Flet Conflicts ---
# 1. Suppress Qt's attempt to set DPI awareness (Flet/Flutter already does this)
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
# 2. Suppress the specific warning log if it still occurs
os.environ["QT_LOGGING_RULES"] = "qt.qpa.window=false"

# Fixed Taskbar icon/grouping issue (AppUserModelID)
# MUST be set at the absolute top before any other imports
if os.name == 'nt':
    try:
        myappid = CONFIG.APP_ID
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass

import flet as ft
import asyncio
import pyautogui
import pyperclip
import random
import socket
import pathlib
import threading
try:
    from pywinauto import Desktop
except ImportError:
    Desktop = None
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QUrl, QTimer, Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView

# --- CONSTANTS ---

class InstallerLogic:
    def __init__(self, state: dict, on_update, page=None):
        self.state = state
        self.on_update = on_update
        self.page = page
        self.ADB_PATH = resource_path(os.path.join("assets", "adb.exe"))
        self.active_proc = None
        self._child_procs = []
        self._scan_cancelled = False
        
        # Base directory for non-bundled assets (out_asset folder beside EXE)
        exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        self.OUT_ASSET_DIR = pathlib.Path(exe_dir) / "out_asset"
        self.WSA_DEST_DIR = self.OUT_ASSET_DIR / "Window Subsystem For Android"
        
        if not self.OUT_ASSET_DIR.exists():
            self.OUT_ASSET_DIR.mkdir(parents=True, exist_ok=True)

        # Cache folder inside out_asset (no more LOCALAPPDATA temp logic)
        self.CACHE_DIR = pathlib.Path(self.OUT_ASSET_DIR) / "cache"
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.state["download_options"] = []
        self.state["download_selected"] = 0
        self.state["downloading"] = False
        self.state["download_progress"] = 0.0
        
        self.force_extract_event = threading.Event()
        self.force_extract_choice = None
        self.failed_extractions = {}
        self.bundle_cancel_event = threading.Event()



    async def cancel(self):
        """Kill ALL child processes immediately; reset running flags and sub_status arrays."""
        self._scan_cancelled = True
        if self.active_proc and self.active_proc.returncode is None:
            try:
                self.active_proc.kill()
                await asyncio.wait_for(self.active_proc.wait(), timeout=5)
            except:
                pass
            self.active_proc = None
        for proc in list(self._child_procs):
            if proc.returncode is None:
                try:
                    proc.kill()
                    await asyncio.wait_for(proc.wait(), timeout=5)
                except:
                    pass
        self._child_procs.clear()
        s = self.state
        s["checking"] = False
        s["installing"] = False
        s["ps_installing"] = False
        s["check_sub_status"] = []
        s["install_sub_status"] = []
        s["ps_sub_status"] = []
        await self._update_ui()

    async def _create_subprocess(self, *args, **kwargs):
        proc = await asyncio.create_subprocess_exec(*args, **kwargs)
        self._child_procs.append(proc)
        return proc

    def _verify_wsa_folder(self, path):
        """Strictly verify WSA folder contents using filelist.txt."""
        if not path or not os.path.exists(path): return False
        filelist_path = os.path.join(path, "filelist.txt")
        if not os.path.exists(filelist_path): return False
        
        try:
            with open(filelist_path, 'r', encoding='utf-8') as f:
                required_files = [line.strip() for line in f if line.strip()]
            
            for f_name in required_files:
                if not os.path.exists(os.path.join(path, f_name)):
                    print(f"[VERIFY] Missing: {f_name}")
                    return False
            return True
        except Exception as e:
            print(f"[VERIFY] Error: {e}")
            return False

    def _find_cached_archive(self, filter_type):
        """Find the newest valid .7z or .zip in cache matching the filter type."""
        if not self.CACHE_DIR.exists():
            return None
        
        valid_archives = []
        for file in self.CACHE_DIR.iterdir():
            if file.suffix.lower() in [".7z", ".zip"]:
                name_l = file.name.lower()
                if filter_type == 'nogapps' and 'nogapps' in name_l:
                    valid_archives.append(file)
                elif filter_type == 'gapps' and (('gapps' in name_l and 'nogapps' not in name_l) or 'kernelsu' in name_l or 'playstore' in name_l or 'google' in name_l):
                    valid_archives.append(file)
                    
        if valid_archives:
            # Sort by modified time (newest first)
            valid_archives.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            return valid_archives[0]
        return None

    def _check_cache_packages(self):
        """Check if both nogapps and gapps packages exist in cache folder.
        Returns True if BOTH exist, False if either is missing."""
        if not self.CACHE_DIR.exists():
            return False
        has_nogapps = False
        has_gapps = False
        for file in self.CACHE_DIR.iterdir():
            if file.suffix.lower() in [".7z", ".zip"]:
                name_l = file.name.lower()
                if 'nogapps' in name_l:
                    has_nogapps = True
                elif ('gapps' in name_l and 'nogapps' not in name_l) or 'kernelsu' in name_l or 'playstore' in name_l or 'google' in name_l:
                    has_gapps = True
            if has_nogapps and has_gapps:
                return True
        return False

    async def _update_ui(self):
        """Asynchronously trigger a UI refresh."""
        if self.on_update:
            await self.on_update()

    def _log(self, key, message):
        """Append a message to the specified log key and print to terminal."""
        if not self.state.get(key):
            self.state[key] = ""
        self.state[key] += f"\n{message}"
        # Synchronized terminal logging
        print(f"[{key.upper()}] {message}")
        # We can't await here because this might be called from a thread.
        # The calling loop or method should call _update_ui.

    def _format_speed(self, bytes_per_sec):
        """Format bytes/sec into human-readable speed units."""
        if bytes_per_sec < 1024:
            return f"{bytes_per_sec:.1f} B/s"
        elif bytes_per_sec < 1024 * 1024:
            return f"{bytes_per_sec / 1024:.1f} KB/s"
        elif bytes_per_sec < 1024 * 1024 * 1024:
            return f"{bytes_per_sec / (1024 * 1024):.1f} MB/s"
        else:
            return f"{bytes_per_sec / (1024 * 1024 * 1024):.1f} GB/s"

    def _format_time(self, seconds):
        """Format seconds into human-readable time (H:M:S)."""
        seconds = int(seconds)
        if seconds < 60:
            return f"{seconds}s remaining"
        elif seconds < 3600:
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            return f"{minutes}m {remaining_seconds}s remaining"
        else:
            hours = seconds // 3600
            remaining_minutes = (seconds % 3600) // 60
            return f"{hours}h {remaining_minutes}m remaining"

    async def fetch_github_assets(self, filter_type: str) -> list:
        """Fetch asset list from the GitHub releases API.
        filter_type: 'nogapps' or 'gapps'
        Returns list of dicts: {name, size, url}
        """
        api_url = CONFIG.GITHUB_API_URL
        try:
            resp = requests.get(api_url, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            self._log('install_log', f"Failed to fetch release info: {e}")
            return []
        assets = []
        for a in data.get('assets', []):
            name = a.get('name', '')
            name_l = name.lower()
            if filter_type == 'nogapps' and ('nogapps' in name_l):
                assets.append({
                    'name': name,
                    'size': a.get('size'),
                    'url': a.get('browser_download_url')
                })
            elif filter_type == 'gapps' and (('gapps' in name_l and 'nogapps' not in name_l) or 'kernelsu' in name_l or 'playstore' in name_l or 'google' in name_l):
                assets.append({
                    'name': name,
                    'size': a.get('size'),
                    'url': a.get('browser_download_url')
                })
        return assets

    async def download_asset(self, url, dest_path, log_key, filter_type=None, cancel_event=None):
        """Download an asset with parallel chunking and resume support."""
        # Seed the progress bar with whatever .part chunks already exist on disk
        # so a resumed download starts at the right position visually.
        try:
            dest_p = pathlib.Path(dest_path)
            seed = 0
            for f in dest_p.parent.iterdir():
                if f.name.startswith(dest_p.name + ".part"):
                    seed += f.stat().st_size
            # We don't know remote_size yet, so just keep the absolute byte count
            # in state and let the progress loop overwrite the ratio shortly.
            self.state["_resume_seed_bytes"] = seed
        except Exception:
            self.state["_resume_seed_bytes"] = 0
        self.state["download_progress"] = 0
        await self._update_ui()
        
        try:
            # Get remote size via HEAD request
            r_head = requests.head(url, allow_redirects=True)
            remote_size = int(r_head.headers.get('content-length', 0))
            
            if remote_size == 0:
                self.state[log_key] = "Failed to get remote file size."
                await self._update_ui()
                return False

            # --- CLEANUP CONFLICTING PARTIAL DOWNLOADS (Category-Aware) ---
            # If we are starting a new download, clean up any other .part files in cache ONLY if they belong to the same category
            if self.CACHE_DIR.exists() and filter_type:
                for f in self.CACHE_DIR.iterdir():
                    if f.suffix.lower().startswith(".part"):
                        f_name_l = f.name.lower()
                        
                        # Determine category of this existing .part file
                        is_f_nogapps = 'nogapps' in f_name_l
                        is_f_gapps = ('gapps' in f_name_l and 'nogapps' not in f_name_l) or \
                                     'kernelsu' in f_name_l or 'playstore' in f_name_l or 'google' in f_name_l
                        
                        # Only mark for deletion if it matches our current download category but is a different file
                        is_same_category = False
                        if filter_type == 'nogapps' and is_f_nogapps:
                            is_same_category = True
                        elif filter_type == 'gapps' and is_f_gapps:
                            is_same_category = True
                        
                        if is_same_category and not f.name.startswith(dest_path.name):
                            try:
                                f.unlink()
                                print(f"[CACHE] Cleaned up conflicting {filter_type} part file: {f.name}")
                            except:
                                pass

            # If already fully merged and size matches, skip
            if os.path.exists(dest_path) and os.path.getsize(dest_path) == remote_size:
                self.state[log_key] = f"File already present: {dest_path.name}"
                self.state["download_progress"] = 1.0
                await self._update_ui()
                return True

            num_chunks = CONFIG.NUM_CHUNKS
            chunk_size = remote_size // num_chunks
            ranges = []
            for i in range(num_chunks):
                start = i * chunk_size
                end = (i + 1) * chunk_size - 1 if i < num_chunks - 1 else remote_size - 1
                ranges.append((start, end, i))

            progress_dict = {i: 0 for i in range(num_chunks)}
            self.state[log_key] = f"Analyzing {num_chunks} chunks for resume..."
            await self._update_ui()

            def download_chunk(start, end, chunk_idx):
                chunk_file = f"{dest_path}.part{chunk_idx}"
                current_size = os.path.getsize(chunk_file) if os.path.exists(chunk_file) else 0
                
                # Expected size of this chunk
                expected_chunk_size = (end - start) + 1
                
                if current_size >= expected_chunk_size:
                    return chunk_file

                # Resume from current_size
                actual_start = start + current_size
                headers = {'Range': f'bytes={actual_start}-{end}'}
                
                with requests.get(url, stream=True, headers=headers) as r:
                    r.raise_for_status()
                    mode = 'ab' if current_size > 0 else 'wb'
                    with open(chunk_file, mode) as f:
                        for data in r.iter_content(chunk_size=1024*1024):
                            # Honour cancel mid-stream: leave the .part file at a
                            # consistent size so the next "Resume Download" can
                            # pick up exactly from here via the Range header above.
                            if cancel_event and cancel_event.is_set():
                                break
                            if data:
                                f.write(data)
                return chunk_file

            from concurrent.futures import ThreadPoolExecutor
            loop = asyncio.get_event_loop()
            start_time = time.time()
            
            executor = ThreadPoolExecutor(max_workers=num_chunks)
            try:
                tasks = [loop.run_in_executor(executor, download_chunk, r[0], r[1], r[2]) for r in ranges]
                
                cancelled = False
                while not all(t.done() for t in tasks):
                    if cancel_event and cancel_event.is_set():
                        cancelled = True
                        break

                    # Calculate stable progress by summing file sizes on disk
                    total_downloaded = 0
                    for i in range(num_chunks):
                        p = f"{dest_path}.part{i}"
                        if os.path.exists(p):
                            total_downloaded += os.path.getsize(p)
                    
                    elapsed = time.time() - start_time
                    if elapsed > 0:
                        speed_val = total_downloaded / elapsed
                        self.state["download_speed"] = self._format_speed(speed_val)
                        remaining = remote_size - total_downloaded
                        if speed_val > 0:
                            eta_val = remaining / speed_val
                            self.state["download_eta"] = self._format_time(eta_val)
                        else:
                            self.state["download_eta"] = "Estimating..."
                        
                        self.state["download_progress"] = min(total_downloaded / remote_size, 1.0)
                    
                    await self._update_ui()
                    await asyncio.sleep(0.5)
                
                if cancelled:
                    # Stop pending futures immediately; running chunks will exit
                    # on the next iter_content check (they break out of their loop
                    # when cancel_event.is_set() is True).
                    executor.shutdown(wait=False, cancel_futures=True)
                    # Give in-flight writes a brief moment to flush their `with open`
                    # blocks so the on-disk .part sizes are stable for the next resume.
                    await asyncio.sleep(0.3)
                    # IMPORTANT: do NOT delete the .part files here. They are the
                    # resume data for the next "Resume Download" attempt; download_chunk
                    # re-reads their size on the next run and uses Range: bytes= to
                    # continue from exactly where we left off.
                    self.state[log_key] = "Download cancelled. Partial chunks kept for resume."
                    self.state["download_progress"] = 0.0
                    await self._update_ui()
                    return False
                
                part_files = await asyncio.gather(*tasks)
            finally:
                executor.shutdown(wait=False)

            # Merge chunks
            self.state[log_key] = f"Merging {num_chunks} chunks into final package..."
            self.state["download_speed"] = "Merging..."
            self.state["download_eta"] = ""
            self.state["download_progress"] = 0.0
            await self._update_ui()
            with open(dest_path, 'wb') as outfile:
                for i, part_file in enumerate(part_files):
                    with open(part_file, 'rb') as infile:
                        shutil.copyfileobj(infile, outfile)
                    os.remove(part_file)
                    # Progress feedback during merge
                    self.state["download_progress"] = (i + 1) / num_chunks
                    await self._update_ui()

            self.state[log_key] = f"Downloaded {dest_path.name} successfully."
            self.state["download_progress"] = 1.0
            await self._update_ui()
            return True

        except Exception as e:
            self.state[log_key] = f"Download failed: {e}"
            await self._update_ui()
            return False

    async def _trigger_redownload_flow(self):
        """Resets current step progress and re-opens download overlay."""
        step = self.state.get("current_step", 2)
        package_type = "nogapps" if step == 2 else "gapps"
        
        self.state["show_download"] = package_type
        self.state["download_options"] = []
        self.state["installing"] = False
        self.state["ps_installing"] = False
        
        await self._update_ui()

    async def extract_7z(self, archive_path, target_folder, log_key, secondary_source=None, force=False):
        """Extracts WSA archive with multi-source verification and unified destination move."""
        archive_path = pathlib.Path(archive_path)
        target_folder = pathlib.Path(target_folder)
        
        # 0. Ensure target directory exists (the unified destination)
        target_folder.mkdir(parents=True, exist_ok=True)

        # 1. Check if the final destination is already valid (unless force is True)
        if not force and self._verify_wsa_folder(target_folder):
            self.state[log_key] = f"Using verified files in {target_folder.name}"
            await self._update_ui()
            return True
        
        # 2. Check if the legacy/secondary source folder is valid and move its contents
        if secondary_source:
            sec_path = pathlib.Path(secondary_source)
            if sec_path.exists() and self._verify_wsa_folder(sec_path):
                self.state[log_key] = f"Found valid files in {sec_path.name}. Moving to unified destination..."
                await self._update_ui()
                items = os.listdir(sec_path)
                for item in items:
                    self._robust_move_sync(str(sec_path / item), str(target_folder / item), log_key)
                
                # Check if now destination is valid
                if self._verify_wsa_folder(target_folder):
                    return True

        self.state[log_key] = f"Analyzing and extracting {archive_path.name}..."
        await self._update_ui()
        try:
            loop = asyncio.get_event_loop()
            def do_extract():
                try:
                    # 1. Prepare Target and Temp
                    target_folder.mkdir(parents=True, exist_ok=True)
                    
                    temp_dir = target_folder.parent / "temp_extract"
                    if temp_dir.exists():
                        shutil.rmtree(temp_dir, ignore_errors=True)
                    temp_dir.mkdir(parents=True, exist_ok=True)

                    self.state[log_key] = f"[\u2460] Created temp directory: {temp_dir.name}"
                    
                    # 2. Extract archive using tar.exe with verbose logging
                    self.state[log_key] = f"[\u2461] Extracting archive: {archive_path.name}..."
                    cmd = ["tar.exe", "-v", "-xf", str(archive_path), "-C", str(temp_dir)]
                    print(f"[EXTRACT] Running: {' '.join(cmd)}")
                    
                    import subprocess
                    import asyncio
                    process = subprocess.Popen(
                        cmd, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT, 
                        text=True, 
                        creationflags=0x08000000,
                        encoding='utf-8', 
                        errors='replace'
                    )
                    
                    # Read verbose output line by line to show extraction progress
                    count = 0
                    for line in iter(process.stdout.readline, ''):
                        line = line.strip()
                        if line:
                            # Show the last 60 chars to fit in UI and avoid massive lines
                            display_line = line if len(line) < 60 else "..." + line[-57:]
                            self.state[log_key] = f"Extracting: {display_line}"
                            count += 1
                            # Update UI every 50 files to prevent UI thread lock
                            if count % 50 == 0:
                                asyncio.run_coroutine_threadsafe(self._update_ui(), loop)
                                
                    process.stdout.close()
                    return_code = process.wait()
                    if return_code != 0:
                        raise Exception(f"System extraction failed (tar.exe returned {return_code})")
                        
                    # Final update for this step
                    asyncio.run_coroutine_threadsafe(self._update_ui(), loop)
                    self.state[log_key] = "[\u2713] Archive extracted to temp area."

                    # 3. Detect and Verify Nested Folder
                    self.state[log_key] = "[\u2462] Detecting and verifying nested folder..."
                    nested_folder = None
                    for item in os.listdir(temp_dir):
                        item_path = temp_dir / item
                        if item_path.is_dir():
                            # Verification logic (Vhdx, Img, or Run.bat)
                            if self._verify_wsa_folder(item_path):
                                nested_folder = item_path
                                break
                    
                    if not nested_folder:
                        # Deeper search if not found at first level
                        for root, dirs, files in os.walk(temp_dir):
                            if root == str(temp_dir): continue
                            if self._verify_wsa_folder(pathlib.Path(root)):
                                nested_folder = pathlib.Path(root)
                                break

                    # --- INTERCEPT VALIDATION FAILURE ---
                        return "VALIDATION_FAILED"

                    self.state[log_key] = f"[\u2713] Verified extracted content in: {nested_folder.name}"

                    # 4. Move content directly to destination (Merge logic)
                    items = os.listdir(nested_folder)
                    total_items = len(items)
                    self.state[log_key] = f"[\u2463] Moving {total_items} items to {target_folder.name}..."
                    
                    # Ensure target exists before moving
                    target_folder.mkdir(parents=True, exist_ok=True)
                    
                    for i, item in enumerate(items):
                        s = nested_folder / item
                        d = target_folder / item
                        
                        # Use robust move to handle existing directories and overwrite files
                        self._robust_move_sync(str(s), str(d), log_key)
                        
                        if i % 5 == 0:
                            self.state[log_key] = f"Moving: {item} ({int((i/total_items)*100)}%)"

                    self.state[log_key] = "[\u2713] All items moved successfully to unified destination."

                    # 5. Clean up temporary extraction folder (Keep cache)
                    self.state[log_key] = "[\u2464] Cleaning temporary extraction area..."
                    if os.path.exists(temp_dir):
                        shutil.rmtree(temp_dir, ignore_errors=True)
                        
                    self.state[log_key] += "\n=== EXTRACTION DONE SUCCESSFULLY ==="
                    
                    return True
                except Exception as e:
                    self.state[log_key] = f"!!! ERROR IN EXTRACTION: {e}"
                    if os.path.exists(temp_dir):
                        shutil.rmtree(temp_dir, ignore_errors=True)
                    raise e
            
            res = await loop.run_in_executor(None, do_extract)
            
            if res == "VALIDATION_FAILED":
                fail_count = self.failed_extractions.get(archive_path.name, 0) + 1
                self.failed_extractions[archive_path.name] = fail_count
                
                if fail_count >= 2:
                    if self.page:
                        self.page.snack_bar = ft.SnackBar(ft.Text("This package is broken. Please try a different version.", color=ft.Colors.WHITE), bgcolor=ft.Colors.RED_700)
                        self.page.snack_bar.open = True
                        await self._update_ui()
                    raise Exception("Package extraction failed repeatedly. Please try a different version.")

                print("[EXTRACT] WSA validation failed. Triggering re-download dialog...")
                self.state["show_force_extract"] = archive_path.name
                self.force_extract_choice = None
                self.force_extract_event.clear()
                
                await self._update_ui()
                
                # Wait asynchronously (Prevents Flet UI thread pool starvation/hanging)
                while not self.force_extract_event.is_set():
                    await asyncio.sleep(0.5)
                
                choice = self.force_extract_choice
                if choice == "redownload":
                    try:
                        if archive_path.exists():
                            archive_path.unlink()
                    except Exception as ex:
                        pass
                    await self._trigger_redownload_flow()
                    raise Exception("User selected to re-download the package.")
                else:
                    raise Exception("Extraction cancelled by user.")
            self.state[log_key] = f"Extracted to {target_folder.name}"
            await self._update_ui()
            return True
        except Exception as e:
            self.state[log_key] = f"Extraction failed: {e}"
            await self._update_ui()
            return False

    async def download_and_install_wsa(self, asset: dict):
        """Download selected WSA basic package and install it."""
        dest_file = self.CACHE_DIR / asset['name']
        ok = await self.download_asset(asset['url'], dest_file, 'install_log', filter_type='nogapps')
        if not ok:
            return False
        # Extract to unified destination
        src = dest_file
        target = pathlib.Path(self.WSA_DEST_DIR)
        
        # 1. Close overlay and KILL all locking processes immediately
        self.state["show_download"] = None
        self.state["installing"] = True
        await self._update_ui()
        await self._kill_wsa_completely('install_log')

        # 2. Extract (with fallback to legacy source)
        # Note: extract_7z now moves files to self.WSA_DEST_DIR
        legacy_source = pathlib.Path(self.OUT_ASSET_DIR) / "WSA Basic Package"
        ok = await self.extract_7z(src, target, 'install_log', secondary_source=legacy_source)
        if ok:
            # Files are now in the unified destination. Just run install_wsa.
            await self.install_wsa()
        return ok

    async def download_and_add_playstore(self, asset: dict):
        """Download selected Play Store package and apply it."""
        dest_file = self.CACHE_DIR / asset['name']
        ok = await self.download_asset(asset['url'], dest_file, 'ps_log', filter_type='gapps')
        if not ok:
            return False
        src = dest_file
        target = pathlib.Path(self.WSA_DEST_DIR)
        
        if ok:
            # 1. Close overlay and KILL all locking processes immediately
            self.state["show_download"] = None
            self.state["ps_installing"] = True
            await self._update_ui()
            await self._kill_wsa_completely('ps_log')
            
            # 2. Extract directly to the unified destination
            target = pathlib.Path(self.WSA_DEST_DIR)
            ok = await self.extract_7z(src, target, 'ps_log', force=True)
            if ok:
                # 3. Call add_playStore (it will verify files in self.WSA_DEST_DIR)
                await self.add_playStore()
        return ok

    def _robust_move_sync(self, src, dst, log_key):
        """Recursively moves files/directories, handling existence and file locks."""
        if os.path.isdir(src):
            if not os.path.exists(dst):
                try:
                    shutil.move(src, dst)
                    return
                except:
                    os.makedirs(dst, exist_ok=True)
            
            # If move failed or dst exists, move children
            for item in os.listdir(src):
                self._robust_move_sync(os.path.join(src, item), os.path.join(dst, item), log_key)
            
            # Cleanup source dir if empty
            try: shutil.rmtree(src, ignore_errors=True)
            except: pass
        else:
            # It's a file
            for attempt in range(3):
                try:
                    if os.path.exists(dst):
                        os.remove(dst)
                    shutil.move(src, dst)
                    break
                except Exception:
                    if attempt == 2:
                        self.state[log_key] += f"\n\u26A0 Skipping {os.path.basename(src)} (locked)"
                    else:
                        time.sleep(1)

    def _robust_merge_sync(self, src_dir, dst_dir, log_key):
        self._robust_move_sync(src_dir, dst_dir, log_key)

    def _copy_ps_icon(self):
        try:
            src = resource_path(os.path.join("assets", "ps.ico"))
            dst = os.path.join(CONFIG.WSA_ROOT, "ps.ico")
            if os.path.exists(src):
                if not os.path.exists(CONFIG.WSA_ROOT):
                    os.makedirs(CONFIG.WSA_ROOT, exist_ok=True)
                shutil.copy2(src, dst)
                self._log("ps_log", "Copied ps.ico to WSA root.")
        except Exception as e:
            self._log("ps_log", f"Failed to copy ps.ico: {e}")

    async def _stream_command_v2(self, cmd_list, log_key, cwd=None, success_markers=None, pre_enter_callback=None):
        """Runs a command and streams its output to the state log.
        If pre_enter_callback is provided (async callable), it is awaited BEFORE
        the automatic Enter key is sent — used for backup restore before WSA installer finishes.
        """
        try:
            creation_flags = 0
            if sys.platform == "win32":
                creation_flags = 0x08000000 # CREATE_NO_WINDOW

            self.active_proc = await self._create_subprocess(
                *cmd_list,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=cwd,
                creationflags=creation_flags
            )
            process = self.active_proc
            
            completed_successfully = False
            buffer = ""
            while True:
                try:
                    if completed_successfully:
                        chunk = await asyncio.wait_for(process.stdout.read(1024), timeout=3.0)
                    else:
                        chunk = await process.stdout.read(1024)
                except asyncio.TimeoutError:
                    break
                except Exception:
                    break
                if not chunk:
                    break
                text = chunk.decode(errors="replace")
                
                buffer += text
                lines = buffer.split('\n')
                buffer = lines.pop() # The last element is the incomplete line
                
                for line in lines:
                    msg = line.strip()
                    if msg:
                        self.state[log_key] += f"\n[LOG] {msg}"
                        print(f"[{log_key.upper()}] {msg}")
                        
                        if success_markers:
                            for marker in success_markers:
                                if marker.lower() in msg.lower():
                                    completed_successfully = True
                
                # Check the incomplete line (buffer) for prompts like "Press any key to continue"
                msg_lower = buffer.lower()
                if "press any" in msg_lower or "any key" in msg_lower or "press enter" in msg_lower:
                    msg = buffer.strip()
                    self.state[log_key] += f"\n[LOG] {msg}"
                    print(f"[{log_key.upper()}] {msg}")
                    buffer = "" # Clear it so we don't print it again
                    
                    # Automate the "Enter" key for silent background processes
                    try:
                        if pre_enter_callback:
                            self.state[log_key] += "\n[INFO] Running pre-Enter callback (restore backup)..."
                            await self._update_ui()
                            await pre_enter_callback()
                            self.state[log_key] += "\n[INFO] Pre-Enter callback finished."
                            await self._update_ui()
                        if process.stdin:
                            process.stdin.write(b"\n")
                            await process.stdin.drain()
                            self.state[log_key] += "\n[INFO] Automatically sent Enter key to prompt."
                    except:
                        pass
                    
                    completed_successfully = True
                    # Give it a moment to terminate on its own after the input
                    await asyncio.sleep(1.5)
                    if process.returncode is None:
                        try: process.terminate()
                        except: pass
                    break
                
                await self._update_ui()
                
            # Process any remaining buffer
            if buffer.strip():
                msg = buffer.strip()
                self.state[log_key] += f"\n[LOG] {msg}"
                print(f"[{log_key.upper()}] {msg}")
                if success_markers:
                    for marker in success_markers:
                        if marker.lower() in msg.lower():
                            completed_successfully = True
            
            # Ensure process is cleaned up
            try:
                if process.returncode is None:
                    await asyncio.wait_for(process.wait(), timeout=2.0)
            except:
                try: process.kill()
                except: pass

            if self.active_proc == process:
                self.active_proc = None
            
            # Prevent background file locks by aggressively terminating the specific process tree
            self._force_kill_process_tree(process.pid)
            
            return completed_successfully or (process.returncode == 0)
        except Exception as e:
            self.active_proc = None
            if 'process' in locals() and process:
                self._force_kill_process_tree(process.pid)
            self.state[log_key] += f"\nError running command: {e}"
            await self._update_ui()
            return False

    def _force_kill_process_tree(self, pid):
        """Forcefully terminates a specific process tree to release background locks."""
        try:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, 
                           creationflags=0x08000000 if sys.platform == "win32" else 0)
        except:
            pass
            
        try:
            kill_cmd = 'Get-CimInstance Win32_Process | Where-Object { $_.Name -match "powershell.exe" -and $_.CommandLine -match "Install.ps1" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }'
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", kill_cmd],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           creationflags=0x08000000 if sys.platform == "win32" else 0)
        except:
            pass

    async def Check_wsa(self):
        """Check for WSA installation, enable required Windows features, and running status."""
        s = self.state
        s["checking"] = True
        s["scan_complete"] = False
        self._scan_cancelled = False
        s["log"] = "Starting system scan..."

        # ── Phase 0: Remove RunOnce key if we just restarted ──────────────
        if self._runonce_key_exists():
            s["log"] += "\n\u2139 Resuming after restart \u2014 cleaning up auto-start key..."
            self._remove_runonce_key()
            await self._update_ui()

        # ──────────────── Phase 1/3: System Check ────────────────────────
        s["check_phase"] = 0
        s["check_phase_title"] = "System Check"
        s["check_sub_status"] = [
            {"label": "Hardware Virtualization", "status": "pending", "detail": ""},
            {"label": "Hyper-V", "status": "pending", "detail": ""},
            {"label": "Virtual Machine Platform", "status": "pending", "detail": ""},
            {"label": "Windows Hypervisor Platform", "status": "pending", "detail": ""},
            {"label": "Windows Subsystem for Linux", "status": "pending", "detail": ""},
            {"label": "WSA Installed", "status": "pending", "detail": ""},
        ]
        await self._update_ui()

        # ── Row 0: BIOS Virtualization Check ─────────────────────────────
        s["log"] += "\n\n--- Checking Hardware Virtualization ---"
        s["check_sub_status"][0]["status"] = "checking"
        s["log"] += "\n  \u23f3 Hardware Virtualization \u2014 checking..."
        await self._update_ui()

        bio_enabled, bio_msg = await self._check_bios_virtualization()
        if bio_enabled:
            s["check_sub_status"][0]["status"] = "enabled"
            s["check_sub_status"][0]["detail"] = "Ready"
            s["log"] += f"\n  \u2713 {bio_msg}"
        else:
            s["check_sub_status"][0]["status"] = "disabled"
            s["check_sub_status"][0]["detail"] = "Disabled"
            s["log"] += f"\n  \u2717 {bio_msg}"
            s["log"] += "\n  \u2139 Virtualization must be enabled in BIOS/UEFI settings."
            s["log"] += "\n  \u2139 Restart your PC, press BIOS key (F2/Del/F10) at boot, and enable VT-x/AMD-V."
        s["vhd_enabled"] = bio_enabled
        await self._update_ui()
        if self._scan_cancelled:
            s["checking"] = False
            return False

        # ── Rows 1-4: Check & Enable Required Windows Features ───────────
        s["log"] += "\n\n--- Checking Required Windows Features ---"
        await self._update_ui()

        restart_dialog_shown = False
        features = []
        for idx, feat in enumerate(self.WSA_REQUIRED_FEATURES):
            row_idx = idx + 1
            s["check_sub_status"][row_idx]["status"] = "checking"
            s["log"] += f"\n  \u23f3 {feat['label']} \u2014 checking..."
            await self._update_ui()

            enabled = await self._check_windows_feature(feat["name"])
            features.append({"name": feat["name"], "label": feat["label"], "enabled": enabled, "row_idx": row_idx})

            if enabled is True:
                s["check_sub_status"][row_idx]["status"] = "enabled"
                s["check_sub_status"][row_idx]["detail"] = "Ready"
                s["log"] += f"\n  \u2713 {feat['label']} \u2014 already enabled."
            elif enabled is False:
                s["check_sub_status"][row_idx]["status"] = "disabled"
                s["check_sub_status"][row_idx]["detail"] = "Disabled"
                s["log"] += f"\n  \u2717 {feat['label']} \u2014 not enabled, will enable."
            else:
                s["check_sub_status"][row_idx]["status"] = "disabled"
                s["check_sub_status"][row_idx]["detail"] = "Disabled"
                s["log"] += f"\n  \u2139 {feat['label']} \u2014 status unknown, will attempt enable."
            await self._update_ui()

        need_enable = [f for f in features if f["enabled"] is False or f["enabled"] is None]

        if need_enable:
            s["log"] += f"\n\n  Enabling {len(need_enable)} feature(s)..."
            await self._update_ui()

            restart_needed = False
            for f in need_enable:
                row_idx = f["row_idx"]
                s["check_sub_status"][row_idx]["status"] = "enabling"
                s["check_sub_status"][row_idx]["detail"] = "Will enable"
                s["log"] += f"\n  \u23f3 {f['label']} \u2014 enabling..."
                await self._update_ui()
                success, msg = await self._enable_windows_feature(f["name"])
                if success:
                    actual = await self._check_windows_feature(f["name"])
                    if actual is True:
                        s["check_sub_status"][row_idx]["status"] = "done"
                        s["check_sub_status"][row_idx]["detail"] = "Enabled (restart pending)"
                        s["log"] += f"\n  \u2713 {f['label']} \u2014 {msg}"
                        restart_needed = True
                    elif actual is None and await self._feature_pending_restart(f["name"]):
                        s["check_sub_status"][row_idx]["status"] = "done"
                        s["check_sub_status"][row_idx]["detail"] = "Enabled (restart pending)"
                        s["log"] += f"\n  \u2713 {f['label']} \u2014 {msg}"
                        restart_needed = True
                    else:
                        s["log"] += f"\n  \u2139 {f['label']} \u2014 command passed but not enabled yet, retrying with DISM..."
                        await self._update_ui()
                        success2, msg2 = await self._enable_windows_feature_dism(f["name"])
                        if success2:
                            s["check_sub_status"][row_idx]["status"] = "done"
                            s["check_sub_status"][row_idx]["detail"] = "Enabled (restart pending)"
                            s["log"] += f"\n  \u2713 {f['label']} \u2014 {msg2}"
                            restart_needed = True
                        else:
                            s["check_sub_status"][row_idx]["status"] = "failed"
                            s["check_sub_status"][row_idx]["detail"] = "Failed"
                            s["log"] += f"\n  \u2717 {f['label']} \u2014 could not enable: {msg2}"
                else:
                    s["check_sub_status"][row_idx]["status"] = "failed"
                    s["check_sub_status"][row_idx]["detail"] = "Failed"
                    s["log"] += f"\n  \u2717 {f['label']} \u2014 failed: {msg}"
                await self._update_ui()

            if restart_needed:
                s["log"] += "\n\n  \u26a0 A system restart is required to apply feature changes."
                s["log"] += "\n  The installer will automatically resume after restart."
                s["log"] += "\n  Creating auto-start entry..."
                self._create_runonce_key()
                await self._update_ui()
                if self.page:
                    await self._show_restart_dialog(self.page)
                    await self.restart_action_event.wait()
                    restart_dialog_shown = True
        else:
            s["log"] += "\n\n  \u2713 All required features are already enabled."
            for idx, feat in enumerate(self.WSA_REQUIRED_FEATURES):
                s["check_sub_status"][idx + 1]["status"] = "enabled"
                s["check_sub_status"][idx + 1]["detail"] = "Ready"
            if self._runonce_key_exists():
                self._remove_runonce_key()
            await self._update_ui()

        # ── Row 5: Check WSA Installation ────────────────────────────────
        if self._scan_cancelled:
            s["checking"] = False
            return False
        s["check_sub_status"][5]["status"] = "checking"
        s["log"] += "\n\n--- Checking WSA Installation ---"
        s["log"] += "\n  \u23f3 WSA Installed \u2014 checking..."
        await self._update_ui()

        cmd_installed = ["powershell.exe", "-NoProfile", "-Command", "Get-AppxPackage *WindowsSubsystemForAndroid* | Select-Object -ExpandProperty InstallLocation"]
        creation_flags = 0x08000000 if sys.platform == "win32" else 0
        try:
            self.active_proc = await self._create_subprocess(
                *cmd_installed,
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                creationflags=creation_flags
            )
            process = self.active_proc
            stdout, _ = await process.communicate()
            if self.active_proc == process: self.active_proc = None
            install_location = stdout.decode().strip()
            
            if install_location:
                s["wsa_found"] = True
                s["check_sub_status"][5]["status"] = "installed"
                s["check_sub_status"][5]["detail"] = "Found"
                s["log"] += f"\n  \u2713 WSA Found at: {install_location}"
                
                check_cmd = "Get-Process -Name WsaClient, WsaService, vmmemWSA -ErrorAction SilentlyContinue"
                self.active_proc = await self._create_subprocess(
                    "powershell.exe", "-NoProfile", "-Command", check_cmd,
                    stdin=asyncio.subprocess.DEVNULL,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    creationflags=creation_flags
                )
                process = self.active_proc
                stdout, _ = await process.communicate()
                if self.active_proc == process: self.active_proc = None
                
                if stdout.strip():
                    s["wsa_running"] = True
                    s["check_sub_status"][5]["status"] = "running"
                    s["check_sub_status"][5]["detail"] = "Running"
                    s["log"] += "\n  \u2713 WSA Status: Running"
                else:
                    s["wsa_running"] = False
                    s["check_sub_status"][5]["status"] = "stopped"
                    s["check_sub_status"][5]["detail"] = "Stopped"
                    s["log"] += "\n  \u2139 WSA Status: Stopped"
            else:
                s["wsa_found"] = False
                s["wsa_running"] = False
                s["check_sub_status"][5]["status"] = "not_installed"
                s["check_sub_status"][5]["detail"] = "Not Installed"
                s["log"] += "\n\n  \u2717 Result: WSA was not found on this system."
        except Exception as e:
            s["log"] += f"\n  Error during scan: {e}"

        # ──────────────── Phase 2/3: Bundle Check ────────────────────────
        if self._scan_cancelled:
            s["checking"] = False
            return False
        s["check_phase"] = 1
        s["check_phase_title"] = "Bundle Check"
        s["check_sub_status"] = [
            {"label": "Searching for bundle file", "status": "pending", "detail": ""},
            {"label": "Checking bundle integrity", "status": "pending", "detail": ""},
            {"label": "Preparing cache folder", "status": "pending", "detail": ""},
            {"label": "Extracting WSA packages", "status": "pending", "detail": ""},
            {"label": "Cleaning up archive", "status": "pending", "detail": ""},
        ]
        await self._update_ui()

        out_asset = pathlib.Path(self.OUT_ASSET_DIR)
        bundle_name_cfg = getattr(self, "_cfg_cache", None)
        if bundle_name_cfg is None:
            try:
                bundle_name_cfg = getattr(CONFIG, "config", {}).get("BUNDLE_NAME", getattr(CONFIG, "BUNDLE_NAME", ""))
            except Exception:
                bundle_name_cfg = ""
        if not bundle_name_cfg:
            bundle_name_cfg = "bundle.wsa"
        candidate_names = [bundle_name_cfg]
        candidate_names += ["bundle.7z", "bundle.zip"]
        seen = set()
        bundle_path = None
        for name in candidate_names:
            if not name or name in seen:
                continue
            seen.add(name)
            candidate = out_asset / name
            if candidate.exists():
                bundle_path = candidate
                break

        if bundle_path:
            s["bundle_check_result"] = "found"
            s["check_sub_status"][0]["status"] = "done"
            s["check_sub_status"][0]["detail"] = bundle_path.name
            s["log"] += f"\n[\u2139] Bundled package found: {bundle_path.name}"
            await self._update_ui()

            s["check_sub_status"][1]["status"] = "checking"
            await self._update_ui()
            if self._scan_cancelled:
                s["checking"] = False
                return False
            try:
                size_mb = bundle_path.stat().st_size / 1024 / 1024
                if size_mb > 1:
                    s["check_sub_status"][1]["status"] = "done"
                    s["check_sub_status"][1]["detail"] = f"{size_mb:.0f} MB"
                else:
                    s["check_sub_status"][1]["status"] = "failed"
                    s["check_sub_status"][1]["detail"] = "Corrupt"
                    s["log"] += "\n  \u26A0 Bundle file appears corrupt (too small)."
                await self._update_ui()
            except Exception:
                s["check_sub_status"][1]["status"] = "failed"
                s["check_sub_status"][1]["detail"] = "Error"
                await self._update_ui()

            s["check_sub_status"][2]["status"] = "checking"
            await self._update_ui()
            if self._scan_cancelled:
                s["checking"] = False
                return False
            try:
                self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
                s["check_sub_status"][2]["status"] = "done"
                s["check_sub_status"][2]["detail"] = "Ready"
            except Exception:
                s["check_sub_status"][2]["status"] = "failed"
                s["check_sub_status"][2]["detail"] = "Failed"
            await self._update_ui()

            s["check_sub_status"][3]["status"] = "checking"
            s["log"] += "\nExtracting bundle..."
            await self._update_ui()
            if self._scan_cancelled:
                s["checking"] = False
                return False
            try:
                process = await self._create_subprocess(
                    "tar.exe", "-xvf", str(bundle_path), "-C", str(self.CACHE_DIR),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT,
                    creationflags=0x08000000 if sys.platform == "win32" else 0
                )
                count = 0
                while True:
                    line = await process.stdout.readline()
                    if not line: break
                    line_text = line.decode(errors='replace').strip()
                    if line_text:
                        display_line = line_text if len(line_text) < 50 else "..." + line_text[-47:]
                        s["log"] = f"Extracting Bundle: {display_line}"
                        count += 1
                        if count % 20 == 0:
                            await self._update_ui()
                await process.wait()
                s["check_sub_status"][3]["status"] = "done"
                s["check_sub_status"][3]["detail"] = "Extracted"
                s["log"] = "[\u2713] Bundle extracted successfully."
                await self._update_ui()
            except Exception as e:
                s["check_sub_status"][3]["status"] = "failed"
                s["check_sub_status"][3]["detail"] = "Failed"
                s["log"] += f"\n  \u26A0 Bundle extraction failed: {e}"
                await self._update_ui()

            s["check_sub_status"][4]["status"] = "checking"
            await self._update_ui()
            try:
                os.remove(bundle_path)
                s["check_sub_status"][4]["status"] = "done"
                s["check_sub_status"][4]["detail"] = "Removed"
                s["log"] += "\n[\u2713] Bundle archive removed to save space."
            except Exception:
                s["check_sub_status"][4]["status"] = "done"
                s["check_sub_status"][4]["detail"] = "Skipped"
            await self._update_ui()
        else:
            has_partial = False
            partial_bytes = 0
            try:
                bundle_name_cfg = getattr(self, "_cfg_cache", None)
                if bundle_name_cfg is None:
                    try:
                        bundle_name_cfg = getattr(CONFIG, "config", {}).get("BUNDLE_NAME", getattr(CONFIG, "BUNDLE_NAME", ""))
                    except Exception:
                        bundle_name_cfg = ""
                if not bundle_name_cfg:
                    bundle_name_cfg = "bundle.wsa"
                bundle_dest = out_asset / bundle_name_cfg
                prefix = str(bundle_dest) + ".part"
                for item in bundle_dest.parent.iterdir():
                    if str(item).startswith(prefix):
                        has_partial = True
                        try:
                            partial_bytes += item.stat().st_size
                        except Exception:
                            pass
            except Exception:
                pass

            if has_partial:
                size_str = f"{partial_bytes / 1024 / 1024:.1f} MB" if partial_bytes > 1024 * 1024 else f"{partial_bytes / 1024:.1f} KB"
                s["bundle_check_result"] = "partial"
                s["check_sub_status"][0]["status"] = "done"
                s["check_sub_status"][0]["detail"] = "Partial found"
                s["log"] += f"\n  \u2139 Partial download detected ({size_str} saved) — will resume if needed."
            else:
                s["bundle_check_result"] = "not_found"
                s["check_sub_status"][0]["status"] = "done"
                s["check_sub_status"][0]["detail"] = "Not found"
                s["log"] += "\n  \u2139 No bundle file found — will download if needed."
            await self._update_ui()

        # ──────────────── Phase 3/3: System-Level Fixes ──────────────────
        bundle_needs_download = s.get("bundle_check_result") in ("not_found", "partial")
        if not s.get("wsa_found", False) and not bundle_needs_download:
            s["check_phase"] = 2
            s["check_phase_title"] = "System-Level Fixes"
            s["log"] += "\n\n  \u2139 Applying system-level fixes before installation..."
            await self._update_ui()
            try:
                restart_needed = await self.virtualization_bypass_for_wsa("log")
            except Exception as fix_err:
                s["log"] += f"\n  \u26a0 Some system fixes encountered issues: {fix_err}"
                restart_needed = False

            if restart_needed and not restart_dialog_shown:
                s["log"] += "\n\n  \u26a0 A system restart is required to apply system-level fixes."
                s["log"] += "\n  The installer will automatically resume after restart."
                s["log"] += "\n  Creating auto-start entry..."
                self._create_runonce_key()
                await self._update_ui()
                if self.page:
                    await self._show_restart_dialog(self.page)
                    await self.restart_action_event.wait()
                    restart_dialog_shown = True

        # ── Scan Complete ─────────────────────────────────────────────────
        s["checking"] = False
        s["scan_complete"] = True
        await self._update_ui()
        return s["wsa_found"]

    # ─── WSA Virtualization Bypass Methods ──────────────────────────────────

    async def _feature_pending_restart(self, feature_name):
        """Check if a Windows optional feature is enabled but pending restart."""
        try:
            cmd = ["powershell.exe", "-NoProfile", "-Command",
                   f"(Get-WindowsOptionalFeature -Online -FeatureName '{feature_name}').State"]
            proc = await self._create_subprocess(
                *cmd, stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                creationflags=0x08000000
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=30)
            state = stdout.decode(errors="ignore").strip().lower()
            return "pendingrestart" in state or "pending" in state
        except Exception:
            return False

    async def _ensure_hyper_v(self, log_key):
        """Enable Hyper-V, VirtualMachinePlatform, and HypervisorPlatform features.
        Returns True if any feature requires a system restart to take effect."""
        s = self.state
        if self._scan_cancelled:
            return False
        restart_needed = False
        s[log_key] += "\nChecking Hyper-V features..."
        await self._update_ui()
        features = ["Microsoft-Hyper-V", "VirtualMachinePlatform", "HypervisorPlatform"]
        for feat in features:
            try:
                cmd = ["powershell.exe", "-NoProfile", "-Command",
                       f"Enable-WindowsOptionalFeature -Online -FeatureName {feat} -All -NoRestart -ErrorAction SilentlyContinue"]
                proc = await self._create_subprocess(
                    *cmd, stdin=asyncio.subprocess.DEVNULL,
                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                    creationflags=0x08000000
                )
                await asyncio.wait_for(proc.communicate(), timeout=60)
                if proc.returncode == 0:
                    s[log_key] += f"\n  \u2713 {feat} enabled."
                    if await self._feature_pending_restart(feat):
                        restart_needed = True
                        s[log_key] += f"\n  \u2139 {feat} enabled (restart pending)."
                else:
                    s[log_key] += f"\n  \u2139 {feat} already enabled or pending restart."
            except Exception as e:
                s[log_key] += f"\n  \u26A0 {feat}: {e}"
            await self._update_ui()
        return restart_needed

    async def _uninstall_problematic_kbs(self, log_key):
        """Detect and uninstall known problematic Windows Updates that break WSA."""
        s = self.state
        if self._scan_cancelled:
            return
        s[log_key] += "\nChecking for problematic Windows Updates..."
        await self._update_ui()
        problematic_kbs = ["KB5062553", "KB5064081", "KB5072033", "KB5094126"]
        for kb in problematic_kbs:
            if self._scan_cancelled:
                return
            try:
                check_cmd = ["powershell.exe", "-NoProfile", "-Command",
                             f"Get-HotFix -Id {kb} -ErrorAction SilentlyContinue"]
                proc = await self._create_subprocess(
                    *check_cmd, stdin=asyncio.subprocess.DEVNULL,
                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                    creationflags=0x08000000
                )
                stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=30)
                if kb.encode() in stdout:
                    s[log_key] += f"\n  \u26A0 Found {kb} — uninstalling..."
                    await self._update_ui()
                    uninstall_cmd = ["powershell.exe", "-NoProfile", "-Command",
                                     f"wusa.exe /uninstall /kb:{kb} /quiet /norestart"]
                    proc2 = await self._create_subprocess(
                        *uninstall_cmd, stdin=asyncio.subprocess.DEVNULL,
                        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                        creationflags=0x08000000
                    )
                    await asyncio.wait_for(proc2.communicate(), timeout=120)
                    s[log_key] += f"\n  \u2713 {kb} uninstall initiated."
                else:
                    s[log_key] += f"\n  \u2713 {kb} not installed (OK)."
            except Exception as e:
                s[log_key] += f"\n  \u26A0 {kb} check failed: {e}"
            await self._update_ui()

    async def _ensure_wsl2(self, log_key):
        """Check and install WSL2 if not present. Returns True if a restart is required."""
        s = self.state
        if self._scan_cancelled:
            return False
        restart_needed = False
        s[log_key] += "\nChecking WSL2..."
        await self._update_ui()
        try:
            proc = await self._create_subprocess(
                "wsl", "--status",
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                creationflags=0x08000000
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=15)
            output = (stdout.decode(errors="ignore") + stderr.decode(errors="ignore")).lower()
            if proc.returncode == 0 and ("default version" in output or "wsl2" in output or "windows subsystem for linux" in output):
                s[log_key] += "\n  \u2713 WSL2 is installed."
            else:
                raise FileNotFoundError("WSL2 not detected")
        except Exception:
            s[log_key] += "\n  \u2139 WSL2 not found — installing..."
            await self._update_ui()
            try:
                proc = await self._create_subprocess(
                    "wsl", "--install", "--no-distribution",
                    stdin=asyncio.subprocess.DEVNULL,
                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                    creationflags=0x08000000
                )
                await asyncio.wait_for(proc.communicate(), timeout=120)
                s[log_key] += "\n  \u2713 WSL2 installation initiated (restart may be required)."
                restart_needed = True
            except Exception as e:
                s[log_key] += f"\n  \u26A0 WSL2 install failed: {e}"
        await self._update_ui()
        return restart_needed

    async def _add_defender_exclusion(self, log_key):
        """Add WSA installation folder to Windows Defender exclusion list."""
        s = self.state
        if self._scan_cancelled:
            return
        s[log_key] += "\nAdding Defender exclusion..."
        await self._update_ui()
        wsa_path = str(self.WSA_DEST_DIR)
        try:
            cmd = ["powershell.exe", "-NoProfile", "-Command",
                   f"Add-MpPreference -ExclusionPath '{wsa_path}' -ErrorAction Stop"]
            proc = await self._create_subprocess(
                *cmd, stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                creationflags=0x08000000
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
            if proc.returncode == 0:
                s[log_key] += f"\n  \u2713 Defender exclusion added for: {wsa_path}"
            else:
                err = stderr.decode(errors="ignore").strip()
                s[log_key] += f"\n  \u26A0 Defender exclusion failed: {err}"
        except Exception as e:
            s[log_key] += f"\n  \u26A0 Defender exclusion failed: {e}"
        await self._update_ui()

    async def _apply_registry_vbs_fix(self, log_key):
        """Disable Virtualization-Based Security via registry to fix WSA compatibility."""
        s = self.state
        if self._scan_cancelled:
            return
        s[log_key] += "\nApplying registry fix (VBS)..."
        await self._update_ui()
        try:
            cmd = ["reg", "add",
                   r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
                   "/v", "EnableVirtualizationBasedSecurity", "/t", "REG_DWORD",
                   "/d", "0", "/f"]
            proc = await self._create_subprocess(
                *cmd, stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                creationflags=0x08000000
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=15)
            if proc.returncode == 0:
                s[log_key] += "\n  \u2713 EnableVirtualizationBasedSecurity set to 0."
            else:
                s[log_key] += "\n  \u26A0 VBS registry fix failed (may need admin)."
        except Exception as e:
            s[log_key] += f"\n  \u26A0 VBS registry error: {e}"
        await self._update_ui()

    async def _apply_registry_fsdepends_fix(self, log_key):
        """Disable FsDepends service to fix WSA virtual disk conflicts."""
        s = self.state
        if self._scan_cancelled:
            return
        s[log_key] += "\nApplying registry fix (FsDepends)..."
        await self._update_ui()
        try:
            cmd = ["reg", "add",
                   r"HKLM\SYSTEM\CurrentControlSet\Services\FsDepends",
                   "/v", "Start", "/t", "REG_DWORD", "/d", "0", "/f"]
            proc = await self._create_subprocess(
                *cmd, stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                creationflags=0x08000000
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=15)
            if proc.returncode == 0:
                s[log_key] += "\n  \u2713 FsDepends Start set to 0."
            else:
                s[log_key] += "\n  \u26A0 FsDepends registry fix failed (may need admin)."
        except Exception as e:
            s[log_key] += f"\n  \u26A0 FsDepends registry error: {e}"
        await self._update_ui()

    # ─── BIOS Virtualization Detection ─────────────────────────────────────

    async def _check_bios_virtualization(self):
        """Detect if hardware virtualization (VT-x/AMD-V) is enabled in BIOS.
        Uses multiple fallback methods for reliable detection.
        Returns (enabled: bool, details: str)."""
        creation_flags = 0x08000000 if sys.platform == "win32" else 0

        # Method 1: WMI VirtualizationFirmwareEnabled
        try:
            cmd = ["powershell.exe", "-NoProfile", "-Command",
                   "Get-CimInstance -ClassName Win32_Processor | Select-Object -First 1 -ExpandProperty VirtualizationFirmwareEnabled"]
            proc = await self._create_subprocess(
                *cmd, stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                creationflags=creation_flags
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=15)
            result = stdout.decode(errors="ignore").strip().lower()
            if result == "true":
                return True, "Hardware virtualization (VT-x/AMD-V) is enabled."
        except Exception:
            pass

        # Method 2: systeminfo — check for hypervisor presence and VM extensions
        try:
            cmd2 = ["systeminfo"]
            proc2 = await self._create_subprocess(
                *cmd2, stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                creationflags=creation_flags
            )
            stdout2, _ = await asyncio.wait_for(proc2.communicate(), timeout=30)
            output = stdout2.decode(errors="ignore")
            # If a hypervisor is detected, virtualization IS enabled
            if "a hypervisor has been detected" in output.lower():
                return True, "Hardware virtualization is enabled (hypervisor detected)."
            # Check Hyper-V requirements for VM extensions
            if "hyper-v requirements" in output.lower():
                if "yes" in output.lower().split("hyper-v requirements")[-1][:200]:
                    return True, "Hardware virtualization is enabled (VM extensions present)."
        except Exception:
            pass

        # Method 3: Get-ComputerInfo PropertyVirtualizationFirmwareEnabled
        try:
            cmd3 = ["powershell.exe", "-NoProfile", "-Command",
                    "(Get-ComputerInfo -Property HyperVRequirementVirtualizationFirmwareEnabled -ErrorAction SilentlyContinue).HyperVRequirementVirtualizationFirmwareEnabled"]
            proc3 = await self._create_subprocess(
                *cmd3, stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                creationflags=creation_flags
            )
            stdout3, _ = await asyncio.wait_for(proc3.communicate(), timeout=15)
            result3 = stdout3.decode(errors="ignore").strip().lower()
            if result3 == "true":
                return True, "Hardware virtualization is enabled (ComputerInfo)."
        except Exception:
            pass

        # Method 4: Check if any Hyper-V / virtualization feature is active
        try:
            cmd4 = ["powershell.exe", "-NoProfile", "-Command",
                    "(Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All -ErrorAction SilentlyContinue).State"]
            proc4 = await self._create_subprocess(
                *cmd4, stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                creationflags=creation_flags
            )
            stdout4, _ = await asyncio.wait_for(proc4.communicate(), timeout=15)
            result4 = stdout4.decode(errors="ignore").strip().lower()
            if result4 == "enabled":
                return True, "Hardware virtualization is enabled (Hyper-V active)."
        except Exception:
            pass

        # Method 5: Check VmMonitorModeExtensions in registry
        try:
            cmd5 = ["powershell.exe", "-NoProfile", "-Command",
                    "(Get-ItemProperty 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Configuration Manager' -ErrorAction SilentlyContinue).VmMonitorModeExtensions"]
            proc5 = await self._create_subprocess(
                *cmd5, stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                creationflags=creation_flags
            )
            stdout5, _ = await asyncio.wait_for(proc5.communicate(), timeout=10)
            result5 = stdout5.decode(errors="ignore").strip()
            if result5 and result5.lower() != "false" and result5 != "0":
                return True, "Hardware virtualization is enabled (registry check)."
        except Exception:
            pass

        return False, "Hardware virtualization (VT-x/AMD-V) could not be confirmed. It may be disabled in BIOS."

    def _get_pc_brand(self):
        """Detect PC manufacturer for brand-specific BIOS instructions."""
        try:
            cmd = ["powershell.exe", "-NoProfile", "-Command",
                   "Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object -First 1 -ExpandProperty Manufacturer"]
            import subprocess as _sp
            r = _sp.run(cmd, capture_output=True, timeout=10, creationflags=0x08000000)
            brand = r.stdout.decode(errors="ignore").strip().lower()
            return brand
        except Exception:
            return "generic"

    # ─── Windows Feature Check/Enable ──────────────────────────────────────

    WSA_REQUIRED_FEATURES = [
        {"name": "Microsoft-Hyper-V",              "label": "Hyper-V"},
        {"name": "VirtualMachinePlatform",          "label": "Virtual Machine Platform"},
        {"name": "HypervisorPlatform",              "label": "Windows Hypervisor Platform"},
        {"name": "Microsoft-Windows-Subsystem-Linux", "label": "Windows Subsystem for Linux (WSL)"},
    ]

    async def _check_windows_feature(self, feature_name):
        """Check if a Windows optional feature is enabled.
        Returns True if enabled, False if disabled, None if error."""
        try:
            cmd = ["powershell.exe", "-NoProfile", "-Command",
                   f"(Get-WindowsOptionalFeature -Online -FeatureName '{feature_name}').State"]
            proc = await self._create_subprocess(
                *cmd, stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                creationflags=0x08000000
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=30)
            state = stdout.decode(errors="ignore").strip().lower()
            return state == "enabled"
        except Exception:
            return None

    async def _check_all_features(self):
        """Check all 4 required features. Returns list of {name, label, enabled}."""
        results = []
        for feat in self.WSA_REQUIRED_FEATURES:
            enabled = await self._check_windows_feature(feat["name"])
            results.append({
                "name": feat["name"],
                "label": feat["label"],
                "enabled": enabled,
            })
        return results

    async def _enable_windows_feature(self, feature_name):
        """Enable a single Windows optional feature. Returns (success: bool, msg: str)."""
        try:
            cmd = ["powershell.exe", "-NoProfile", "-Command",
                   f"Enable-WindowsOptionalFeature -Online -FeatureName '{feature_name}' -All -NoRestart -ErrorAction Stop"]
            proc = await self._create_subprocess(
                *cmd, stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                creationflags=0x08000000
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
            if proc.returncode == 0:
                return True, "Enabled successfully."
            else:
                err = stderr.decode(errors="ignore").strip()
                if "restart" in err.lower() or "pending" in err.lower():
                    return True, "Enabled (restart required)."
                return False, err[:200] if err else "Unknown error."
        except asyncio.TimeoutError:
            return False, "Timed out."
        except Exception as e:
            return False, str(e)[:200]

    async def _enable_windows_feature_dism(self, feature_name):
        """Enable a Windows optional feature using DISM as fallback. Returns (success: bool, msg: str)."""
        try:
            cmd = ["dism", "/online", "/Enable-Feature", f"/FeatureName:{feature_name}", "/All", "/NoRestart", "/Quiet"]
            proc = await self._create_subprocess(
                *cmd, stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                creationflags=0x08000000
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
            if proc.returncode == 0:
                return True, "Enabled successfully (DISM)."
            elif proc.returncode == 3010:
                return True, "Enabled successfully (DISM, restart required)."
            else:
                err = stderr.decode(errors="ignore").strip() or stdout.decode(errors="ignore").strip()
                return False, err[:200] if err else "DISM error."
        except asyncio.TimeoutError:
            return False, "DISM timed out."
        except Exception as e:
            return False, f"DISM error: {str(e)[:200]}"

    # ─── RunOnce Registry Key ──────────────────────────────────────────────

    RUNONCE_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"
    RUNONCE_VALUE_NAME = "WSAInstallerResume"

    def _create_runonce_key(self):
        """Create RunOnce registry key so app auto-launches after restart."""
        try:
            exe_path = sys.executable if getattr(sys, 'frozen', False) else sys.executable
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.RUNONCE_KEY, 0,
                                 winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY)
            winreg.SetValueEx(key, self.RUNONCE_VALUE_NAME, 0, winreg.REG_SZ, f'"{exe_path}"')
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"[RUNONCE] Failed to create: {e}")
            return False

    def _remove_runonce_key(self):
        """Remove RunOnce registry key after successful feature check."""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.RUNONCE_KEY, 0,
                                 winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY)
            winreg.DeleteValue(key, self.RUNONCE_VALUE_NAME)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            return True
        except Exception as e:
            print(f"[RUNONCE] Failed to remove: {e}")
            return False

    def _runonce_key_exists(self):
        """Check if RunOnce key exists."""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.RUNONCE_KEY, 0,
                                 winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            winreg.QueryValueEx(key, self.RUNONCE_VALUE_NAME)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False

    async def _show_restart_dialog(self, page):
        """Show restart overlay prompting user to restart now or later."""
        self.restart_action_event.clear()
        self.state["show_restart_dialog"] = True
        await self._update_ui()

    async def virtualization_bypass_for_wsa(self, log_key):
        """All-in-one virtualization bypass for WSA stability.
        Applies system-level fixes to prevent WSA crash on newer Windows builds.
        Returns True if any change requires a system restart to take effect."""
        s = self.state
        restart_needed = False
        s["check_sub_status"] = [
            {"label": "Checking Hyper-V features", "status": "pending", "detail": ""},
            {"label": "Checking for problematic Windows Updates", "status": "pending", "detail": ""},
            {"label": "Checking WSL2", "status": "pending", "detail": ""},
            {"label": "Adding Defender exclusion", "status": "pending", "detail": ""},
            {"label": "Applying registry fix (VBS)", "status": "pending", "detail": ""},
            {"label": "Applying registry fix (FsDepends)", "status": "pending", "detail": ""},
        ]
        s[log_key] += "\n\u2500\u2500 Applying WSA Virtualization Bypass \u2500\u2500"
        await self._update_ui()

        s["check_sub_status"][0]["status"] = "checking"
        if await self._ensure_hyper_v(log_key):
            restart_needed = True
        s["check_sub_status"][0]["status"] = "done"
        s["check_sub_status"][0]["detail"] = "All enabled"
        s["check_sub_status"][1]["status"] = "checking"
        await self._update_ui()

        await self._uninstall_problematic_kbs(log_key)
        s["check_sub_status"][1]["status"] = "done"
        s["check_sub_status"][1]["detail"] = "OK"
        s["check_sub_status"][2]["status"] = "checking"
        await self._update_ui()

        if await self._ensure_wsl2(log_key):
            restart_needed = True
        s["check_sub_status"][2]["status"] = "done"
        s["check_sub_status"][2]["detail"] = "OK"
        s["check_sub_status"][3]["status"] = "checking"
        await self._update_ui()

        await self._add_defender_exclusion(log_key)
        s["check_sub_status"][3]["status"] = "done"
        s["check_sub_status"][3]["detail"] = "Excluded"
        s["check_sub_status"][4]["status"] = "checking"
        await self._update_ui()

        await self._apply_registry_vbs_fix(log_key)
        s["check_sub_status"][4]["status"] = "done"
        s["check_sub_status"][4]["detail"] = "Applied"
        s["check_sub_status"][5]["status"] = "checking"
        await self._update_ui()

        await self._apply_registry_fsdepends_fix(log_key)
        s["check_sub_status"][5]["status"] = "done"
        s["check_sub_status"][5]["detail"] = "Applied"
        await self._update_ui()

        s[log_key] += "\n\u2500\u2500 Virtualization Bypass Complete \u2500\u2500"
        return restart_needed

    # ─── WSA Client EXE Patch ──────────────────────────────────────────────

    async def _patch_wsa_client_exe(self, log_key):
        """Replace WsaClient.exe with pre-patched version from assets to fix crash."""
        s = self.state
        s[log_key] += "\nPatching WsaClient.exe (crash fix)..."
        await self._update_ui()

        patched_exe = resource_path(os.path.join("assets", "WsaClient.exe"))
        if not os.path.exists(patched_exe):
            s[log_key] += "\n  \u2139 Patched WsaClient.exe not found in assets — skipping."
            return False

        # Find the target WsaClient.exe in WSA destination
        target_exe = os.path.join(self.WSA_DEST_DIR, "WsaClient", "WsaClient.exe")
        if not os.path.exists(target_exe):
            target_exe = os.path.join(self.WSA_DEST_DIR, "WsaClient.exe")
        if not os.path.exists(target_exe):
            s[log_key] += "\n  \u2139 WsaClient.exe not found in WSA folder — skipping."
            return False

        try:
            backup = target_exe + ".bak"
            if not os.path.exists(backup):
                shutil.copy2(target_exe, backup)
                s[log_key] += "\n  Original WsaClient.exe backed up."
            shutil.copy2(patched_exe, target_exe)
            s[log_key] += "\n  \u2713 WsaClient.exe patched successfully (crash fix applied)."
            await self._update_ui()
            return True
        except Exception as e:
            s[log_key] += f"\n  \u26A0 Could not patch WsaClient.exe: {e}"
            await self._update_ui()
            return False

    async def install_wsa(self):
        """Installs the basic WSA package from the unified destination."""
        self._scan_cancelled = False
        s = self.state
        s["installing"] = True
        s["install_log"] = "Starting WSA Basic installation..."
        s["install_progress"] = 0.1
        s["install_done"] = False

        async def begin_phase(phase_idx, title, step_labels):
            s["install_phase"] = phase_idx
            s["install_phase_title"] = title
            s["install_sub_status"] = [{"label": lbl, "status": "pending"} for lbl in step_labels]
            s["install_log"] += f"\n\n=== Phase {phase_idx+1}/6: {title} ==="
            await self._update_ui()

        async def step_checking(idx):
            s["install_sub_status"][idx]["status"] = "checking"
            await self._update_ui()

        async def step_done(idx):
            s["install_sub_status"][idx]["status"] = "done"
            await self._update_ui()

        async def step_failed(idx):
            s["install_sub_status"][idx]["status"] = "failed"
            await self._update_ui()

        async def step_done_text(idx, text):
            s["install_sub_status"][idx]["status"] = "done"
            s["install_sub_status"][idx]["detail"] = text
            await self._update_ui()

        async def step_failed_text(idx, text):
            s["install_sub_status"][idx]["status"] = "failed"
            s["install_sub_status"][idx]["detail"] = text
            await self._update_ui()

        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        # PHASE 1: Locate Package  (5 tracker steps, 7 sub-steps)
        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        await begin_phase(0, "Locate Package", [
            "Check unified destination",
            "Check legacy folder",
            "Check bundled assets",
            "Check cached archive",
            "Extract archive",
        ])

        # Step 1: Check unified destination
        await step_checking(0)
        s["install_log"] += "\n  Checking unified destination..."
        await self._update_ui()
        src = self.WSA_DEST_DIR
        if self._verify_wsa_folder(src):
            await step_done_text(0, "Found")
            s["install_log"] += "  \u2713 Found in unified destination."
        else:
            await step_done_text(0, "Not found")
            s["install_log"] += "  Not found."

        # Step 2: Check legacy folder
        await step_checking(1)
        s["install_log"] += "\n  Checking legacy folder..."
        await self._update_ui()
        src = os.path.join(self.OUT_ASSET_DIR, "WSA Basic Package")
        if self._verify_wsa_folder(src):
            await step_done_text(1, "Found")
            s["install_log"] += "  \u2713 Found in legacy folder."
        else:
            await step_done_text(1, "Not found")
            s["install_log"] += "  Not found."

        # Step 3: Check bundled assets
        await step_checking(2)
        s["install_log"] += "\n  Checking bundled assets..."
        await self._update_ui()
        src = resource_path(os.path.join("assets", "WSA Basic Package"))
        if self._verify_wsa_folder(src):
            await step_done_text(2, "Found")
            s["install_log"] += "  \u2713 Found in bundled assets."
        else:
            await step_done_text(2, "Not found")
            s["install_log"] += "  Not found."

        # Step 4: Check cached archive
        await step_checking(3)
        s["install_log"] += "\n  Checking cached archive..."
        await self._update_ui()
        cached = self._find_cached_archive("nogapps")
        if cached:
            await step_done_text(3, cached.name)
            s["install_log"] += f"  \u2713 Found cached: {cached.name}"
        else:
            await step_done_text(3, "No cache")
            s["install_log"] += "  No cached archive found."

        # Step 5: Extract archive (only if src not verified AND cached found)
        if not self._verify_wsa_folder(src) and cached:
            await step_checking(4)
            s["install_log"] += "\n  Starting extraction..."
            await self._update_ui()

            # Sub-step 5a: prepare
            s["install_sub_status"][4]["detail"] = "Preparing..."
            await self._update_ui()
            target = pathlib.Path(self.WSA_DEST_DIR)
            legacy_source = pathlib.Path(self.OUT_ASSET_DIR) / "WSA Basic Package"

            # Sub-step 5b-g: extract_7z handles internal steps
            ok = await self.extract_7z(cached, target, 'install_log', secondary_source=legacy_source)
            if not ok:
                await step_failed(4)
                s["installing"] = False
                await self._update_ui()
                return

            src = str(target)
            await step_done_text(4, "Extracted")
            s["install_log"] += "  \u2713 Extraction complete."
        elif not self._verify_wsa_folder(src) and not cached:
            await step_failed_text(4, "No package")
            s["install_log"] += "\n  \u2717 No package source available."
            s["installing"] = False
            s["show_download"] = "nogapps"
            await self._update_ui()
            return
        else:
            await step_done_text(4, "Skipped (already verified)")

        if not os.path.exists(src):
            s["install_log"] += f"\n  \u2717 Source not found: {src}"
            s["installing"] = False
            await self._update_ui()
            return

        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        # PHASE 2: Verify Assets  (2 tracker steps, 0 sub-steps)
        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        await begin_phase(1, "Verify Assets", [
            "Read filelist.txt",
            "Verify required files",
        ])

        # Step 1: Read filelist.txt
        await step_checking(0)
        s["install_log"] += "\n  Reading filelist.txt..."
        await self._update_ui()
        filelist_path = os.path.join(src, "filelist.txt")
        has_filelist = os.path.exists(filelist_path)
        if has_filelist:
            with open(filelist_path, "r") as f:
                required = [line.strip() for line in f if line.strip()]
            await step_done_text(0, f"{len(required)} files listed")
            s["install_log"] += f"  \u2713 Found {len(required)} required items."
        else:
            await step_done_text(0, "No filelist.txt")
            s["install_log"] += "  No filelist.txt found, skipping verification."

        # Step 2: Verify required files
        if has_filelist:
            await step_checking(1)
            s["install_log"] += "\n  Verifying files..."
            await self._update_ui()
            missing = [item for item in required if not os.path.exists(os.path.join(src, item))]
            if missing:
                await step_failed_text(1, f"Missing: {', '.join(missing[:3])}")
                s["install_log"] += f"  \u2717 CRITICAL: Assets missing: {', '.join(missing[:3])}..."
                s["install_log"] += "\n  \u2139 Tip: Ensure the application was bundled correctly."
                s["installing"] = False
                await self._update_ui()
                return
            await step_done_text(1, "All verified")
            s["install_log"] += "  \u2713 Verification successful."
        else:
            await step_done_text(1, "Skipped")

        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        # PHASE 3: Prepare System  (3 tracker steps, 3 sub-steps)
        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        await begin_phase(2, "Prepare System", [
            "Kill WSA processes",
            "Deploy shortcut",
            "Copy files to destination",
        ])

        try:
            # Step 1: Kill WSA processes
            await step_checking(0)
            s["install_log"] += "\n  Killing WSA processes..."
            await self._update_ui()
            # Sub-step 1a: graceful shutdown
            s["install_sub_status"][0]["detail"] = "Graceful shutdown..."
            await self._update_ui()
            try:
                proc = await self._create_subprocess(
                    "WsaClient.exe", "/shutdown",
                    stdin=asyncio.subprocess.DEVNULL,
                    creationflags=0x08000000 if sys.platform == "win32" else 0
                )
                await asyncio.wait_for(proc.wait(), timeout=5)
            except:
                pass
            await asyncio.sleep(1)
            # Sub-step 1b: kill install scripts
            s["install_sub_status"][0]["detail"] = "Terminating scripts..."
            await self._update_ui()
            s["install_log"] += "\n  Terminating background install scripts..."
            try:
                kill_ps_cmd = 'Get-CimInstance Win32_Process | Where-Object { ($_.Name -match "powershell.exe" -or $_.Name -match "pwsh.exe") -and $_.CommandLine -match "Install.ps1" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }'
                subprocess.run(["powershell.exe", "-NoProfile", "-Command", kill_ps_cmd],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               creationflags=0x08000000 if sys.platform == "win32" else 0)
            except:
                pass
            # Sub-step 1c: kill target processes
            s["install_sub_status"][0]["detail"] = "Killing target processes..."
            await self._update_ui()
            creation_flags = 0x08000000 if sys.platform == "win32" else 0
            for target in ["WsaClient.exe", "WindowsSubsystemForAndroid.exe", "adb.exe", "vmmemWSA.exe", "WsaService.exe"]:
                try:
                    proc = await self._create_subprocess(
                        "taskkill", "/F", "/IM", target, "/T",
                        stdin=asyncio.subprocess.DEVNULL, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                        creationflags=creation_flags
                    )
                    await proc.wait()
                except:
                    pass
            try:
                kill_cmd_bat = 'Get-CimInstance Win32_Process | Where-Object { $_.Name -match "cmd.exe" -and $_.CommandLine -match "Run.bat" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }'
                subprocess.run(["powershell.exe", "-NoProfile", "-Command", kill_cmd_bat],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               creationflags=creation_flags)
            except:
                pass
            await asyncio.sleep(2)
            await step_done_text(0, "Processes killed")
            s["install_log"] += "  \u2713 WSA processes killed."

            # Step 2: Deploy shortcut
            await step_checking(1)
            s["install_log"] += "\n  Deploying desktop shortcut..."
            await self._update_ui()
            shortcut_src = resource_path(os.path.join("assets", "Windows Subsystem for Android.lnk"))
            if os.path.exists(shortcut_src):
                try:
                    shutil.copy2(shortcut_src, CONFIG.WSA_ROOT)
                    await step_done_text(1, "Shortcut deployed")
                    s["install_log"] += "  \u2713 Shortcut deployed."
                except Exception as e:
                    await step_failed_text(1, str(e)[:40])
                    s["install_log"] += f"  \u26a0 Could not copy shortcut: {e}"
            else:
                await step_done_text(1, "No shortcut file")
                s["install_log"] += "  No shortcut file found, skipping."

            # Step 3: Copy files to destination
            await step_checking(2)
            await self._update_ui()
            os.makedirs(self.WSA_DEST_DIR, exist_ok=True)
            if os.path.abspath(src) != os.path.abspath(self.WSA_DEST_DIR):
                s["install_log"] += "\n  Moving package to unified destination..."
                s["install_sub_status"][2]["detail"] = "Copying files..."
                await self._update_ui()
                self._robust_merge_sync(src, self.WSA_DEST_DIR, "install_log")
                await step_done_text(2, "Files copied")
                s["install_log"] += "  \u2713 Files copied."
            else:
                await step_done_text(2, "Already in place")
                s["install_log"] += "  Already in unified destination."

        except Exception as e:
            s["install_log"] += f"\n  Error in Phase 3: {e}"

        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        # PHASE 4: Apply Patches  (4 tracker steps)
        # ─────────────────────────────────────────────────────────────────
        await begin_phase(3, "Apply Patches", [
            "Patch Run.bat",
            "Patch WsaClient.exe",
            "Patch AppxManifest.xml",
            "Install WSARepair proxy",
        ])

        # Step 1: Patch Run.bat
        await step_checking(0)
        s["install_log"] += "\n  Applying Run.bat patch..."
        await self._update_ui()
        os.makedirs(self.WSA_DEST_DIR, exist_ok=True)
        custom_run_bat = resource_path(os.path.join("assets", "Run.bat"))
        if os.path.exists(custom_run_bat):
            shutil.copy2(custom_run_bat, os.path.join(self.WSA_DEST_DIR, "Run.bat"))
            await step_done_text(0, "Run.bat patched")
            s["install_log"] += "  \u2713 Run.bat patched."
        else:
            await step_done_text(0, "No custom Run.bat")
            s["install_log"] += "  No custom Run.bat found, skipping."

        # Step 2: Patch WsaClient.exe
        await step_checking(1)
        s["install_log"] += "\n  Patching WsaClient.exe (crash fix)..."
        await self._update_ui()

        # Sub-step 2a: check patched exe
        s["install_sub_status"][1]["detail"] = "Checking patched exe..."
        await self._update_ui()
        patched_exe = resource_path(os.path.join("assets", "WsaClient.exe"))
        if not os.path.exists(patched_exe):
            await step_done_text(1, "No patched exe — skipped")
            s["install_log"] += "  Patched WsaClient.exe not found in assets \u2014 skipping."
        else:
            # Sub-step 2b: check target exe
            s["install_sub_status"][1]["detail"] = "Checking target..."
            await self._update_ui()
            target_exe = os.path.join(self.WSA_DEST_DIR, "WsaClient", "WsaClient.exe")
            if not os.path.exists(target_exe):
                target_exe = os.path.join(self.WSA_DEST_DIR, "WsaClient.exe")
            if not os.path.exists(target_exe):
                await step_done_text(1, "Target not found — skipped")
                s["install_log"] += "  WsaClient.exe not found in WSA folder \u2014 skipping."
            else:
                # Sub-step 2c: backup original
                s["install_sub_status"][1]["detail"] = "Backing up original..."
                await self._update_ui()
                backup = target_exe + ".bak"
                if not os.path.exists(backup):
                    shutil.copy2(target_exe, backup)
                    s["install_log"] += "  Original backed up."

                # Sub-step 2d: copy patched version
                s["install_sub_status"][1]["detail"] = "Copying patched exe..."
                await self._update_ui()
                try:
                    shutil.copy2(patched_exe, target_exe)
                    await step_done_text(1, "Crash fix applied")
                    s["install_log"] += "  \u2713 WsaClient.exe patched successfully."
                except Exception as e:
                    await step_failed_text(1, str(e)[:40])
                    s["install_log"] += f"  \u26a0 Could not patch: {e}"

        s["install_progress"] = 0.5
        await self._update_ui()

        # Step 3: Patch AppxManifest.xml (pre-patched with WSARepair.exe File= attribute)
        await step_checking(2)
        s["install_log"] += "\n  Copying AppxManifest.xml..."
        s["install_sub_status"][2]["detail"] = "Checking patched manifest..."
        await self._update_ui()
        custom_manifest = resource_path(os.path.join("assets", "AppxManifest.xml"))
        target_manifest = os.path.join(self.WSA_DEST_DIR, "AppxManifest.xml")
        if os.path.exists(custom_manifest):
            if not os.path.exists(target_manifest):
                shutil.copy2(custom_manifest, target_manifest)
                await step_done_text(2, "AppxManifest.xml copied")
                s["install_log"] += "  \u2713 AppxManifest.xml copied (patched for WSARepair)."
            else:
                shutil.copy2(custom_manifest, target_manifest)
                await step_done_text(2, "AppxManifest.xml patched")
                s["install_log"] += "  \u2713 AppxManifest.xml patched (File=WSARepair.exe)."
        else:
            await step_done_text(2, "No manifest — skipped")
            s["install_log"] += "  No custom AppxManifest.xml found, skipping."

        # Step 4: Copy WSARepair.exe to CustomInstall/
        await step_checking(3)
        s["install_log"] += "\n  Installing WSARepair proxy..."
        s["install_sub_status"][3]["detail"] = "Checking proxy..."
        await self._update_ui()
        repair_proxy = resource_path(os.path.join("assets", "WSARepair.exe"))
        custom_install_dir = os.path.join(self.WSA_DEST_DIR, "CustomInstall")
        if os.path.exists(repair_proxy):
            os.makedirs(custom_install_dir, exist_ok=True)
            target_repair = os.path.join(custom_install_dir, "WSARepair.exe")
            try:
                shutil.copy2(repair_proxy, target_repair)
                await step_done_text(3, "WSARepair installed")
                s["install_log"] += "  \u2713 WSARepair.exe installed to CustomInstall\\."
            except Exception as e:
                await step_failed_text(3, str(e)[:40])
                s["install_log"] += f"  \u26a0 Could not copy WSARepair.exe: {e}"
        else:
            await step_done_text(3, "No proxy — skipped")
            s["install_log"] += "  WSARepair.exe not found in assets, skipping."

        s["install_progress"] = 0.55
        await self._update_ui()

        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        # PHASE 5: Run Installer  (3 tracker steps, 3 sub-steps)
        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        await begin_phase(4, "Run Installer", [
            "Cleanup temp files",
            "Verify Run.bat exists",
            "Execute installer script",
        ])

        # Step 1: Cleanup temp files
        await step_checking(0)
        s["install_log"] += "\n  Cleaning temp files..."
        await self._update_ui()
        if os.path.exists(src) and os.path.abspath(src) != os.path.abspath(self.WSA_DEST_DIR):
            shutil.rmtree(src, ignore_errors=True)
        temp_extract_dir = os.path.join(self.OUT_ASSET_DIR, "temp_extract")
        if os.path.exists(temp_extract_dir) and os.path.abspath(temp_extract_dir) != os.path.abspath(self.WSA_DEST_DIR):
            shutil.rmtree(temp_extract_dir, ignore_errors=True)
        await step_done_text(0, "Cleaned")
        s["install_log"] += "  \u2713 Temp files cleaned."

        # Step 2: Verify Run.bat exists
        await step_checking(1)
        s["install_log"] += "\n  Verifying Run.bat..."
        await self._update_ui()
        bat_path = os.path.join(self.WSA_DEST_DIR, "Run.bat")
        if not os.path.exists(bat_path):
            await step_failed_text(1, "Run.bat not found")
            s["install_log"] += f"  \u2717 Run.bat not found in {self.WSA_DEST_DIR}"
            s["installing"] = False
            await self._update_ui()
            return
        await step_done_text(1, "Run.bat found")

        # Step 3: Execute installer script
        await step_checking(2)
        s["install_log"] += "\n  Running installer..."
        s["install_sub_status"][2]["detail"] = "Executing Run.bat..."
        await self._update_ui()

        # Restore callback: fires BEFORE "press any key" sends Enter
        async def _restore_backup_callback():
            backup_src = _wsa_backup_path()
            backup_dst = _wsa_data_path()
            if not os.path.isdir(backup_src):
                s["install_log"] += "\n  No repair backup found, skipping restore."
                await self._update_ui()
                return
            s["install_log"] += f"\n  Restoring backup from:\n    {backup_src}"
            s["install_log"] += f"\n    → {backup_dst}"
            await self._update_ui()
            try:
                os.makedirs(backup_dst, exist_ok=True)
                # Calculate total size for progress
                total_size = 0
                file_count = 0
                for dirpath, dirnames, filenames in os.walk(backup_src):
                    for fn in filenames:
                        fp = os.path.join(dirpath, fn)
                        total_size += os.path.getsize(fp)
                        file_count += 1
                copied = 0
                start_time = time.time()
                for dirpath, dirnames, filenames in os.walk(backup_src):
                    rel = os.path.relpath(dirpath, backup_src)
                    dest_dir = os.path.join(backup_dst, rel) if rel else backup_dst
                    os.makedirs(dest_dir, exist_ok=True)
                    for fn in filenames:
                        src_fp = os.path.join(dirpath, fn)
                        dst_fp = os.path.join(dest_dir, fn)
                        shutil.copy2(src_fp, dst_fp)
                        copied += os.path.getsize(src_fp)
                        if total_size > 0 and file_count > 10:
                            pct = copied / total_size
                            speed = copied / max(time.time() - start_time, 0.001)
                            remaining = (total_size - copied) / max(speed, 1)
                            s["install_log"] += f"\n  Restoring: {pct:.0%} | {speed/1024/1024:.1f} MB/s | ETA {remaining:.0f}s"
                            await self._update_ui()
                s["install_log"] += f"\n  \u2713 Backup restored ({file_count} files)."
                await self._update_ui()
                # Cleanup backup after successful restore
                shutil.rmtree(backup_src, ignore_errors=True)
                s["install_log"] += "  Repair backup cleaned up."
                await self._update_ui()
            except Exception as ex:
                s["install_log"] += f"\n  \u26a0 Backup restore error: {ex}"
                await self._update_ui()

        # Sub-step 3a: stream output
        # Sub-step 3b: auto-enter if prompt (with pre-enter callback for backup restore)
        # Sub-step 3c: detect success/failure
        success = await self._stream_command_v2(
            ["cmd.exe", "/c", "Run.bat"],
            "install_log",
            cwd=self.WSA_DEST_DIR,
            success_markers=["all done", "installation completed"],
            pre_enter_callback=_restore_backup_callback,
        )

        if success:
            await step_done_text(2, "Completed")
            s["install_log"] += "  \u2713 Installer finished."
        else:
            await step_failed_text(2, "Failed or timed out")
            s["install_log"] += "  \u2717 Installer might have failed or timed out."

        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        # PHASE 6: Finalize  (2 tracker steps, 0 sub-steps)
        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        await begin_phase(5, "Finalize", [
            "Check result",
            "Mark complete",
        ])

        # Step 1: Check result
        await step_checking(0)
        await self._update_ui()
        if success:
            await step_done_text(0, "Success")
            s["install_progress"] = 1.0
            s["install_done"] = True
            s["install_log"] += "\n  \u2713 WSA Base installation successfully completed."
        else:
            await step_failed_text(0, "Installation failed")
            s["install_log"] += "\n  \u2717 Installation might have failed or timed out."

        # Step 2: Mark complete
        await step_checking(1)
        await self._update_ui()
        s["installing"] = False
        await step_done_text(1, "Done")
        await self._update_ui()

    async def add_playStore(self):
        """Adds Play Store support to WSA — 7-phase visualizer (18 tracker steps)."""
        self._scan_cancelled = False
        s = self.state
        s["ps_installing"] = True
        s["ps_log"] = "Starting Google Play integration..."
        s["ps_progress"] = 0.05
        s["ps_done"] = False
        dst = CONFIG.WSA_ROOT

        # ── Helper functions ─────────────────────────────────────────────
        async def begin_phase_ps(phase_idx, title, step_labels):
            s["ps_phase"] = phase_idx
            s["ps_phase_title"] = title
            s["ps_sub_status"] = [{"label": lbl, "status": "pending", "detail": ""} for lbl in step_labels]
            await self._update_ui()

        async def step_checking_ps(idx):
            s["ps_sub_status"][idx]["status"] = "checking"
            s["ps_sub_status"][idx]["detail"] = "Processing..."
            await self._update_ui()

        async def step_done_ps(idx):
            s["ps_sub_status"][idx]["status"] = "done"
            s["ps_sub_status"][idx]["detail"] = "Done"
            await self._update_ui()

        async def step_failed_ps(idx):
            s["ps_sub_status"][idx]["status"] = "failed"
            s["ps_sub_status"][idx]["detail"] = "Failed"
            await self._update_ui()

        async def step_done_text_ps(idx, text):
            s["ps_sub_status"][idx]["status"] = "done"
            s["ps_sub_status"][idx]["detail"] = text
            await self._update_ui()

        async def step_failed_text_ps(idx, text):
            s["ps_sub_status"][idx]["status"] = "failed"
            s["ps_sub_status"][idx]["detail"] = text
            await self._update_ui()

        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        # PHASE 1: Check Prerequisites  (3 tracker steps, 6 sub-steps)
        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        await begin_phase_ps(0, "Check Prerequisites", [
            "Ensure WSA running",
            "Check Play Store support",
            "Check Developer Mode",
        ])

        # Step 1: Ensure WSA running
        await step_checking_ps(0)
        s["ps_log"] += "\n  Checking if WSA is running..."
        await self._update_ui()
        wsa_running = await self._ensure_wsa_running("ps_log")
        if not wsa_running:
            await step_failed_text_ps(0, "WSA failed to start")
            s["ps_log"] += "\n  \u2717 Failed to start WSA. Please start it manually."
            s["ps_installing"] = False
            await self._update_ui()
            return
        await step_done_text_ps(0, "WSA running")
        s["ps_progress"] = 0.10
        await self._update_ui()

        # Step 2: Check Play Store support
        await step_checking_ps(1)
        s["ps_log"] += "\n  Checking if Play Store already installed..."
        await self._update_ui()
        supported = await self._check_playstore_support()
        if supported:
            await step_done_text_ps(1, "Play Store found!")
            s["ps_log"] += "\n  \u2713 Google Play support is already present!"
            s["ps_progress"] = 1.0
            s["ps_done"] = True
            s["ps_installing"] = False
            await self._update_ui()
            return
        await step_done_text_ps(1, "Not found")

        # Step 3: Check Developer Mode
        await step_checking_ps(2)
        s["ps_log"] += "\n  Checking Developer Mode..."
        s["ps_sub_status"][2]["detail"] = "Port 58526 check..."
        await self._update_ui()
        ready = await self._check_wsa_dev_ready("ps_log")
        if ready:
            await step_done_text_ps(2, "Dev Mode ON")
        else:
            await step_done_text_ps(2, "Dev Mode OFF")
        s["ps_progress"] = 0.15
        await self._update_ui()

        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        # PHASE 2: Enable Dev Mode  (3 tracker steps, 9 sub-steps)
        # SKIPPED if Dev Mode already ON
        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        if not ready:
            await begin_phase_ps(1, "Enable Dev Mode", [
                "Kill WSA processes",
                "Patch settings.dat",
                "Restart + verify Dev Mode",
            ])

            # Step 4: Kill WSA processes
            await step_checking_ps(0)
            s["ps_log"] += "\n  Developer Mode is OFF. Patching via settings.dat..."
            await self._update_ui()
            await self._kill_wsa_completely("ps_log")
            await step_done_text_ps(0, "Processes killed")
            s["ps_log"] += "  \u2713 WSA processes killed."

            # Step 5: Patch settings.dat
            await step_checking_ps(1)
            s["ps_log"] += "\n  Patching Developer Mode via settings.dat..."
            s["ps_sub_status"][1]["detail"] = "Copying patched file..."
            await self._update_ui()
            patched = await self._patch_wsa_settings_dat("ps_log")
            if not patched:
                await step_failed_text_ps(1, "Patch failed")
                s["ps_log"] += "\n  [ACTION REQUIRED] Settings patch failed. Please enable 'Developer Mode' manually in WSA Settings."
                s["ps_installing"] = False
                await self._update_ui()
                return
            await step_done_text_ps(1, "Settings patched")
            s["ps_log"] += "  \u2713 Settings.dat patched."

            # Step 6: Restart + verify Dev Mode
            await step_checking_ps(2)
            s["ps_log"] += "\n  Restarting WSA..."
            s["ps_sub_status"][2]["detail"] = "Starting WSA..."
            await self._update_ui()
            await self._ensure_wsa_running("ps_log")
            s["ps_sub_status"][2]["detail"] = "Verifying port 58526..."
            await self._update_ui()
            ready = await self._check_wsa_dev_ready("ps_log")
            if not ready:
                await step_failed_text_ps(2, "Dev Mode still OFF")
                s["ps_log"] += "\n  \u2717 Port 58526 still not responding. Please check WSA screen manually."
                s["ps_installing"] = False
                await self._update_ui()
                return
            await step_done_text_ps(2, "Dev Mode active")
            s["ps_log"] += "\n  \u2713 Developer Mode is ACTIVE."
            s["ps_progress"] = 0.25
            await self._update_ui()
        else:
            s["ps_log"] += "\n  \u2713 Developer Mode is already ACTIVE."
            await self._update_ui()

        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        # PHASE 3: Connect ADB  (1 tracker step, 3 sub-steps)
        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        await begin_phase_ps(2, "Connect ADB", [
            "ADB bridge connect",
        ])

        # Step 7: ADB Connect
        await step_checking_ps(0)
        s["ps_log"] += "\n  Connecting to WSA ADB bridge..."
        s["ps_sub_status"][0]["detail"] = "Establishing connection..."
        await self._update_ui()
        connected = await self._adb_connect_loop("ps_log")
        if not connected:
            await step_failed_text_ps(0, "ADB connect failed")
            s["ps_installing"] = False
            await self._update_ui()
            return
        await step_done_text_ps(0, "ADB connected")
        s["ps_progress"] = 0.30
        await self._update_ui()

        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        # PHASE 4: Prepare Package  (3 tracker steps, 9 sub-steps)
        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        await begin_phase_ps(3, "Prepare Package", [
            "Re-check Play Store",
            "Locate package",
            "Verify package files",
        ])

        # Step 8: Re-check Play Store support
        await step_checking_ps(0)
        s["ps_log"] += "\n  Verifying Play Store support via ADB..."
        s["ps_sub_status"][0]["detail"] = "ADB pm list packages..."
        await self._update_ui()
        supported = await self._check_playstore_support()
        if supported:
            await step_done_text_ps(0, "Play Store found!")
            s["ps_log"] += "\n  \u2713 Google Play support verified! Performing final cleanup..."
            await self._final_cleanup_sequence("ps_log")
            s["ps_progress"] = 1.0
            s["ps_done"] = True
            s["ps_installing"] = False
            await self._update_ui()
            return
        await step_done_text_ps(0, "Not found")

        # Step 9: Locate package
        await step_checking_ps(1)
        s["ps_log"] += "\n  Google Play missing. Preparing fresh integration package..."
        s["ps_sub_status"][1]["detail"] = "Checking cached archive..."
        await self._update_ui()
        src = None
        cached = self._find_cached_archive("gapps")
        if cached:
            s["ps_log"] += f"\n  Found cached package: {cached.name}. Replacing existing files..."
            s["ps_sub_status"][1]["detail"] = f"Extracting {cached.name}..."
            await self._update_ui()
            temp_patch_target = pathlib.Path(self.WSA_DEST_DIR)
            ok = await self.extract_7z(cached, temp_patch_target, 'ps_log', force=True)
            if not ok:
                await step_failed_text_ps(1, "Extraction failed")
                s["ps_installing"] = False
                await self._update_ui()
                return
            src = str(temp_patch_target)
            await step_done_text_ps(1, "Archive extracted")
        else:
            s["ps_sub_status"][1]["detail"] = "Checking folder..."
            await self._update_ui()
            folder_path = os.path.join(self.OUT_ASSET_DIR, "WSA PlayStore Package")
            if os.path.exists(folder_path):
                src = folder_path
            else:
                folder_path2 = resource_path(os.path.join("assets", "WSA PlayStore Package"))
                if os.path.exists(folder_path2):
                    src = folder_path2

            if src is None:
                await step_done_text_ps(1, "No package found")
                s["ps_log"] += "\n  No Play Store package found. Showing download selection..."
                s["ps_installing"] = False
                s["show_download"] = "gapps"
                await self._update_ui()
                return
            await step_done_text_ps(1, "Folder found")

        # Step 10: Verify package files
        await step_checking_ps(2)
        s["ps_sub_status"][2]["detail"] = "Reading filelist.txt..."
        await self._update_ui()
        filelist_path = os.path.join(src, "filelist.txt")
        if os.path.exists(filelist_path):
            s["ps_log"] += "\n  Verifying package files..."
            await self._update_ui()
            with open(filelist_path, "r") as f:
                required = [line.strip() for line in f if line.strip()]
            s["ps_sub_status"][2]["detail"] = f"Checking {len(required)} files..."
            await self._update_ui()
            missing = [item for item in required if not os.path.exists(os.path.join(src, item))]
            if missing:
                await step_failed_text_ps(2, f"Missing: {', '.join(missing[:3])}")
                s["ps_log"] += f"\n  \u2717 CRITICAL: Files missing in package: {', '.join(missing[:3])}..."
                s["ps_log"] += "\n  Tip: Ensure the application was bundled correctly."
                s["ps_installing"] = False
                await self._update_ui()
                return
            await step_done_text_ps(2, f"All {len(required)} files present")
            s["ps_log"] += "  Verification successful \u2713"
        else:
            await step_done_text_ps(2, "No filelist.txt")
        s["ps_progress"] = 0.40
        await self._update_ui()

        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        # PHASE 5: Apply Patches  (4 tracker steps, 12 sub-steps)
        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        await begin_phase_ps(4, "Apply Patches", [
            "Kill WSA processes",
            "Merge Play Store files",
            "Patch system files",
            "Verify destination folder",
        ])

        # Step 11: Kill WSA processes
        await step_checking_ps(0)
        s["ps_log"] += "\n  Killing WSA processes..."
        await self._update_ui()
        await self._kill_wsa_completely("ps_log")
        await step_done_text_ps(0, "Processes killed")
        s["ps_log"] += "  \u2713 WSA processes killed."

        # Step 12: Merge Play Store files
        await step_checking_ps(1)
        s["ps_log"] += "\n  Merging Play Store package into unified destination..."
        s["ps_sub_status"][1]["detail"] = "Copying files..."
        await self._update_ui()
        os.makedirs(self.WSA_DEST_DIR, exist_ok=True)

        def copy_play_files():
            if os.path.abspath(src) == os.path.abspath(self.WSA_DEST_DIR):
                return
            for root, dirs, files in os.walk(src):
                rel_path = os.path.relpath(root, src)
                target_root = os.path.join(self.WSA_DEST_DIR, rel_path)
                os.makedirs(target_root, exist_ok=True)
                for file in files:
                    if file.lower() == "run.bat":
                        continue
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(target_root, file)
                    for attempt in range(5):
                        try:
                            shutil.copy2(src_file, dst_file)
                            break
                        except Exception as err:
                            if attempt == 4:
                                self.state["ps_log"] += f"\n  \u26A0 FAILED COPY {file} (skipping)"
                                break
                            time.sleep(1)

        await asyncio.to_thread(copy_play_files)
        await step_done_text_ps(1, "Files merged")
        s["ps_log"] += "  \u2713 Files merged."

        # Step 13: Patch system files
        await step_checking_ps(2)
        s["ps_sub_status"][2]["detail"] = "Patching Run.bat..."
        s["ps_log"] += "\n  Patching system files..."
        await self._update_ui()

        # Sub-step 13a: Patch Run.bat
        custom_run_bat = resource_path(os.path.join("assets", "Run.bat"))
        if os.path.exists(custom_run_bat):
            shutil.copy2(custom_run_bat, os.path.join(self.WSA_DEST_DIR, "Run.bat"))
            s["ps_sub_status"][2]["detail"] = "Run.bat patched"
            await self._update_ui()

        # Sub-step 13b: Patch WsaClient.exe
        s["ps_sub_status"][2]["detail"] = "Patching WsaClient.exe..."
        await self._update_ui()
        await self._patch_wsa_client_exe("ps_log")

        # Sub-step 13c: Deploy ps.ico
        s["ps_sub_status"][2]["detail"] = "Deploying ps.ico..."
        await self._update_ui()
        ico_src = resource_path(os.path.join("assets", "ps.ico"))
        if os.path.exists(ico_src):
            shutil.copy2(ico_src, os.path.join(self.WSA_DEST_DIR, "ps.ico"))
            s["ps_log"] += "  Copied ps.ico."

        await step_done_text_ps(2, "All patches applied")
        s["ps_log"] += "  Files patched successfully \u2713"

        # Step 14: Verify destination folder
        await step_checking_ps(3)
        s["ps_sub_status"][3]["detail"] = "Verifying folder structure..."
        await self._update_ui()
        if not self._verify_wsa_folder(self.WSA_DEST_DIR):
            await step_done_text_ps(3, "Verification warning")
            s["ps_log"] += "\n  \u26A0 WARNING: Destination folder verification failed after merge."
        else:
            await step_done_text_ps(3, "Folder verified")
        s["ps_progress"] = 0.60
        await self._update_ui()

        # Cleanup temp source folder
        if os.path.exists(src) and os.path.abspath(src) != os.path.abspath(self.WSA_DEST_DIR):
            shutil.rmtree(src, ignore_errors=True)

        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        # PHASE 6: Run Installer  (2 tracker steps, 5 sub-steps)
        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        await begin_phase_ps(5, "Run Installer", [
            "Run integration script",
            "Deploy shortcut + restart",
        ])

        # Step 15: Run integration script
        await step_checking_ps(0)
        s["ps_log"] += "\n  Running Play Store integration script..."
        s["ps_sub_status"][0]["detail"] = "Checking Run.bat..."
        await self._update_ui()
        bat_path = os.path.join(self.WSA_DEST_DIR, "Run.bat")
        if not os.path.exists(bat_path):
            await step_failed_text_ps(0, "Run.bat not found")
            s["ps_log"] += f"  \u2717 Run.bat not found in {self.WSA_DEST_DIR}"
            s["ps_installing"] = False
            await self._update_ui()
            return
        s["ps_sub_status"][0]["detail"] = "Executing Run.bat..."
        await self._update_ui()
        success = await self._stream_command_v2(
            ["cmd.exe", "/c", "Run.bat"],
            "ps_log",
            cwd=self.WSA_DEST_DIR,
            success_markers=["all done", "installation completed"]
        )
        if success:
            await step_done_text_ps(0, "Script completed")
            s["ps_log"] += "  \u2713 Patch installed."
        else:
            await step_failed_text_ps(0, "Script failed or timed out")
            s["ps_log"] += "  \u2717 Patch installation failed."

        # Step 16: Deploy shortcut + restart WSA
        if success:
            await step_checking_ps(1)
            s["ps_sub_status"][1]["detail"] = "Deploying Play Store shortcut..."
            await self._update_ui()
            try:
                shortcut_src = resource_path(os.path.join("assets", "Play Store.lnk"))
                start_menu_path = os.path.join(os.environ.get('APPDATA', ''), r"Microsoft\Windows\Start Menu\Programs")
                if os.path.exists(shortcut_src) and os.path.exists(start_menu_path):
                    target_lnk = os.path.join(start_menu_path, "Play Store.lnk")
                    shutil.copy2(shortcut_src, target_lnk)
                    s["ps_log"] += "  \u2713 Play Store shortcut added to Start Menu."
            except:
                pass
            s["ps_sub_status"][1]["detail"] = "Restarting WSA..."
            await self._update_ui()
            await self._ensure_wsa_running("ps_log")
            await step_done_text_ps(1, "WSA restarted")
            s["ps_progress"] = 0.80
            await self._update_ui()
        else:
            await step_failed_text_ps(1, "Skipped (script failed)")

        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        # PHASE 7: Finalize  (2 tracker steps, 7 sub-steps)
        # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
        await begin_phase_ps(6, "Finalize", [
            "Final verification",
            "Cleanup + mark complete",
        ])

        # Step 17: Final verification
        await step_checking_ps(0)
        s["ps_log"] += "\n  Final verification..."
        s["ps_sub_status"][0]["detail"] = "Reconnecting ADB..."
        await self._update_ui()
        await self._adb_connect_loop("ps_log")
        s["ps_sub_status"][0]["detail"] = "Checking Play Store via ADB..."
        await self._update_ui()
        if await self._check_playstore_support():
            await step_done_text_ps(0, "Play Store verified!")
            s["ps_log"] += "  \u2713 Google Play Store is now fully supported!"
            s["ps_progress"] = 1.0
            s["ps_done"] = True
        else:
            await step_done_text_ps(0, "Not yet detected")
            s["ps_log"] += "  \u2139 Patch finished, but Play Store not yet detected by ADB."
            s["ps_log"] += "  You may need to open the WSA Settings app once to initialize."
            s["ps_done"] = True
        await self._update_ui()

        # Step 18: Cleanup + mark complete
        await step_checking_ps(1)
        s["ps_sub_status"][1]["detail"] = "Cleaning up packages..."
        s["ps_log"] += "\n  Cleaning up extracted packages..."
        await self._update_ui()
        basic_pkg = os.path.join(self.OUT_ASSET_DIR, "WSA Basic Package")
        ps_pkg = os.path.join(self.OUT_ASSET_DIR, "WSA PlayStore Package")
        if os.path.exists(basic_pkg): shutil.rmtree(basic_pkg, ignore_errors=True)
        if os.path.exists(ps_pkg): shutil.rmtree(ps_pkg, ignore_errors=True)

        # Cleanup repair backup if it exists (no longer needed after successful Play Store install)
        repair_backup = _wsa_backup_path()
        if os.path.isdir(repair_backup):
            try:
                shutil.rmtree(repair_backup, ignore_errors=True)
                s["ps_log"] += "\n  Repair backup cleaned up."
            except Exception:
                pass

        if await self._check_playstore_support():
            s["ps_log"] += "\n  Integration Verified. Finalizing..."
            await self._final_cleanup_sequence("ps_log")
            s["ps_log"] += "  Cleanup Complete. System is ready."

        await step_done_text_ps(1, "Complete")
        s["ps_installing"] = False
        await self._update_ui()

    async def complete(self):
        """Finishes the setup."""
        self.state["current_step"] = 4
        await self._update_ui()

    # --- Private Helpers ---

    async def _check_and_extract_bundle(self):
        """Detects and extracts bundle (any extension configured via BUNDLE_NAME) with real-time UI logging."""
        out_asset = pathlib.Path(self.OUT_ASSET_DIR)
        
        bundle_name_cfg = getattr(self, "_cfg_cache", None)
        if bundle_name_cfg is None:
            try:
                bundle_name_cfg = getattr(CONFIG, "config", {}).get("BUNDLE_NAME", getattr(CONFIG, "BUNDLE_NAME", ""))
            except Exception:
                bundle_name_cfg = ""
        if not bundle_name_cfg:
            bundle_name_cfg = "bundle.wsa"
        
        # Search for the configured bundle (any extension) in out_asset.
        # We first try the exact configured name; if missing, fall back to legacy bundle.7z / bundle.zip
        # so older packages still work.
        candidate_names = [bundle_name_cfg, f"bundle{os.path.splitext(bundle_name_cfg)[1]}"]
        candidate_names += ["bundle.7z", "bundle.zip"]
        seen = set()
        bundle_path = None
        for name in candidate_names:
            if not name or name in seen:
                continue
            seen.add(name)
            candidate = out_asset / name
            if candidate.exists():
                bundle_path = candidate
                break
        
        if bundle_path and bundle_path.exists():
            self.state["log"] = f"[\u2139] Bundled package found: {bundle_path.name}"
            await self._update_ui()
            
            try:
                # Create cache if not exists
                self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
                
                # Use tar.exe with -v for verbose output to show progress in UI
                process = await self._create_subprocess(
                    "tar.exe", "-xvf", str(bundle_path), "-C", str(self.CACHE_DIR),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT,
                    creationflags=0x08000000 if sys.platform == "win32" else 0
                )
                
                count = 0
                while True:
                    line = await process.stdout.readline()
                    if not line: break
                    
                    line_text = line.decode(errors='replace').strip()
                    if line_text:
                        # Show extraction progress in UI
                        display_line = line_text if len(line_text) < 50 else "..." + line_text[-47:]
                        self.state["log"] = f"Extracting Bundle: {display_line}"
                        count += 1
                        if count % 20 == 0:
                            await self._update_ui()
                
                await process.wait()
                self.state["log"] = "[\u2713] Bundle extracted successfully. Finalizing..."
                await self._update_ui()
                
                # Delete the bundle archive after extraction to save space as requested
                try:
                    os.remove(bundle_path)
                    self.state["log"] = "[\u2713] Bundle archive removed to save space."
                except:
                    pass
                
                await asyncio.sleep(1)
            except Exception as e:
                self.state["log"] = f"[\u26A0] Bundle extraction failed: {e}"
            
            self.state["log"] = "Starting WSA system scan..."
            await self._update_ui()
            return

    async def _final_cleanup_sequence(self, log_key):
        """Standardized cleanup of all temporary extracted folders and the download cache."""
        s = self.state
        s[log_key] += "\n[CLEANUP] Purging temporary assets..."
        
        # 1. Clean extracted package folders
        folders_to_clean = [
            os.path.join(self.OUT_ASSET_DIR, "WSA Basic Package"),
            os.path.join(self.OUT_ASSET_DIR, "WSA PlayStore Package"),
            os.path.join(self.OUT_ASSET_DIR, "temp_extract")
        ]
        for pkg in folders_to_clean:
            if os.path.exists(pkg): 
                shutil.rmtree(pkg, ignore_errors=True)
        
        # 2. Clean Cache Folder (Aggressive cleanup to save space)
        if os.path.exists(self.CACHE_DIR):
            try:
                shutil.rmtree(self.CACHE_DIR, ignore_errors=True)
                s[log_key] += "\n\u2713 Cache directory purged successfully."
            except Exception as e:
                self._log(log_key, f"Warning: Could not fully purge cache: {e}")
        
        await self._update_ui()

    async def _ensure_wsa_running(self, log_key):
        s = self.state
        self.state[log_key] += "\nChecking if WSA is running..."
        await self._update_ui()

        for i in range(3):
            # Check for WsaClient process
            process = await self._create_subprocess(
                "tasklist",
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                creationflags=0x08000000
            )
            stdout, _ = await process.communicate()
            if b"WsaClient.exe" in stdout or b"WindowsSubsystemForAndroid" in stdout:
                self.state[log_key] += "\n\u2713 WSA is running."
                await self._update_ui()
                return True
            
            self.state[log_key] += f"\n\u2139 Starting WSA... (attempt {i+1}/3)"
            
            await self._update_ui()
            await self._create_subprocess(
                "powershell.exe", "-Command", "Start-Process 'wsa://system'",
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
                creationflags=0x08000000
            )
            await asyncio.sleep(12)
        
        return False

    async def _check_wsa_dev_ready(self, log_key=None):
        """Perform 3 connection attempts to check if WSA is ready for ADB."""
        for attempt in range(3):
            try:
                # Check port 58526
                reader, writer = await asyncio.open_connection("127.0.0.1", CONFIG.WSA_PORT)
                writer.close()
                await writer.wait_closed()
                return True
            except:
                if log_key:
                    self.state[log_key] += f"\n\u2139 Waiting for Developer Mode... (retry {attempt+1}/3)"
                    await self._update_ui()
                if attempt < 2:
                    await asyncio.sleep(6)
        return False

    async def _check_playstore_support(self):
        """Robustly check if Play Store is supported via ADB, with retries and auto-cleanup."""
        if not os.path.exists(self.ADB_PATH):
            return False
            
        # 1. Ensure WSA is actually running first
        await self._ensure_wsa_running("ps_log")
        
        # 2. Retry loop (3 attempts) as WSA takes time to initialize the PM service
        for attempt in range(3):
            try:
                # Precisely check for com.android.vending (Google Play Store)
                process = await self._create_subprocess(
                    self.ADB_PATH, "-s", CONFIG.WSA_DEVICE, "shell", "pm", "list", "packages", "com.android.vending",
                    stdin=asyncio.subprocess.DEVNULL,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    creationflags=0x08000000
                )
                stdout, _ = await process.communicate()
                result = stdout.decode().lower()
                
                # Match strictly against the package name
                if "package:com.android.vending" in result:
                    self.state["ps_log"] += "\n\u2713 Google Play Store package detected via ADB."
                    print("[PS_LOG] Google Play Store package detected via ADB.")
                    
                    # Automated final cleanup once confirmed
                    await self._final_cleanup_sequence("ps_log")
                    return True
            except:
                pass
            
            if attempt < 2:
                await asyncio.sleep(2) # Wait before retry
                
        return False

    async def _adb_connect_loop(self, log_key):
        if not os.path.exists(self.ADB_PATH):
            self.state[log_key] += "\n\u2717 ADB not found in assets."
            return False

        # Attempt connection ONCE
        self.state[log_key] += "\n\u2139 Establishing initial ADB connection..."
        await self._create_subprocess(
            self.ADB_PATH, "connect", CONFIG.WSA_DEVICE,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            creationflags=0x08000000 if sys.platform == "win32" else 0
        )
        await asyncio.sleep(2)

        for i in range(15):
            p_dev = await self._create_subprocess(
                self.ADB_PATH, "devices",
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                creationflags=0x08000000 if sys.platform == "win32" else 0
            )
            o_dev, _ = await p_dev.communicate()
            result = o_dev.decode().lower()

            if f"{CONFIG.WSA_DEVICE}\tdevice" in result:
                self.state[log_key] += "\n\u2713 ADB Connected and Authorized."
                return True

            # ---------------- UNAUTHORIZED ----------------
            if f"{CONFIG.WSA_DEVICE}\tunauthorized" in result:
                self.state[log_key] += f"\n\u26A0 ADB Unauthorized ({i+1}/15) \u2192 Awaiting authorization popup..."
                await self._update_ui()
                
                # Periodically attempt automated authorization if the popup is visible
                if i % 3 == 0:
                    await self._automate_adb_authorization()
                
                await asyncio.sleep(3)
                continue

            # ---------------- OFFLINE/NO DEVICE ----------------
            self.state[log_key] += f"\n\u2139 Waiting for WSA heart-beat... ({i+1}/15)"
            await self._update_ui()
            
            # If completely offline, maybe try one more connect just in case
            if i % 5 == 0 and i > 0:
                 await self._create_subprocess(self.ADB_PATH, "connect", CONFIG.WSA_DEVICE, creationflags=0x08000000)
            
            await asyncio.sleep(3)
        
        return False

    async def _automate_adb_authorization(self):
        """Specifically handle the 'Allow USB debugging?' popup."""
        try:
            # Block input during this brief automation
            try: ctypes.windll.user32.BlockInput(True)
            except: pass
            
            desktop = Desktop(backend="uia")
            popup = None
            # Search for the specific authorization dialog
            for w in desktop.windows():
                if "Allow USB debugging" in w.window_text():
                    popup = w
                    break
            
            if popup:
                popup.set_focus()
                await asyncio.sleep(0.8)
                
                # Check for 'Always allow' checkbox using UIA
                try:
                    # Find checkbox that contains 'Always allow' in its title
                    checkbox = popup.child_window(title_re=".*Always allow.*", control_type="CheckBox")
                    if checkbox.exists():
                        checkbox.click_input()
                        await asyncio.sleep(0.4)
                except:
                    pass

                # Find and click the 'Allow' or 'OK' button
                try:
                    # Look for buttons named Allow or OK
                    for btn_name in ["Allow", "OK"]:
                        btn = popup.child_window(title=btn_name, control_type="Button")
                        if btn.exists():
                            btn.click_input()
                            print(f"[INFO] Clicked {btn_name} button.")
                            return True
                except:
                    pass
                
                # Absolute fallback: Enter key
                pyautogui.press('enter')
                print("[INFO] ADB Authorization popup handled via fallback.")
                return True
        except Exception as e:
            print(f"[DEBUG] ADB Popup automation error: {e}")
        finally:
            try: ctypes.windll.user32.BlockInput(False)
            except: pass
        return False

    async def _kill_wsa_completely(self, log_key):
        self.state[log_key] += "\nForcefully killing all WSA processes to release file locks..."
        await self._update_ui()
        
        # 1. Shut down gracefully first
        try:
            proc = await self._create_subprocess("WsaClient.exe", "/shutdown", stdin=asyncio.subprocess.DEVNULL, creationflags=0x08000000 if sys.platform == "win32" else 0)
            await asyncio.wait_for(proc.wait(), timeout=5)
        except:
            pass
        await asyncio.sleep(1)

        # 2. Kill any PowerShell processes running Install.ps1 (Crucial for releasing locks)
        try:
            self.state[log_key] += "\nTerminating background install scripts..."
            kill_ps_cmd = 'Get-CimInstance Win32_Process | Where-Object { ($_.Name -match "powershell.exe" -or $_.Name -match "pwsh.exe") -and $_.CommandLine -match "Install.ps1" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }'
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", kill_ps_cmd],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           creationflags=0x08000000 if sys.platform == "win32" else 0)
        except:
            pass

        # 3. Specific WSA targets to resolve "File in use" errors
        targets = [
            "WsaClient.exe", "WindowsSubsystemForAndroid.exe", "adb.exe", 
            "vmmemWSA.exe", "WsaService.exe", "cmd.exe"
        ]
        creation_flags = 0x08000000 if sys.platform == "win32" else 0
        
        for target in targets:
            try:
                # If target is cmd.exe, only kill it if it's running Run.bat
                if target == "cmd.exe":
                    kill_cmd_bat = 'Get-CimInstance Win32_Process | Where-Object { $_.Name -match "cmd.exe" -and $_.CommandLine -match "Run.bat" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }'
                    subprocess.run(["powershell.exe", "-NoProfile", "-Command", kill_cmd_bat],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                   creationflags=0x08000000 if sys.platform == "win32" else 0)
                else:
                    proc = await self._create_subprocess(
                        "taskkill", "/F", "/IM", target, "/T",
                        stdin=asyncio.subprocess.DEVNULL,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        creationflags=creation_flags
                    )
                    await proc.wait() 
            except:
                pass
        
        # Give OS more time to release file handles
        await asyncio.sleep(2) 

    async def _patch_wsa_settings_dat(self, log_key):
        """Patch WSA settings.dat to permanently enable Developer Mode.
        Copies pre-patched settings.dat from assets/ over the user's file.
        WSA must be killed first for the file to be unlockable."""
        s = self.state
        s[log_key] += "\nPatching Developer Mode via settings.dat..."
        await self._update_ui()

        # 1. Locate user's settings.dat
        user_settings = os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            r"Packages\MicrosoftCorporationII.WindowsSubsystemForAndroid_8wekyb3d8bbwe",
            "Settings", "settings.dat"
        )
        if not os.path.exists(user_settings):
            s[log_key] += "\nWSA settings.dat not found. Is WSA installed?"
            return False

        # 2. Locate our patched settings.dat
        patched = resource_path(os.path.join("assets", "settings.dat"))
        if not os.path.exists(patched):
            s[log_key] += "\nPatched settings.dat not found in assets."
            return False

        # 3. Backup original
        backup = user_settings + ".bak"
        try:
            shutil.copy2(user_settings, backup)
            s[log_key] += "\nOriginal settings.dat backed up."
        except Exception as e:
            s[log_key] += f"\nWarning: Could not backup settings.dat: {e}"

        # 4. Copy patched file (cmd copy bypasses file locks)
        try:
            result = subprocess.run(
                ["cmd", "/c", "copy", "/Y", patched, user_settings],
                capture_output=True, text=True, timeout=10,
                creationflags=0x08000000
            )
            if result.returncode == 0:
                s[log_key] += "\nDeveloper Mode patched successfully."
                await self._update_ui()
                return True
            else:
                s[log_key] += f"\nCopy failed: {result.stderr.strip()}"
                return False
        except Exception as e:
            s[log_key] += f"\nPatch error: {e}"
            return False

    async def _automate_dev_mode(self, log_key): 
        """Automated logic ported from logic2.py with latest coordinates."""
        try:
            # Block user input during automation
            try: ctypes.windll.user32.BlockInput(True)
            except: pass
            
            import pyautogui
            try:
                from pywinauto import Desktop
            except ImportError:
                self.state[log_key] += "\n\u2139 Missing 'pywinauto' library for automation."
                return False

            self.state[log_key] += "\nOpening WSA Settings..."
            await self._update_ui()
            
            subprocess.Popen(
                r'explorer.exe shell:AppsFolder\MicrosoftCorporationII.WindowsSubsystemForAndroid_8wekyb3d8bbwe!SettingsApp'
            )
            await asyncio.sleep(4)

            desktop = Desktop(backend="uia")
            window = None
            for w in desktop.windows():
                if "Subsystem" in w.window_text():
                    window = w
                    break

            if not window:
                self.state[log_key] += "\n\u2717 WSA window not found."
                return False

            window.set_focus()
            await asyncio.sleep(1)
            if not window:
                self.state[log_key] += "\n\u2717 WSA Settings window not found."
                return False

            print(f"[DEBUG] Found and focusing WSA window: {window.window_text()}")
            window.set_focus()
            await asyncio.sleep(1.5)

            # Open Sidebar/Menu
            rect = window.rectangle()
            pyautogui.click(rect.left + 40, rect.top + 40)
            await asyncio.sleep(0.5)

            # Find Advanced Settings
            found_adv = False
            for c in window.descendants():
                try:
                    if "advanced" in c.window_text().lower():
                        c.click_input()
                        found_adv = True
                        break
                except:
                    pass
            
            if not found_adv:
                 # Fallback click based on relative pos if text search failed
                 pyautogui.click(rect.left + 100, rect.top + 300)

            await asyncio.sleep(1.5)

           
            # But first check if it's already "On"
            is_on = False
            for c in window.descendants():
                try:
                    text = c.window_text().lower()
                    if "developer mode" in text:
                        if "On" in text or "enabled" in text:
                            is_on = True
                        break
                except:
                    pass

            if is_on:
                self.state[log_key] += "\n\u2713 Developer Mode already ON. Skipping toggle click."
            else:
                adv_rect = window.rectangle()
                toggle_x = adv_rect.right - 70
                toggle_y = adv_rect.top + 145
                
                pyautogui.moveTo(toggle_x, toggle_y, duration=0.05)
                pyautogui.click()
                self.state[log_key] += "\n\u2713 Sent toggle command."
            
            await self._update_ui()
            
            # Try to click 'Allow' if a popup appears (Commented out per user request)
            # pyautogui.press('tab')
            # pyautogui.press('enter')
            
            # Minimize ONLY the WSA Settings window after automation
            # Using pywinauto's .minimize() to target the window specifically
            await asyncio.sleep(1)
            try:
                if window: window.minimize()
            except:
                pass
            
            return True
        except Exception as e:
            self.state[log_key] += f"\n\u2717 Automation error: {e}"
            return False
        finally:
            # Always restore user control
            try: ctypes.windll.user32.BlockInput(False)
            except: pass

    async def youtube_subscribe(self):
        """Automated YouTube subscription with status check and terminal logging."""
        print("\n" + "="*50)
        print("STEP 5: FINAL VERIFICATION & ENGAGEMENT")
        print("="*50)
        
        _yt_handle = getattr(CONFIG, "YT_CHANNEL_HANDLE", "@AT_Tech_Zone")
        _yt_title  = getattr(CONFIG, "YT_CHANNEL_TITLE", "AT Tech Zone")
        _yt_url    = getattr(CONFIG, "YT_CHANNEL_URL", "https://www.youtube.com/@AT_Tech_Zone")
        print(f"[INFO] Launching YouTube channel: {_yt_handle}")
        subprocess.Popen(["start", _yt_url], shell=True)
        
        print("[INFO] Waiting for browser to load (15s polling)...")
        browser_window = None
        target_channel = _yt_handle
        target_title_part = _yt_title
        
        for i in range(15):
            await asyncio.sleep(1)
            try:
                if Desktop:
                    for w in Desktop(backend="uia").windows():
                        title = w.window_text()
                        # Strictly target the specific channel window/tab
                        # Must contain "YouTube" and either the channel handle or title
                        if "YouTube" in title and (target_title_part in title or target_channel in title):
                            browser_window = w
                            print(f"[INFO] Targeting window: {title}")
                            w.set_focus()
                            await asyncio.sleep(0.5)
                            break
                if browser_window: break
            except:
                pass
        
        if not browser_window:
            print(f"[WARN] Could not find YouTube window for {target_channel}. Please subscribe manually.")
            return

        print(f"[INFO] Targeting window: {browser_window.window_text()}")
        print("[INFO] Verifying full page load (Waiting for channel name in UI)...")
        
        # content-verification loop
        is_fully_loaded = False
        for _ in range(15):
            try:
                # Search for the channel name in any descendant's text
                for child in browser_window.descendants():
                    if target_title_part in child.window_text():
                        is_fully_loaded = True
                        break
                if is_fully_loaded: break
            except:
                pass
            await asyncio.sleep(1)

        if not is_fully_loaded:
            print(f"[WARN] Page content for {target_channel} did not load in time. Proceeding with caution.")
        else:
            print(f"[SUCCESS] Page fully loaded: '{target_title_part}' detected in UI.")

        browser_window.set_focus()
        await asyncio.sleep(2)
        
        # Block input
        try: ctypes.windll.user32.BlockInput(True)
        except: pass
        
        try:
            print("[INFO] Verifying subscription status (Searching for 'Subscribed')...")
            # Try to check if "Subscribed" (with 'd') is already present
            pyautogui.hotkey('ctrl', 'f')
            await asyncio.sleep(0.6)
            pyautogui.write('Subscribed', interval=0.06)
            await asyncio.sleep(1)
            
            # Verify URL if possible (Address Bar)
            try:
                # Common browsers (Chrome/Edge/Brave) use an Edit control for Address Bar
                addr = browser_window.child_window(title_re=".*Address.*", control_type="Edit")
                if addr.exists(timeout=1):
                    url = addr.get_value()
                    if url and getattr(CONFIG, "YT_CHANNEL_HANDLE", "@AT_Tech_Zone") not in url:
                        print(f"[INFO] Current URL: {url} - Switching tab or reloading might be needed.")
            except:
                pass

            # Try searching for "Subscribed" multiple times with small delays
            is_already_subscribed = False
            _yt_subscribed = getattr(CONFIG, "YT_SUBSCRIBED_BTN_TEXT", "Subscribed")
            for _ in range(3):
                try:
                    # Look for anything containing "Subscribed" (exact or substring)
                    if browser_window.child_window(title=_yt_subscribed, control_type="Button").exists(timeout=0.2):
                        is_already_subscribed = True
                        break

                    # More aggressive: search descendants for text match in any button or text
                    for child in browser_window.descendants(control_type="Button"):
                        txt = child.window_text()
                        if _yt_subscribed in txt:
                            is_already_subscribed = True
                            break
                    if is_already_subscribed: break
                except:
                    pass
                await asyncio.sleep(1)

            if is_already_subscribed:
                print("[SUCCESS] Already Subscribed! No further action needed.")
                pyautogui.press('esc') # Close the find bar
            else:
                print(f"[INFO] '{_yt_subscribed}' not detected. Attempting to click 'Subscribe' button...")

                # 1. Try UIA direct click first (Most reliable for PWAs/Modern Browsers)
                clicked = False
                try:
                    btn = browser_window.child_window(title=getattr(CONFIG, "YT_SUBSCRIBE_BTN_TEXT", "Subscribe"), control_type="Button")
                    if btn.exists(timeout=1):
                        btn.click_input()
                        clicked = True
                        print("[SUCCESS] Clicked Subscribe via UI Automation.")
                except:
                    pass
                
                # 2. Fallback to CTRL+F method if UIA click failed
                if not clicked:
                    print("[INFO] UIA failed, falling back to Find (CTRL+F) method...")
                    pyautogui.hotkey('ctrl', 'f')
                    await asyncio.sleep(0.6)
                    pyautogui.write('Subscribe', interval=0.06)
                    pyautogui.press('enter')
                    await asyncio.sleep(1)
                    pyautogui.press('esc')
                    await asyncio.sleep(0.5)
                    pyautogui.press('enter')
                    print("[SUCCESS] Subscribe command sent via keyboard fallback.")
            
            await asyncio.sleep(2)
            print("[INFO] Verification complete.")
            
        except Exception as e:
            print(f"[ERROR] Verification failed: {e}")
        finally:
            # Restore input
            try: ctypes.windll.user32.BlockInput(False)
            except: pass
            
        print("[INFO] Exiting in 3 seconds...")
        await asyncio.sleep(3)
        print("="*50)
        print("SETUP COMPLETED SUCCESSFULLY")
        print("="*50)
        
        # Close the Flet UI window gracefully if page reference exists
        if self.page:
            try:
                await self.page.window.close()
            except:
                pass
        
        os._exit(0)
    
    async def uninstall_wsa_logic(self):
        """System-level cleanup for WSA uninstallation."""
        log_key = "uninstall_log" # Internal key for logging
        self.state[log_key] = "Starting WSA Uninstallation..."
        await self._update_ui()
        
        # 1. Kill all WSA processes
        await self._kill_wsa_completely(log_key)
        
        # 1.5 Find Package Install Location
        self.state[log_key] += "\nChecking for registered package location..."
        cmd_get_loc = ["powershell.exe", "-NoProfile", "-Command", "Get-AppxPackage *WindowsSubsystemForAndroid* | Select-Object -ExpandProperty InstallLocation"]
        install_location = ""
        try:
            proc_loc = await self._create_subprocess(
                *cmd_get_loc,
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                creationflags=0x08000000 if sys.platform == "win32" else 0
            )
            stdout, _ = await proc_loc.communicate()
            install_location = stdout.decode().strip()
            if install_location:
                self.state[log_key] += f"\n\u2139 Found package at: {install_location}"
        except Exception:
            pass

        # 2. Uninstall the Appx Package
        self.state[log_key] += "\nUninstalling WSA Appx Package..."
        cmd_uninstall = ["powershell.exe", "-NoProfile", "-Command", "Get-AppxPackage *WindowsSubsystemForAndroid* | Remove-AppxPackage"]
        uninstall_success = False
        try:
            proc = await self._create_subprocess(
                *cmd_uninstall,
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                creationflags=0x08000000 if sys.platform == "win32" else 0
            )
            stdout, stderr = await proc.communicate()
            if proc.returncode == 0:
                self.state[log_key] += "\n\u2713 WSA Appx package removed."
                uninstall_success = True
            else:
                err = stderr.decode(errors="ignore").strip()
                self.state[log_key] += f"\n\u26A0 Remove-AppxPackage exit code {proc.returncode}: {err[:200]}"
                # Retry with -AllUsers
                self.state[log_key] += "\n  Retrying with -AllUsers..."
                await self._update_ui()
                cmd_retry = ["powershell.exe", "-NoProfile", "-Command",
                             "Get-AppxPackage *WindowsSubsystemForAndroid* | Remove-AppxPackage -AllUsers"]
                proc2 = await self._create_subprocess(
                    *cmd_retry,
                    stdin=asyncio.subprocess.DEVNULL,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    creationflags=0x08000000 if sys.platform == "win32" else 0
                )
                stdout2, stderr2 = await proc2.communicate()
                if proc2.returncode == 0:
                    self.state[log_key] += "\n\u2713 WSA Appx package removed (with -AllUsers)."
                    uninstall_success = True
                else:
                    err2 = stderr2.decode(errors="ignore").strip()
                    self.state[log_key] += f"\n\u2717 Remove-AppxPackage -AllUsers also failed: {err2[:200]}"
            await self._update_ui()
        except Exception as e:
            self.state[log_key] += f"\n\u2717 Failed to remove Appx package: {e}"
            await self._update_ui()
        finally:
            if 'proc' in locals() and proc:
                self._force_kill_process_tree(proc.pid)

        # Verify uninstall
        if uninstall_success:
            self.state[log_key] += "\nVerifying uninstall..."
            await self._update_ui()
            verify_cmd = ["powershell.exe", "-NoProfile", "-Command",
                          "Get-AppxPackage *WindowsSubsystemForAndroid*"]
            try:
                vproc = await self._create_subprocess(
                    *verify_cmd,
                    stdin=asyncio.subprocess.DEVNULL,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    creationflags=0x08000000 if sys.platform == "win32" else 0
                )
                vout, _ = await vproc.communicate()
                if vout.decode(errors="ignore").strip():
                    self.state[log_key] += "\n\u26A0 Package still registered after remove attempt."
                    uninstall_success = False
                else:
                    self.state[log_key] += "\n\u2713 Confirmed: package no longer registered."
            except Exception:
                pass
            await self._update_ui()

        # 3. Delete the WSA shortcut and unified destination
        self.state[log_key] += f"\nDeleting WSA shortcut and installation directory..."
        await self._update_ui()
        try:
            def delete_files():
                # Delete shortcut
                if os.path.exists(CONFIG.WSA_ROOT):
                    try: os.remove(CONFIG.WSA_ROOT)
                    except: pass
                
                # Delete registered package directory if it exists
                if install_location and os.path.exists(install_location):
                    for attempt in range(3):
                        try:
                            shutil.rmtree(install_location, ignore_errors=True)
                            if not os.path.exists(install_location): break
                            time.sleep(1)
                        except:
                            time.sleep(1)

                # Delete destination directory
                if os.path.exists(self.WSA_DEST_DIR):
                    for attempt in range(3):
                        try:
                            shutil.rmtree(self.WSA_DEST_DIR, ignore_errors=True)
                            if not os.path.exists(self.WSA_DEST_DIR): break
                            time.sleep(1)
                        except:
                            time.sleep(1)
            
            await asyncio.to_thread(delete_files)
            if not os.path.exists(CONFIG.WSA_ROOT) and not os.path.exists(self.WSA_DEST_DIR):
                self.state[log_key] += "\n\u2713 WSA files and directories removed."
            else:
                self.state[log_key] += "\n\u26A0 Could not fully delete all WSA files. Some may be locked."
            await self._update_ui()
        except Exception as e:
            self.state[log_key] += f"\n\u2717 Error deleting files: {e}"
            await self._update_ui()

        return True


# Global socket for instance lock to prevent garbage collection
_instance_lock = None

def check_instance_lock():
    global _instance_lock
    try:
        _instance_lock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind to a unique port for this specific app
        _instance_lock.bind((CONFIG.APP_IP_LOCK, CONFIG.APP_PORT_LOCK))
        return True
    except socket.error:
        return False

# ─── ADS Toggle (Set to True to enable Monetag/PyWinAuto ads, False to skip) ────


class AdWebEngineWindow(QMainWindow):
    def __init__(self, url, display_seconds=15, close_event=None):
        super().__init__()
        self.url = url
        self.display_seconds = display_seconds
        self._close_event = close_event
        self.init_ui()
        self.setWindowTitle("Sponsor Ad")
        # Ensure it stays on top and has basic window controls
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool # Hide from taskbar
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(450, 350)
        self.browser.setUrl(QUrl(self.url))
        
        # Follow main window timer
        self.follow_timer = QTimer(self)
        self.follow_timer.timeout.connect(self.follow_main_app)
        self.follow_timer.start(10) # High frequency for smooth movement
        
        # Auto-close after specified seconds
        QTimer.singleShot(self.display_seconds * 1000, self.close)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.browser = QWebEngineView()
        self.browser.setFixedSize(450, 350)
        # Disable scrollbars and make it feel like a fixed ad unit
        self.browser.settings().setAttribute(self.browser.settings().WebAttribute.ShowScrollBars, False)
        layout.addWidget(self.browser)

    def follow_main_app(self):
        try:
            target_title = "WSA Installer — By MR CYBER"
            hwnd_parent = ctypes.windll.user32.FindWindowW(None, target_title)
            if hwnd_parent:
                # Get child HWND
                hwnd_child = int(self.winId())
                
                # Cross-process embedding (SetParent)
                # We do this once to "link" the windows
                if not hasattr(self, "_is_embedded"):
                    ctypes.windll.user32.SetParent(hwnd_child, hwnd_parent)
                    self._is_embedded = True
                
                import ctypes.wintypes
                rect = ctypes.wintypes.RECT()
                ctypes.windll.user32.GetClientRect(hwnd_parent, ctypes.byref(rect))
                
                # Relative positioning inside parent
                w = rect.right - rect.left
                h = rect.bottom - rect.top
                
                new_x = (w - 450) // 2
                new_y = (h - 350) // 2
                
                if self.pos().x() != new_x or self.pos().y() != new_y:
                    self.move(new_x, new_y)
        except:
            pass

    def closeEvent(self, event):
        if self._close_event:
            self._close_event.set()
        super().closeEvent(event)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    # Re-launch the program with admin rights
    if getattr(sys, 'frozen', False):
        path = sys.executable
        params = ' '.join(sys.argv[1:])
    else:
        path = sys.executable
        params = f'"{sys.argv[0]}" ' + ' '.join(sys.argv[1:])
    
    try:
        # returns > 32 on success
        ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", path, params, None, 1)
        if ret > 32:
            sys.exit(0)
        else:
            return False
    except Exception as e:
        print(f"Failed to elevate: {e}")
        return False


def _kill_existing_bg_service():
    """Kill all running bg-service processes before starting a new one."""
    try:
        own_pid = os.getpid()
        ps_cmd = (
            "Get-CimInstance Win32_Process | "
            "Where-Object { $_.CommandLine -match '--bg-service' -and $_.CommandLine -notmatch '--bg-service-gui' } | "
            "Select-Object -ExpandProperty ProcessId"
        )
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_cmd],
            capture_output=True, text=True, creationflags=0x08000000, timeout=10
        )
        for token in r.stdout.split():
            try:
                pid = int(token)
                if pid != own_pid:
                    subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                                  capture_output=True, creationflags=0x08000000, timeout=5)
                    print(f"[MAIN] Killed old bg-service process (PID: {pid})")
            except ValueError:
                pass
    except Exception:
        pass

def spawn_bg_service_if_needed():
    """Spawns the background service as a detached process if not already active."""
    if _acquire_bg_mutex():
        _release_bg_mutex()
        try:
            cmd = _script_args("--bg-service")
            subprocess.Popen(
                cmd,
                creationflags=0x08000000,
                close_fds=True
            )
            print("[MAIN] Spawned background service process successfully.")
        except Exception as e:
            print(f"[MAIN] Failed to spawn background service: {e}")


# ─── Palette & Constants ───────────────────────────────────────────────
def clean_asset_name(name):
    """Converts cryptic GitHub filenames into readable titles based on features."""
    try:
        name_l = name.lower()
        
        # Extract version if present (e.g. 2407.40000.4.0)
        ver = "Latest"
        if "_" in name:
            parts = name.split("_")
            if len(parts) > 1 and parts[1][0].isdigit():
                ver = parts[1]

        features = []
        
        # 1. Play Store & Amazon
        if ("gapps" in name_l or "mindthegapps" in name_l) and "nogapps" not in name_l:
            features.append("PlayStore")
        else:
            features.append("No PlayStore")
            
        if "noamazon" in name_l or "removedamazon" in name_l:
            features.append("No Amazon")
        else:
            features.append("With Amazon")

        # 2. Root Access
        if "magisk" in name_l:
            if "canary" in name_l:
                features.append("Magisk Canary")
            else:
                features.append("Magisk Stable")
        elif "kernelsu" in name_l:
            features.append("KernelSU")
        else:
            features.append("No Rooted")

        # 3. Architecture
        arch = "x64"
        if "arm64" in name_l:
            arch = "ARM64"
            
        return f"WSA ({', '.join(features)})"
    except:
        return name

# ─── Transparency Settings (1 is Solid, 100 is Fully Transparent) ────
# Matches the reference pattern used in D:\python pro\wsa_installer\app.py
GLASS_LEVEL = 75
ALPHA = getattr(CONFIG, "ALPHA", f"{int((1 - GLASS_LEVEL/100) * 255):02X}" if GLASS_LEVEL else "BF")

def _apply_glass_alpha(hex_color, alpha_hex):
    """Apply alpha_hex to hex_color. Matches the reference pattern used in
    D:\\python pro\\wsa_installer\\app.py.

    - 6-digit "#RRGGBB" -> prepend alpha -> "#AARRGGBB"
    - 9-digit "#AARRGGBB" -> replace alpha -> "#AARRGGBB"
    - Anything else (no leading "#", wrong length, named color) -> returned as-is.
    """
    if not hex_color or not isinstance(hex_color, str):
        return hex_color
    s = hex_color.strip()
    if s.startswith("#"):
        body = s[1:]
        if len(body) == 6:
            return f"#{alpha_hex}{body}"
        if len(body) == 8:
            return f"#{alpha_hex}{body[2:]}"
    return hex_color


# NOTE: Flet 0.84.0 on Windows only honours `page.window.bgcolor = TRANSPARENT`
# for OS-level window transparency (GitHub issue #5747). Passing a hex with an
# alpha channel (e.g. "#BF000000") is treated as a solid color, not as per-pixel
# alpha. Therefore the actual transparency effect is created by applying ALPHA
# to the inner BG_DARK / BG_CARD / BG_SIDEBAR color constants below; the window
# background itself stays fully transparent.


def _walk_and_repaint_glass(controls, alpha_hex):
    """Recursively walk a list of controls and rewrite the alpha channel of any
    7- or 9-digit ARGB hex bgcolor to the given alpha_hex. Used by the runtime
    glass slider to repaint backgrounds live without rebuilding the UI.
    Mirrors the reference pattern (D:\\python pro\\wsa_installer\\app.py)."""
    def _visit(c):
        if not c:
            return
        try:
            bg = getattr(c, "bgcolor", None)
            if isinstance(bg, str) and bg.startswith("#"):
                body = bg[1:]
                if len(body) == 8:
                    c.bgcolor = f"#{alpha_hex}{body[2:]}"
                elif len(body) == 6:
                    c.bgcolor = f"#{alpha_hex}{body}"
        except Exception:
            pass
        if hasattr(c, "controls") and c.controls:
            for child in c.controls:
                _visit(child)
        if hasattr(c, "content") and c.content:
            _visit(c.content)
    for c in controls:
        _visit(c)

BG_DARK = _apply_glass_alpha(CONFIG.COLOR_BG_DARK, ALPHA)
BG_CARD = _apply_glass_alpha(CONFIG.COLOR_BG_CARD, ALPHA)
BG_SIDEBAR = _apply_glass_alpha(CONFIG.COLOR_BG_SIDEBAR, ALPHA)
ACCENT = CONFIG.COLOR_ACCENT
ACCENT_HOVER = CONFIG.COLOR_ACCENT_HOVER
SUCCESS = CONFIG.COLOR_SUCCESS
WARNING = CONFIG.COLOR_WARNING
TEXT_PRIMARY = CONFIG.COLOR_TEXT_PRIMARY
TEXT_SECONDARY = CONFIG.COLOR_TEXT_SECONDARY   

BORDER = CONFIG.COLOR_BORDER
RED_DOT = CONFIG.COLOR_RED_DOT
YELLOW_DOT = CONFIG.COLOR_YELLOW_DOT
GREEN_DOT = CONFIG.COLOR_GREEN_DOT

def get_steps():
    return [
        {"id": 0, "label": CONFIG.STEP_INTRO_LABEL,   "icon": ft.Icons.INFO_OUTLINE},
        {"id": 1, "label": CONFIG.STEP_CHECK_LABEL,      "icon": ft.Icons.SEARCH_OUTLINED},
        {"id": 2, "label": CONFIG.STEP_INSTALL_LABEL,    "icon": ft.Icons.ANDROID_OUTLINED},
        {"id": 3, "label": CONFIG.STEP_PLAYSTORE_LABEL,  "icon": ft.Icons.STORE_OUTLINED},
        {"id": 4, "label": CONFIG.STEP_COMPLETE_LABEL,       "icon": ft.Icons.CHECK_CIRCLE_OUTLINE},
    ]


# ─── Automation Helpers ────────────────────────────────────────────────
def set_user_input(enabled: bool):
    """Enable or disable mouse and keyboard input."""
    try:
        ctypes.windll.user32.BlockInput(not enabled)
    except:
        pass


# ─── Helper builders ───────────────────────────────────────────────────
def dot(color: str) -> ft.Container:
    return ft.Container(
        width=12, height=12,
        border_radius=6,
        bgcolor=color,
    )


def traffic_lights(on_close=None, on_minimize=None, on_maximize=None) -> ft.Row:
    def _btn(color, tooltip, handler):
        c = ft.Container(
            width=12, height=12,
            border_radius=6,
            bgcolor=color,
            tooltip=tooltip,
            on_click=handler,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
        return c

    return ft.Row(
        controls=[
            _btn(RED_DOT,    "Close",    on_close),
            _btn(YELLOW_DOT, "Minimise", on_minimize),
            _btn(GREEN_DOT,  "Maximise", on_maximize),
        ],
        spacing=8,
    )


def sidebar_item(step: dict, current: int, on_click=None) -> ft.Container:
    is_done    = step["id"] < current
    is_active  = step["id"] == current
    text_color = TEXT_PRIMARY if is_active else (SUCCESS if is_done else TEXT_SECONDARY)
    bg         = "#0A84FF22" if is_active else ft.Colors.TRANSPARENT

    icon_color = SUCCESS if is_done else (ACCENT if is_active else TEXT_SECONDARY)
    icon_name  = ft.Icons.CHECK_CIRCLE if is_done else step["icon"]

    return ft.Container(
        key=f"step_{step['id']}",
        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
        border_radius=10,
        bgcolor=bg,
        animate=ft.Animation(400, ft.AnimationCurve.DECELERATE),
        offset=ft.Offset(0, 0),
        content=ft.Row(
            spacing=12,
            controls=[
                ft.Icon(
                    icon_name, 
                    color=icon_color, 
                    size=18,
                    animate_scale=ft.Animation(300, ft.AnimationCurve.BOUNCE_OUT),
                    scale=1.1 if is_active else 1.0,
                ),
                ft.Text(step["label"], color=text_color, size=13,
                        weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.NORMAL),
            ],
        ),
    )


def progress_bar(value: float) -> ft.Container:
    return ft.Container(
        height=5,
        border_radius=3,
        bgcolor="#3A3A3C",
        content=ft.Container(
            width=None,
            height=5,
            border_radius=3,
            bgcolor=ACCENT,
            animate=ft.Animation(600, ft.AnimationCurve.EASE_OUT),
        ),
    )


# ─── Step Content Pages ────────────────────────────────────────────────
def page_intro() -> ft.Column:
    return ft.Column(
        spacing=20,
        expand=True,
        controls=[
            ft.Container(height=10),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.ANDROID, color=ACCENT, size=64),
                        bgcolor="#0A84FF18",
                        border_radius=20,
                        padding=20,
                    )
                ],
            ),
            ft.Text(
                CONFIG.INTRO_TITLE,
                size=28, weight=ft.FontWeight.BOLD,
                color=TEXT_PRIMARY, text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                getattr(CONFIG, "INTRO_SUBTITLE", "This installer will set up Windows Subsystem for Android\u2122\nand configure Google Play Store on your Windows 11 PC."),
                size=14, color=TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=10),
            ft.Container(
                border=ft.Border.all(1, BORDER),
                border_radius=12,
                padding=16,
                bgcolor="#2C2C2E",
                content=ft.Column(
                    spacing=10,
                    controls=[
                        _req_row(ft.Icons.COMPUTER_OUTLINED,       CONFIG.REQ_TITLE_1),
                        _req_row(ft.Icons.MEMORY_OUTLINED,         CONFIG.REQ_TITLE_2),
                        _req_row(ft.Icons.STORAGE_OUTLINED,        CONFIG.REQ_TITLE_3),
                        _req_row(ft.Icons.WIFI_OUTLINED,           CONFIG.REQ_TITLE_4),
                        _req_row(ft.Icons.ADMIN_PANEL_SETTINGS_OUTLINED, CONFIG.REQ_TITLE_5),
                    ],
                ),
            ),
        ],
    )


def _req_row(icon, text) -> ft.Row:
    return ft.Row(
        spacing=12,
        controls=[
            ft.Icon(icon, color=ACCENT, size=16),
            ft.Text(text, color=TEXT_SECONDARY, size=13),
        ],
    )


# ─── Page Builders (accepting persistent controls) ─────────────────────
def page_check_wsa(ui) -> ft.Column:
    return ft.Column(
        spacing=20, expand=True,
        controls=[
            ft.Container(height=10),
            ft.Text(CONFIG.SCAN_TITLE, size=22, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
            ft.Text(
                getattr(CONFIG, "SCAN_DESC", "We'll scan your system to check if Windows Subsystem for\nAndroid is already installed."),
                size=13, color=TEXT_SECONDARY,
            ),
            ft.Container(
                border=ft.Border.all(1, BORDER),
                border_radius=14, padding=20, bgcolor=BG_CARD,
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ui["check_phase_header"],
                        ft.Divider(height=1, color="#3A3A3C33"),
                        ui["check_sub_rows"],
                    ],
                ),
            ),
            ft.Container(
                border=ft.Border.all(1, "#3A3A3C33"),
                border_radius=10, padding=10, bgcolor="#1C1C1E",
                content=ft.Column(
                    spacing=0,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(CONFIG.SCAN_LOG_HEADER, color=TEXT_SECONDARY, size=11, weight=ft.FontWeight.BOLD),
                                ft.IconButton(
                                    icon=ft.Icons.COPY_ROUNDED,
                                    icon_size=14,
                                    icon_color=TEXT_SECONDARY,
                                    tooltip="Copy Log",
                                on_click=lambda e: (pyperclip.copy(ui["check_log"].value), e.page.update())
                                ),
                            ]
                        ),
                        ft.Container(
                            height=120,
                            content=ft.Column(
                                controls=[ui["check_log"]],
                                scroll=ft.ScrollMode.ADAPTIVE,
                                spacing=0,
                            )
                        ),
                    ],
                ),
            ),
        ],
    )


def page_install_wsa(ui) -> ft.Column:
    return ft.Column(
        spacing=20, expand=True,
        controls=[
            ft.Container(height=10),
            ft.Text(CONFIG.INSTALL_TITLE, size=22, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
            ft.Text(
                CONFIG.INSTALL_DESC,
                size=13, color=TEXT_SECONDARY,
            ),
            ft.Container(
                border=ft.Border.all(1, BORDER),
                border_radius=14, padding=20, bgcolor=BG_CARD,
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ui["install_phase_header"],
                        ft.Divider(height=1, color="#3A3A3C33"),
                        ui["install_sub_rows"],
                    ],
                ),
            ),
            ft.Container(
                border=ft.Border.all(1, "#3A3A3C33"),
                border_radius=10, padding=10, bgcolor="#1C1C1E",
                content=ft.Column(
                    spacing=0,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Install Log", color=TEXT_SECONDARY, size=11, weight=ft.FontWeight.BOLD),
                                ft.IconButton(
                                    icon=ft.Icons.COPY_ROUNDED, 
                                    icon_size=14, 
                                    icon_color=TEXT_SECONDARY,
                                    tooltip="Copy Log",
                                on_click=lambda e: (pyperclip.copy(ui["install_log"].value), e.page.update())
                                ),
                            ]
                        ),
                        ft.Container(
                            height=120,
                            content=ft.Column(
                                controls=[ui["install_log"]],
                                scroll=ft.ScrollMode.ADAPTIVE,
                                spacing=0,
                            )
                        ),
                    ],
                ),
            ),
        ],
    )


def page_playstore(ui) -> ft.Column:
    return ft.Column(
        spacing=20, expand=True,
        controls=[
            ft.Container(height=10),
            ft.Text(CONFIG.PS_TITLE, size=22, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
            ft.Text(
                CONFIG.PS_DESC,
                size=13, color=TEXT_SECONDARY,
            ),
            ft.Container(
                border=ft.Border.all(1, BORDER),
                border_radius=14, padding=20, bgcolor=BG_CARD,
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ui["ps_phase_header"],
                        ft.Divider(height=1, color="#3A3A3C33"),
                        ui["ps_sub_rows"],
                    ],
                ),
            ),
            ft.Container(
                border=ft.Border.all(1, "#3A3A3C33"),
                border_radius=10, padding=10, bgcolor="#1C1C1E",
                content=ft.Column(
                    spacing=0,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Patch Log", color=TEXT_SECONDARY, size=11, weight=ft.FontWeight.BOLD),
                                ft.IconButton(
                                    icon=ft.Icons.COPY_ROUNDED, 
                                    icon_size=14, 
                                    icon_color=TEXT_SECONDARY,
                                    tooltip="Copy Log",
                                on_click=lambda e: (pyperclip.copy(ui["ps_log"].value), e.page.update())
                                ),
                            ]
                        ),
                        ft.Container(
                            height=120,
                            content=ft.Column(
                                controls=[ui["ps_log"]],
                                scroll=ft.ScrollMode.ADAPTIVE,
                                spacing=0,
                            )
                        ),
                    ],
                ),
            ),
        ],
    )



def page_complete(ui) -> ft.Column:

    def _on_about_md_tap(e):
        webbrowser.open(e.data)

    _about_md = getattr(CONFIG, "ABOUT_MD", ABOUT_MD)

    return ft.Column(
        spacing=14,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                expand=True,
                border=ft.Border.all(1, BORDER),
                border_radius=12,
                padding=20,
                bgcolor=BG_CARD,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                content=ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=12,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.INFO_ROUNDED, color=ACCENT, size=16),
                                ft.Text("About", size=16, weight=ft.FontWeight.BOLD,
                                        color=TEXT_PRIMARY),
                            ],
                        ),
                        ft.Markdown(
                            _about_md,
                            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                            on_tap_link=_on_about_md_tap,
                            selectable=True,
                        ),
                    ],
                ),
            ),
            ft.Container(height=5),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=SUCCESS, size=24),
                    ft.Text(
                        CONFIG.COMPLETE_TITLE,
                        size=16, weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                    ),
                ],
            ),
            ft.Text(
                getattr(CONFIG, "COMPLETE_DESC", "WSA with Google Play Store has been successfully installed."),
                size=12, color=TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=7),
        ],
    )


# ─── Main App ──────────────────────────────────────────────────────────


def page_about(ui) -> ft.Column:
    def _on_about_md_tap(e):
        webbrowser.open(e.data)

    _about_md = getattr(CONFIG, "ABOUT_MD", ABOUT_MD)

    return ft.Column(
        spacing=14,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                expand=True,
                border=ft.Border.all(1, BORDER),
                border_radius=12,
                padding=20,
                bgcolor=BG_CARD,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                content=ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=12,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.INFO_ROUNDED, color=ACCENT, size=16),
                                ft.Text("About", size=16, weight=ft.FontWeight.BOLD,
                                        color=TEXT_PRIMARY),
                            ],
                        ),
                        ft.Markdown(
                            _about_md,
                            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                            on_tap_link=_on_about_md_tap,
                            selectable=True,
                        ),
                    ],
                ),
            ),
            ft.Container(height=7),
        ],
    )


def _get_available_letters(mode="user"):
    """Return list of drive letters available for WebDAV mounting.
    - Local physical drives → hidden
    - `net use` entries matching our prev_letter → shown (ours)
    - `net use` entries pointing to 127.0.0.1:8088 but NOT ours → hidden (other tool)
    - `net use` entries pointing elsewhere → hidden (manual mapping)
    - The prev_letter is always included so user can reuse the same letter.
    """
    import string
    adv = _read_adv_state()
    prev_key = f"share_{mode}_prev_letter"
    our_letter = adv.get(prev_key, "X" if mode == "user" else "R").upper().strip(":")
    used = set()
    import re
    try:
        r = subprocess.run(["net", "use"], capture_output=True, text=True, creationflags=0x08000000, timeout=5)
        for line in r.stdout.splitlines():
            m = re.search(r"\b([A-Za-z]):\s+(\\\\\S+)", line)
            if m:
                l = m.group(1).upper()
                url = m.group(2)
                if "127.0.0.1:8088" in url:
                    if l == our_letter:
                        continue
                    used.add(l)
                else:
                    used.add(l)
    except: pass
    for l in string.ascii_uppercase:
        try:
            if os.path.exists(f"{l}:\\"):
                used.add(l)
        except: pass
    avail = [f"{l}:" for l in string.ascii_uppercase if l not in used]
    if f"{our_letter}:" not in avail:
        avail.append(f"{our_letter}:")
    avail.sort()
    return avail if avail else ["X:", "Y:", "Z:", "R:", "S:", "T:"]

# ── Advanced Page UI ──────────────────────────────────────────────────────

def page_advanced(page, ui, logic=None) -> ft.Column:
    adv = _read_adv_state()
    mode_data = {
        "user": {
            "icon": ft.Icons.FOLDER_SHARED,
            "title": "File Sharing with Windows",
            "desc": "Access WSA user files from Windows Explorer via WebDAV drive.",
            "color": ACCENT,
        },
        "root": {
            "icon": ft.Icons.ADMIN_PANEL_SETTINGS,
            "title": "Super User File Sharing",
            "desc": "Access WSA root filesystem from Windows Explorer (requires Magisk root).",
            "color": WARNING,
        },
    }

    card_ctrl = {"user": {}, "root": {}}

    def _set_controls_enabled(mode, enabled):
        cc = card_ctrl[mode]
        for key in ("letter_dd", "label_field"):
            if key in cc:
                setattr(cc[key], "disabled", not enabled)
        if "sw" in cc:
            cc["sw"].disabled = not enabled
        page.update()

    def _card(mode):
        d = mode_data[mode]
        cc = card_ctrl[mode]
        saved_letter = adv.get(f"share_{mode}_letter", "X" if mode == "user" else "R")
        saved_label  = adv.get(f"share_{mode}_label",
                                "Windows Subsystem For Android" if mode == "user" else "WSA RootFile System")
        initial_val = f"{saved_letter}:"
        cc["letter_dd"] = ft.Dropdown(
            options=[ft.dropdown.Option("Scanning...")],
            value="Scanning...", width=80, text_size=12,
        )
        cc["label_field"] = ft.TextField(value=saved_label, width=180, text_size=12,
                                          hint_text="Drive name", max_length=32)
        sw = ft.Switch(value=adv.get(f"share_{mode}") == "1")
        cc["sw"] = sw
        st = ft.Text("", size=11, expand=True, no_wrap=False)
        loading = ft.ProgressRing(width=14, height=14, visible=True)

        def _update_st():
            lv = cc["letter_dd"].value or initial_val
            if _is_drive_mounted(lv):
                st.value = f"+ Mounted as {lv} \u2014 {cc['label_field'].value}"
                st.color = SUCCESS
            else:
                st.value = "Not mounted"
                st.color = TEXT_SECONDARY
        cc["_update_st"] = _update_st

        async def _init_card():
            avail = await asyncio.to_thread(_get_available_letters, mode)
            _i_val = initial_val
            if _i_val not in avail:
                _i_val = "X:" if mode == "user" else "R:"
            cc["letter_dd"].options = [ft.dropdown.Option(o) for o in avail]
            cc["letter_dd"].value = _i_val
            _update_st()
            loading.visible = False
            page.update()

        page.run_task(_init_card)

        _share_dialog_running = False

        def _on_toggle(e):
            nonlocal _share_dialog_running
            if _share_dialog_running:
                return
            if sw.value:
                _share_dialog_running = True
                async def _run_fs():
                    nonlocal _share_dialog_running
                    try:
                        _write_adv_state(f"share_{mode}", "1")
                        _write_adv_state(f"share_{mode}_letter", (cc["letter_dd"].value or initial_val).strip(":"))
                        _write_adv_state(f"share_{mode}_prev_letter", (cc["letter_dd"].value or initial_val).strip(":"))
                        _write_adv_state(f"share_{mode}_label", cc["label_field"].value or (
                            "Windows Subsystem For Android" if mode == "user" else "WSA RootFile System"))
                        _cmd = _script_args("--file-sharing", mode)
                        await asyncio.to_thread(subprocess.run, _cmd,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            timeout=120, creationflags=subprocess.CREATE_NO_WINDOW)
                    except Exception as ex:
                        _append_log(f"Error: {ex}")
                    finally:
                        _share_dialog_running = False
                        try:
                            lv = cc["letter_dd"].value or initial_val
                            if _is_drive_mounted(lv):
                                sw.value = True
                                _write_adv_state(f"share_{mode}", "1")
                            else:
                                sw.value = False
                                _write_adv_state(f"share_{mode}", "0")
                            _update_st()
                            page.update()
                        except Exception:
                            pass
                page.run_task(_run_fs)
            else:
                lv = cc["letter_dd"].value or initial_val
                _unmount_drive(lv)
                _write_adv_state(f"share_{mode}", "0")
                _update_st()
                page.update()

        sw.on_change = _on_toggle

        return ft.Container(
            expand=True, border=ft.Border.all(1, BORDER),
            border_radius=14, padding=ft.Padding(14, 12, 14, 12), bgcolor=BG_CARD,
            content=ft.Column(spacing=6, controls=[
                ft.Row(spacing=8, controls=[
                    ft.Icon(d["icon"], color=d["color"], size=18),
                    ft.Text(d["title"], size=13, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY, expand=True),
                ]),
                ft.Text(d["desc"], size=11, color=TEXT_SECONDARY),
                ft.Row(spacing=6, controls=[
                    ft.Text("Drive:", size=11, color=TEXT_SECONDARY),
                    cc["letter_dd"],
                    ft.Text("Label:", size=11, color=TEXT_SECONDARY),
                    cc["label_field"],
                ]),
                ft.Row(spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                       controls=[sw, loading, st]),
            ]),
        )

    def _repair_card():
        adv = _read_adv_state()
        auto_repair_sw = ft.Switch(
            value=adv.get("auto_repair", "0") == "1",
            on_change=lambda e: _write_adv_state("auto_repair", "1" if e.control.value else "0"),
        )
        auto_repair_status = ft.Text(
            "WSA installed" if os.path.isdir(_wsa_data_path()) else "WSA not found",
            size=11, color=SUCCESS if os.path.isdir(_wsa_data_path()) else TEXT_SECONDARY,
        )

        def _on_repair(e):
            subprocess.Popen(_script_args("--repair-wsa"), creationflags=0x08000000)

        repair_btn = ft.FilledButton(
            "Repair WSA", icon=ft.Icons.REFRESH_ROUNDED,
            on_click=_on_repair,
            bgcolor="#E8A317", color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=ft.Padding.symmetric(horizontal=20, vertical=12)),
        )

        return ft.Container(
            expand=True, border=ft.Border.all(1, BORDER),
            border_radius=14, padding=ft.Padding(14, 12, 14, 12), bgcolor=BG_CARD,
            content=ft.Column(spacing=6, controls=[
                ft.Row(spacing=8, controls=[
                    ft.Icon(ft.Icons.REFRESH_ROUNDED, color="#E8A317", size=18),
                    ft.Text("WSA Repair", size=13, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY, expand=True),
                ]),
                ft.Text("If WSA is not working, click Repair to backup data, reinstall, and restore.",
                        size=11, color=TEXT_SECONDARY),
                ft.Container(height=2),
                ft.Row([repair_btn], alignment=ft.MainAxisAlignment.START),
                ft.Divider(height=6, color="#3A3A3C"),
                ft.Row(spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                    ft.Text("Auto-repair:", size=11, color=TEXT_SECONDARY),
                    auto_repair_sw,
                    auto_repair_status,
                ]),
                ft.Text("When enabled: if WSA fails to start 100 times, auto-triggers repair.",
                        size=10, color="#636366"),
            ]),
        )

    return ft.Column(spacing=10, expand=True, scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("File Sharing", size=15, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
            _card("user"),
            _card("root"),
            ft.Divider(height=6, color="#3A3A3C"),
            ft.Text("Maintenance", size=15, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
            _repair_card(),
        ],
    )





async def main(page: ft.Page):
    global _main_event_loop
    _main_event_loop = asyncio.get_event_loop()

    _rebuild_fn = None

    async def _safe_rebuild():
        if _rebuild_fn is None:
            return
        try:
            await _rebuild_fn()
        except Exception as e:
            SDKLogger.error(f"Page rebuild error: {e}")
            import traceback
            for line in traceback.format_exc().splitlines():
                SDKLogger.error(line)

    def _trigger_rebuild():
        try:
            asyncio.create_task(_safe_rebuild())
        except Exception as e:
            SDKLogger.error(f"Failed to schedule rebuild: {e}")

    add_rebuild_callback(_trigger_rebuild)

    _refresh_ui_ready = False

    async def refresh_ui():
        if not _refresh_ui_ready:
            return
        SDKLogger.info("[RUNTIME CONFIG] Applying runtime update")
        page.title = CONFIG.APP_TITLE
        title_text.value = CONFIG.APP_TITLE
        page.window.bgcolor = ft.Colors.TRANSPARENT
        page.fonts = {CONFIG.FONT_NAME_PRIMARY: CONFIG.FONT_URL_PRIMARY, "Consolas": "Consolas"}
        await rebuild_sidebar()
        await rebuild_content()
        apply_runtime_config(page)
        btn_next.style = ft.ButtonStyle(
            bgcolor={ft.ControlState.DEFAULT: ACCENT, ft.ControlState.HOVERED: ACCENT_HOVER},
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.Padding.symmetric(horizontal=20, vertical=12),
            elevation=0,
        )
        btn_back.style = ft.ButtonStyle(
            bgcolor=ft.Colors.TRANSPARENT,
            color=TEXT_SECONDARY,
            shape=ft.RoundedRectangleBorder(radius=8),
            side=ft.BorderSide(1, BORDER),
            padding=ft.Padding.symmetric(horizontal=20, vertical=12),
            elevation=0,
        )
        page.update()
        SDKLogger.info("[FLET UI] Runtime refresh complete")

    # Initialize dynamic configuration gateway with the UI page context
    start_remote_config(page, refresh_ui)

    ActivityLogger.init().event("SESSION_START")
    ActivityLogger.step_enter(0)

    page.title = CONFIG.APP_TITLE
    page.window.icon = resource_path("assets/icon.png") # Set runtime icon
    page.bgcolor        = ft.Colors.TRANSPARENT
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.window.width   = CONFIG.WINDOW_WIDTH
    page.window.height  = CONFIG.WINDOW_HEIGHT
    page.window.min_width  = CONFIG.WINDOW_MIN_WIDTH
    page.window.min_height = CONFIG.WINDOW_MIN_HEIGHT
    # sequence matters for some window managers
    page.window.title_bar_hidden = True
    page.window.frameless = True
    page.window.resizable = True
    page.window.visible = False # Start hidden to avoid "raw" flash
    
    # AppUserModelID is already set globally
    
    # AppUserModelID is already set globally
        
    icon_path = resource_path(os.path.join("assets", "icon.png"))
    if os.path.exists(icon_path):
        page.window.icon = icon_path
        
    page.padding        = 0
    page.fonts          = {
        CONFIG.FONT_NAME_PRIMARY: CONFIG.FONT_URL_PRIMARY,
        "Consolas": "Consolas"
    }
    page.theme = ft.Theme(font_family="Inter")

    # ── State ──────────────────────────────────────────────────────────
    state = {
        "current_step": 0,
        "overlay_mode": None,  # None | "about" | "advanced"
        # Check step
        "checking": False, "wsa_found": False, "wsa_running": False,
        "log": CONFIG.SCAN_AWAITING_TEXT,
        "scan_complete": False,
        "vhd_enabled": None,
        "check_phase": 0,
        "check_phase_title": "",
        "check_sub_status": [],
        # Install step
        "installing": False, "install_progress": 0.0,
        "install_done": False, "install_log": "Awaiting install\u2026",
        "install_phase": 0, "install_phase_title": "", "install_sub_status": [],
        # PlayStore step
        "ps_installing": False, "ps_progress": 0.0,
        "ps_done": False, "ps_log": "Awaiting patch\u2026",
        "ps_phase": 0, "ps_phase_title": "", "ps_sub_status": [],
        # Download Overlay State
        "show_download": None, # "nogapps" or "gapps" or None
        "download_options": [],
        "downloading": False,
        "download_progress": 0.0,
        "download_speed": "",
        "download_eta": "",
        "show_force_extract": None,
        "show_bundle_download": False,
        "bundle_check_result": None,
        "bundle_auto_close_task": None,
        "bundle_progress": 0.0,
        "bundle_speed": "",
        "bundle_eta": "",
        "show_restart_dialog": False,
    }

    # ── Logic class wiring (Initialization placeholder) ────────────────
    logic = None
    restart_action_event = asyncio.Event()

    async def _close(e):
        if logic:
            await logic.youtube_subscribe()
        else:
            ActivityLogger.session_end()
            sys.exit(0)

    # ── Layout containers ──────────────────────────────────────────────
    sidebar_col  = ft.Column(spacing=4, expand=True)
    content_area = ft.Container(
        expand=True,
        padding=ft.Padding.only(right=24, top=24, bottom=24),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )
    btn_back     = ft.FilledButton(getattr(CONFIG, "BUTTON_BACK_TEXT", "â† Back"))
    btn_next     = ft.FilledButton(getattr(CONFIG, "BUTTON_CONTINUE_TEXT", "Continue â†’"))

    # ── Persistent UI Controls ────────────────────────────────────────
    ui = {
        # Check Step
        "check_phase_header": ft.Text("", size=14, color=ACCENT, weight=ft.FontWeight.W_600),
        "check_sub_rows": ft.Column(spacing=10, controls=[]),
        "check_log":    ft.Text(CONFIG.SCAN_AWAITING_TEXT, color="#8E8E93", size=12, font_family="Consolas", selectable=True),

        # Install Step
        "install_phase_header": ft.Text("", size=14, color=ACCENT, weight=ft.FontWeight.W_600),
        "install_sub_rows": ft.Column(spacing=10, controls=[]),
        "install_log":    ft.Text("Awaiting install\u2026", color="#8E8E93", size=12, font_family="Consolas", selectable=True),

        # Play Store Step
        "ps_phase_header": ft.Text("Phase 1/7: Check Prerequisites", color=TEXT_PRIMARY, size=14, weight=ft.FontWeight.W_600),
        "ps_pct":    ft.Text("Pending", color=TEXT_SECONDARY, size=13),
        "ps_pb":     ft.ProgressBar(value=0, color="#30D158", bgcolor="#3A3A3C", height=6, border_radius=3),
        "ps_status": ft.Text("Waiting to start\u2026", color=TEXT_SECONDARY, size=12),
        "ps_sub_rows": ft.Column(spacing=10, controls=[]),
        "ps_log":    ft.Text("Awaiting patch\u2026", color="#8E8E93", size=12, font_family="Consolas", selectable=True),
    }

    # ── Ad Overlay & Timer ──────────────────────────────────────────────
    ad_timer_text = ft.Text("Ad finishes in 15s...", color=TEXT_PRIMARY, size=14, weight=ft.FontWeight.BOLD)
    ad_pb = ft.ProgressBar(width=300, color=ACCENT, bgcolor="#3A3A3C", value=0)
    ad_overlay = ft.Container(
        expand=True,
        bgcolor="#000000DD",
        visible=False,
        on_click=lambda _: None,
        alignment=ft.alignment.Alignment(0, 0),
        content=ft.Container(
            width=450, height=350,
            bgcolor=BG_DARK,
            border_radius=15,
            border=ft.Border.all(1, BORDER),
            padding=20,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Icon(ft.Icons.AD_UNITS_ROUNDED, color=ACCENT, size=48),
                    ft.Text("Monetization Ad Started", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "An ad has opened in your browser to support this tool.\nPlease wait for the timer to unlock the 'Continue' button.",
                        text_align=ft.TextAlign.CENTER, color=TEXT_SECONDARY, size=13
                    ),
                    ft.Container(height=10),
                    ad_timer_text,
                    ad_pb,
                ]
            )
        ),
    )

    # ── Download Selection Overlay ──────────────────────────────────────
    download_options_list = ft.RadioGroup(content=ft.Column(spacing=10))
    download_pb = ft.ProgressBar(width=400, color=ACCENT, bgcolor="#3A3A3C", value=0, visible=False)
    download_status_text = ft.Text("Select a package to continue", color=TEXT_SECONDARY, size=13)
    btn_download_confirm = ft.FilledButton("Download & Install", disabled=True)
    download_speed_text = ft.Text("", color=ACCENT, size=11, weight=ft.FontWeight.BOLD)
    download_eta_text = ft.Text("", color=TEXT_SECONDARY, size=11)

    async def on_download_click(e):
        ActivityLogger.button_click("btn_download_confirm", detail=state.get("show_download"))
        state["downloading"] = True
        download_pb.visible = True
        btn_download_confirm.disabled = True
        download_options_list.disabled = True
        page.update()
        
        selected_idx = int(download_options_list.value)
        asset = state["download_options"][selected_idx]
        
        if state["show_download"] == "nogapps":
            await logic.download_and_install_wsa(asset)
        else:
            await logic.download_and_add_playstore(asset)
            
        state["downloading"] = False
        state["show_download"] = None
        # Reset for next time
        download_pb.visible = False
        download_options_list.disabled = False
        btn_download_confirm.disabled = True
        page.update()

    async def on_download_cancel(e):
        ActivityLogger.button_click("btn_download_cancel")
        await logic.cancel()
        state["show_download"] = None
        await sync_ui()
        page.update()

    async def on_radio_change(e):
        if not download_options_list.value:
            return

        ActivityLogger.event("SELECT", "radio_option", detail=f"idx={download_options_list.value}")

        selected_idx = int(download_options_list.value)
        
        block_list = getattr(CONFIG, "config", {}).get("block_list_package", {})
        if state["show_download"] == "nogapps":
            blocked_indices = block_list.get("base_package", [0])
        else:
            blocked_indices = block_list.get("playstore_package", [0])
            
        if (selected_idx + 1) in blocked_indices:
            download_options_list.value = None
            btn_download_confirm.disabled = True
            download_status_text.value = "Package is corrupted on server. Please select another."
            if page:
                page.snack_bar = ft.SnackBar(ft.Text("This package is corrupted on the server. Please select a different package.", color=ft.Colors.WHITE), bgcolor=ft.Colors.RED_700)
                page.snack_bar.open = True
            page.update()
            return
            
        asset = state["download_options"][selected_idx]
        f_name = asset['name']
        
        # Use pathlib for robust cross-platform path handling
        cache_file = logic.CACHE_DIR / f_name
        
        # Check partial via presence of any chunked .part file
        has_partial = False
        try:
            prefix = f_name + ".part"
            if logic.CACHE_DIR.exists():
                for item in logic.CACHE_DIR.iterdir():
                    if item.name.startswith(prefix):
                        has_partial = True
                        break
        except Exception:
            pass
        
        if cache_file.exists():
            download_status_text.value = f"Ready: Found cached package ({f_name})"
            btn_download_confirm.text = getattr(CONFIG, "DL_BTN_CACHED", "Use Cached Package")
        elif has_partial:
            download_status_text.value = f"Partial download detected: {f_name}"
            btn_download_confirm.text = getattr(CONFIG, "DL_BTN_RESUME", "Resume Download")
        else:
            download_status_text.value = getattr(CONFIG, "DL_STATUS_PROMPT", "Select a package to continue")
            btn_download_confirm.text = getattr(CONFIG, "DL_BTN_NORMAL", "Download & Install")
        
        btn_download_confirm.disabled = False
        page.update()

    download_options_list.on_change = on_radio_change
    btn_download_confirm.on_click = on_download_click

    download_overlay = ft.Container(
        expand=True,
        bgcolor="#000000DD",
        visible=False,
        on_click=lambda _: None,
        alignment=ft.alignment.Alignment(0, 0),
        content=ft.Container(
            width=500, height=480, # Reduced height for better fit
            bgcolor=BG_DARK,
            border_radius=15,
            border=ft.Border.all(1, BORDER),
            padding=ft.Padding(24, 16, 24, 16), # Tightened padding
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START, # Use START to push everything up
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=14, # Reduced spacing
                controls=[
                    ft.Icon(ft.Icons.CLOUD_DOWNLOAD_ROUNDED, color=ACCENT, size=48),
                    ft.Text(getattr(CONFIG, "DL_OVERLAY_TITLE", "Download Required Assets"), size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        getattr(CONFIG, "DL_OVERLAY_DESC", "Assets are not bundled to keep the installer small. Please select a version to download from GitHub."),
                        text_align=ft.TextAlign.CENTER, color=TEXT_SECONDARY, size=13
                    ),
                    ft.Container(
                        height=160, # Reduced height from 200
                        padding=8,
                        border=ft.Border.all(1, "#3A3A3C"),
                        border_radius=10,
                        content=ft.Column([download_options_list], scroll=ft.ScrollMode.ADAPTIVE)
                    ),
                    download_status_text,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[download_speed_text, download_eta_text],
                        width=400
                    ),
                    download_pb,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12,
                        controls=[
                            ft.TextButton(getattr(CONFIG, "DL_BTN_CANCEL", "Cancel"), on_click=on_download_cancel),
                            btn_download_confirm
                        ]
                    )
                ]
            )
        )
    )

    # ── Admin Overlay ──────────────────────────────────────────────────
    admin_title = ft.Text(getattr(CONFIG, "ADMIN_TITLE", "Administrator Privileges Required"), size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)
    admin_msg   = ft.Text(
        getattr(CONFIG, "ADMIN_DESC", "This installer requires administrator privileges to modify system files and integrate WSA.\n\nPlease click 'Run as Admin' to relaunch with elevated permissions."),
        text_align=ft.TextAlign.CENTER, color=TEXT_SECONDARY, size=13
    )

    async def on_run_admin(e):
        ActivityLogger.button_click("btn_run_admin")
        run_as_admin()

    async def on_cancel_admin(e):
        ActivityLogger.button_click("btn_cancel_admin")
        await logic.cancel()
        admin_overlay.visible = False
        page.update()
        await _close(e)

    admin_overlay = ft.Container(
        expand=True,
        bgcolor="#000000EE",
        visible=False,
        on_click=lambda _: None,  # MODAL: Block clicks to background
        alignment=ft.alignment.Alignment(0, 0),
        content=ft.Container(
            width=450, height=300,
            bgcolor=BG_DARK,
            border_radius=15,
            border=ft.Border.all(1, BORDER),
            padding=24,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED, color=ACCENT, size=48),
                    admin_title,
                    admin_msg,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12,
                        controls=[
                            ft.TextButton(getattr(CONFIG, "ADMIN_BTN_CANCEL", "Cancel"), on_click=on_cancel_admin, scale=1.1),
                            ft.FilledButton(
                                getattr(CONFIG, "ADMIN_BTN_RUN", "Run as Admin"),
                                on_click=on_run_admin,
                                bgcolor=ACCENT,
                                color=ft.Colors.WHITE,
                                height=45,
                                width=160
                            ),
                        ]
                    )
                ]
            )
        ),
    )

    # ── Bundle Download Overlay ───────────────────────────────────────
    bundle_msg = ft.Text(
        getattr(CONFIG, "config", {}).get("BUNDLE_MSG", getattr(CONFIG, "BUNDLE_MSG",
            "WSA Basic and Play Store both packages into a single bundle.")),
        text_align=ft.TextAlign.CENTER, color=TEXT_SECONDARY, size=13
    )
    bundle_pb = ft.ProgressBar(value=0, color=ACCENT, bgcolor="#3A3A3C", height=6, border_radius=3, visible=False)
    bundle_speed_text = ft.Text("", color=TEXT_SECONDARY, size=11)
    bundle_eta_text = ft.Text("", color=TEXT_SECONDARY, size=11)
    bundle_status_text = ft.Text("", color=TEXT_SECONDARY, size=13)
    bundle_auto_close_text = ft.Text("", color=ACCENT, size=12, weight=ft.FontWeight.W_500)
    bundle_file_info = ft.Text("", color=TEXT_PRIMARY, size=13, weight=ft.FontWeight.W_600)
    
    def _get_bundle_dest_path():
        bundle_path_str = getattr(CONFIG, "config", {}).get("BUNDLE_PATH", getattr(CONFIG, "BUNDLE_PATH", ""))
        bundle_name = getattr(CONFIG, "config", {}).get("BUNDLE_NAME", getattr(CONFIG, "BUNDLE_NAME", ""))
        if not bundle_name:
            bundle_name = "bundle.zip"
        import pathlib
        try:
            if not bundle_path_str:
                raise ValueError("Empty path")
            p = pathlib.Path(bundle_path_str)
            if not p.parent.exists() and not p.parent.is_dir():
                raise ValueError("Invalid path")
            if p.is_dir():
                return p / bundle_name
            else:
                return p.with_name(bundle_name)
        except Exception:
            return logic.OUT_ASSET_DIR / bundle_name

    async def cancel_bundle_download(e):
        ActivityLogger.button_click("btn_cancel_bundle_download")
        await logic.cancel()
        logic.bundle_cancel_event.set()
        # Cancel auto-close timer if running
        if state.get("bundle_auto_close_task") and not state["bundle_auto_close_task"].done():
            state["bundle_auto_close_task"].cancel()
        state["bundle_auto_close_task"] = None
        bundle_auto_close_text.value = ""
        state["show_bundle_download"] = False
        btn_start_bundle_download.disabled = False
        bundle_pb.visible = False
        btn_cancel_bundle.text = "Cancel"
        btn_cancel_bundle.visible = True
        await sync_ui()
        page.update()

    btn_cancel_bundle = ft.TextButton("Cancel", on_click=cancel_bundle_download)

    async def on_start_bundle_download(e):
        ActivityLogger.button_click("btn_start_bundle_download")
        # Cancel auto-close timer if running
        if state.get("bundle_auto_close_task") and not state["bundle_auto_close_task"].done():
            state["bundle_auto_close_task"].cancel()
        state["bundle_auto_close_task"] = None
        bundle_auto_close_text.value = ""
        state["bundle_download_started"] = True
        logic.bundle_cancel_event.clear()
        bundle_url = getattr(CONFIG, "config", {}).get("BUNDLE_URL", getattr(CONFIG, "BUNDLE_URL", ""))
        dest_path = _get_bundle_dest_path()

        async def _extract_now():
            """Run the same extraction used by Check WSA after a successful download, showing progress in the visual card."""
            try:
                bundle_status_text.value = "Extracting bundle..."
                page.update()

                s = state
                s["check_phase"] = 1
                s["check_phase_title"] = "Bundle Check"
                s["check_sub_status"] = [
                    {"label": "Searching for bundle file", "status": "done", "detail": dest_path.name},
                    {"label": "Checking bundle integrity", "status": "pending", "detail": ""},
                    {"label": "Preparing cache folder", "status": "pending", "detail": ""},
                    {"label": "Extracting WSA packages", "status": "pending", "detail": ""},
                    {"label": "Cleaning up archive", "status": "pending", "detail": ""},
                ]
                s["log"] += "\n\n--- Extracting Bundle ---"
                await sync_ui()
                await rebuild_content()

                s["check_sub_status"][1]["status"] = "checking"
                s["log"] += "\n  \u23f3 Checking bundle integrity..."
                await sync_ui()
                await asyncio.sleep(0.1)

                size_mb = dest_path.stat().st_size / 1024 / 1024
                if size_mb > 1:
                    s["check_sub_status"][1]["status"] = "done"
                    s["check_sub_status"][1]["detail"] = f"{size_mb:.0f} MB"
                    s["log"] += f"\n  \u2713 Bundle size OK ({size_mb:.0f} MB)"
                else:
                    s["check_sub_status"][1]["status"] = "failed"
                    s["check_sub_status"][1]["detail"] = "Corrupt"
                    s["log"] += "\n  \u26A0 Bundle file appears corrupt (too small)."
                await sync_ui()

                s["check_sub_status"][2]["status"] = "checking"
                s["log"] += "\n  \u23f3 Preparing cache folder..."
                await sync_ui()
                try:
                    logic.CACHE_DIR.mkdir(parents=True, exist_ok=True)
                    s["check_sub_status"][2]["status"] = "done"
                    s["check_sub_status"][2]["detail"] = "Ready"
                    s["log"] += "\n  \u2713 Cache folder ready."
                except Exception:
                    s["check_sub_status"][2]["status"] = "failed"
                    s["check_sub_status"][2]["detail"] = "Failed"
                    s["log"] += "\n  \u26A0 Failed to create cache folder."
                await sync_ui()

                s["check_sub_status"][3]["status"] = "checking"
                s["log"] += "\n  \u23f3 Extracting bundle..."
                await sync_ui()
                process = await logic._create_subprocess(
                    "tar.exe", "-xvf", str(dest_path), "-C", str(logic.CACHE_DIR),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT,
                    creationflags=0x08000000 if sys.platform == "win32" else 0
                )
                count = 0
                while True:
                    line = await process.stdout.readline()
                    if not line:
                        break
                    line_text = line.decode(errors="replace").strip()
                    if line_text:
                        display_line = line_text if len(line_text) < 50 else "..." + line_text[-47:]
                        s["log"] = f"Extracting Bundle: {display_line}"
                        count += 1
                        if count % 20 == 0:
                            await sync_ui()
                await process.wait()
                s["check_sub_status"][3]["status"] = "done"
                s["check_sub_status"][3]["detail"] = "Extracted"
                s["log"] = "[\u2713] Bundle extracted successfully."
                await sync_ui()

                s["check_sub_status"][4]["status"] = "checking"
                s["log"] += "\n  \u23f3 Cleaning up archive..."
                await sync_ui()
                try:
                    os.remove(dest_path)
                    s["check_sub_status"][4]["status"] = "done"
                    s["check_sub_status"][4]["detail"] = "Removed"
                    s["log"] += "\n[\u2713] Bundle archive removed to save space."
                except Exception:
                    s["check_sub_status"][4]["status"] = "done"
                    s["check_sub_status"][4]["detail"] = "Skipped"
                await sync_ui()

                # ── Phase 3/3: System-Level Fixes ──────────────────────
                if not s.get("wsa_found", False):
                    s["check_phase"] = 2
                    s["check_phase_title"] = "System-Level Fixes"
                    s["check_sub_status"] = [
                        {"label": "Searching for bundle file", "status": "done", "detail": "Extracted"},
                        {"label": "Checking bundle integrity", "status": "done", "detail": "OK"},
                        {"label": "Preparing cache folder", "status": "done", "detail": "Ready"},
                        {"label": "Extracting WSA packages", "status": "done", "detail": "Extracted"},
                        {"label": "Cleaning up archive", "status": "done", "detail": "Removed"},
                    ]
                    s["log"] += "\n\n--- Phase 3/3: System-Level Fixes ---"
                    s["log"] += "\n  \u2139 Applying system-level fixes before installation..."
                    await sync_ui()

                    try:
                        await logic.virtualization_bypass_for_wsa("log")
                    except Exception as fix_err:
                        s["log"] += f"\n  \u26a0 Some system fixes encountered issues: {fix_err}"
                    await sync_ui()

                s["bundle_check_result"] = None
                page.snack_bar = ft.SnackBar(
                    ft.Text("Bundle downloaded and extracted successfully!"),
                    open=True, bgcolor=ft.Colors.GREEN_700
                )
            except Exception as ex:
                s["log"] += f"\n  \u26A0 Bundle extraction failed: {ex}"
                await sync_ui()
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Bundle downloaded but extraction failed: {ex}"),
                    open=True, bgcolor=ft.Colors.RED_700
                )
            page.update()

        if dest_path.exists():
            state["show_bundle_download"] = False
            # Cancel auto-close timer if running
            if state.get("bundle_auto_close_task") and not state["bundle_auto_close_task"].done():
                state["bundle_auto_close_task"].cancel()
            state["bundle_auto_close_task"] = None
            bundle_auto_close_text.value = ""
            state["bundle_download_started"] = False
            btn_start_bundle_download.disabled = False
            bundle_pb.visible = False
            await sync_ui()
            page.snack_bar = ft.SnackBar(ft.Text("Bundle already cached. Extracting..."), open=True, bgcolor=ft.Colors.GREEN_700)
            page.update()
            await _extract_now()
            return

        state["bundle_download_started"] = True
        btn_start_bundle_download.disabled = True
        bundle_pb.visible = True
        state["download_progress"] = 0.0
        bundle_status_text.value = "Downloading Bundle..."
        page.update()

        try:
            success = await logic.download_asset(bundle_url, dest_path, log_key="bundle_log", cancel_event=logic.bundle_cancel_event)
            state["show_bundle_download"] = False
            # Cancel auto-close timer if running
            if state.get("bundle_auto_close_task") and not state["bundle_auto_close_task"].done():
                state["bundle_auto_close_task"].cancel()
            state["bundle_auto_close_task"] = None
            bundle_auto_close_text.value = ""
            state["bundle_download_started"] = False
            btn_start_bundle_download.disabled = False
            bundle_pb.visible = False
            await sync_ui()
            if success:
                page.snack_bar = ft.SnackBar(ft.Text("Bundle downloaded! Extracting..."), open=True, bgcolor=ft.Colors.GREEN_700)
                page.update()
                await _extract_now()
            else:
                msg = "Bundle download cancelled." if logic.bundle_cancel_event.is_set() else "Failed to download bundle."
                page.snack_bar = ft.SnackBar(ft.Text(msg), open=True, bgcolor=ft.Colors.RED_700)
                page.update()
        except Exception as ex:
            state["show_bundle_download"] = False
            state["bundle_download_started"] = False
            btn_start_bundle_download.disabled = False
            bundle_pb.visible = False
            await sync_ui()
            page.snack_bar = ft.SnackBar(ft.Text(f"Bundle download error: {ex}"), open=True, bgcolor=ft.Colors.RED_700)
            page.update()

    btn_start_bundle_download = ft.FilledButton(
        "Start Download",
        icon=ft.Icons.DOWNLOAD,
        bgcolor=ACCENT,
        color=ft.Colors.WHITE,
        on_click=on_start_bundle_download
    )

    bundle_download_overlay = ft.Container(
        expand=True,
        bgcolor="#000000DD",
        visible=False,
        on_click=lambda _: None,
        alignment=ft.alignment.Alignment(0, 0),
        content=ft.Container(
            width=500, height=360,
            bgcolor=BG_DARK,
            border_radius=15,
            border=ft.Border.all(1, BORDER),
            padding=ft.Padding(24, 16, 24, 16),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
                controls=[
                    ft.Icon(ft.Icons.CLOUD_DOWNLOAD_ROUNDED, color=ACCENT, size=48),
                    ft.Text("Bundle Download", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "Download a pre-packaged bundle containing WSA Basic and Play Store in a single package.",
                        text_align=ft.TextAlign.CENTER, color=TEXT_SECONDARY, size=13
                    ),
                    ft.Container(
                        height=90,
                        padding=8,
                        border=ft.Border.all(1, "#3A3A3C"),
                        border_radius=10,
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=4,
                            controls=[
                                bundle_file_info,
                                ft.Divider(height=4, color="#3A3A3C"),
                                bundle_msg,
                            ],
                        )
                    ),
                    bundle_status_text,
                    bundle_auto_close_text,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[bundle_speed_text, bundle_eta_text],
                        width=400
                    ),
                    bundle_pb,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12,
                        controls=[
                            btn_cancel_bundle,
                            btn_start_bundle_download,
                        ]
                    )
                ]
            )
        )
    )


    # ── Extraction Failed Overlay (Re-download) ────────────────────────
    async def on_force_extract_cancel(e):
        ActivityLogger.button_click("btn_force_extract_cancel")
        await logic.cancel()
        state["show_force_extract"] = None
        logic.force_extract_choice = "cancel"
        logic.force_extract_event.set()
        await sync_ui()
        page.update()

    async def on_force_extract_redownload(e):
        ActivityLogger.button_click("btn_force_extract_redownload")
        state["show_force_extract"] = None
        logic.force_extract_choice = "redownload"
        logic.force_extract_event.set()
        await sync_ui()
        page.update()

    force_extract_overlay = ft.Container(
        expand=True,
        bgcolor="#000000DD",
        visible=False,
        on_click=lambda _: None,
        alignment=ft.alignment.Alignment(0, 0),
        content=ft.Container(
            width=480, height=340,
            bgcolor=BG_DARK,
            border_radius=15,
            border=ft.Border.all(1, BORDER),
            padding=24,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
                controls=[
                    ft.Icon(ft.Icons.WARNING_ROUNDED, color=WARNING, size=48),
                    ft.Text("Extraction Failed", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                    ft.Text(
                        f"The downloaded archive '{state.get('show_force_extract', 'unknown file')}' does not contain a valid WSA folder structure. "
                        "The file may be corrupted or incomplete.\n\n"
                        "Would you like to re-download the package?",
                        text_align=ft.TextAlign.CENTER, color=TEXT_SECONDARY, size=13
                    ),
                    ft.Container(height=10),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12,
                        controls=[
                            ft.TextButton("Cancel", on_click=on_force_extract_cancel),
                            ft.FilledButton("Re-download", on_click=on_force_extract_redownload, bgcolor=ACCENT, color=ft.Colors.WHITE)
                        ]
                    )
                ]
            )
        )
    )

    # ── Restart Overlay ─────────────────────────────────────────────────
    restart_countdown_text = ft.Text("", size=12, color="#FF453A", weight=ft.FontWeight.W_500)

    async def on_restart_later(e):
        state["show_restart_dialog"] = False
        restart_overlay.visible = False
        restart_overlay.update()
        logic.restart_action_event.set()

    async def on_restart_now(e):
        restart_later_btn.disabled = True
        restart_now_btn.disabled = True
        restart_overlay.update()
        for i in range(5, 0, -1):
            restart_countdown_text.value = f"Restarting in {i}s..."
            restart_countdown_text.update()
            await asyncio.sleep(1)
        os.system("shutdown /r /t 1")

    restart_later_btn = ft.TextButton("Restart Later", on_click=on_restart_later)
    restart_now_btn = ft.FilledButton(
        "Restart Now", bgcolor="#FF453A", color=ft.Colors.WHITE, on_click=on_restart_now,
    )

    restart_overlay = ft.Container(
        expand=True,
        bgcolor="#000000DD",
        visible=False,
        on_click=lambda _: None,
        alignment=ft.alignment.Alignment(0, 0),
        content=ft.Container(
            width=500, height=380,
            bgcolor=BG_DARK,
            border_radius=15,
            border=ft.Border.all(1, BORDER),
            padding=ft.Padding(24, 16, 24, 16),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                controls=[
                    ft.Row(
                        [ft.Icon(ft.Icons.RESTART_ALT_ROUNDED, color=ACCENT, size=48)],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text("Restart Required", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                    ft.Text(
                        "Windows features have been enabled successfully.\n"
                        "A system restart is required to apply these changes.",
                        size=13, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER, max_lines=3,
                    ),
                    ft.Container(
                        bgcolor="#1C1C1E",
                        border_radius=10,
                        border=ft.Border.all(1, "#3A3A3C"),
                        padding=ft.padding.all(12),
                        content=ft.Text("The installer will automatically resume after restart.", size=12, color=TEXT_SECONDARY),
                    ),
                    restart_countdown_text,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        spacing=12,
                        controls=[
                            restart_later_btn,
                            restart_now_btn,
                        ]
                    )
                ]
            )
        )
    )

    # ── UI Sync Logic (targeted updates) ──────────────────────────────
    async def sync_ui():
        step = state["current_step"]
        if step == 1:
            ui["check_log"].value = state["log"]
            ui["check_log"].update()

            phase = state.get("check_phase", 0)
            title = state.get("check_phase_title", "")
            ui["check_phase_header"].value = f"Phase {phase+1}/3: {title}"
            ui["check_phase_header"].update()

            sub_status = state.get("check_sub_status", [])
            rows = []
            for i, ss in enumerate(sub_status):
                detail = ss.get("detail", "")
                rows.append(ft.Row(spacing=10, controls=[
                    ft.Icon(ft.Icons.RADIO_BUTTON_UNCHECKED, size=18, color="#3A3A3C"),
                    ft.Text(ss["label"], size=12, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500, expand=True),
                    ft.Text(detail if detail else "\u2014", size=11, color="#3A3A3C"),
                ]))
                rows.append(ft.ProgressBar(visible=False, color=ACCENT, bgcolor="#3A3A3C", height=3, border_radius=2))

            for i, ss in enumerate(sub_status):
                row_idx = i * 2
                pb_idx = i * 2 + 1
                if row_idx >= len(rows): break
                row = rows[row_idx]
                pb = rows[pb_idx]
                detail = ss.get("detail", "")

                status = ss["status"]

                if status == "checking":
                    row.controls[0].name = ft.Icons.HOURGLASS_TOP; row.controls[0].color = ACCENT
                    row.controls[2].value = detail if detail else "Processing..."; row.controls[2].color = TEXT_SECONDARY
                    pb.visible = True; pb.color = ACCENT; pb.value = None
                elif status == "enabling":
                    row.controls[0].name = ft.Icons.SYNC; row.controls[0].color = WARNING
                    row.controls[2].value = detail if detail else "Enabling..."; row.controls[2].color = WARNING
                    pb.visible = True; pb.color = WARNING; pb.value = None
                elif status == "running":
                    row.controls[0].name = ft.Icons.PLAY_CIRCLE; row.controls[0].color = SUCCESS
                    row.controls[2].value = detail if detail else "Running"; row.controls[2].color = SUCCESS
                    pb.visible = False
                elif status == "stopped":
                    row.controls[0].name = ft.Icons.PAUSE_CIRCLE; row.controls[0].color = WARNING
                    row.controls[2].value = detail if detail else "Stopped"; row.controls[2].color = WARNING
                    pb.visible = False
                elif status in ("done", "enabled", "installed"):
                    row.controls[0].name = ft.Icons.CHECK_CIRCLE; row.controls[0].color = SUCCESS
                    row.controls[2].value = detail if detail else "Ready"; row.controls[2].color = SUCCESS
                    pb.visible = False
                elif status in ("failed", "disabled", "not_installed"):
                    row.controls[0].name = ft.Icons.CLOSE; row.controls[0].color = ft.Colors.RED_400
                    row.controls[2].value = detail if detail else "Failed"; row.controls[2].color = ft.Colors.RED_400
                    pb.visible = False
                else:
                    row.controls[0].name = ft.Icons.RADIO_BUTTON_UNCHECKED; row.controls[0].color = "#3A3A3C"
                    row.controls[2].value = "\u2014"; row.controls[2].color = "#3A3A3C"
                    pb.visible = False

            ui["check_sub_rows"].controls = rows
            ui["check_sub_rows"].update()

        elif step == 2:
            phase = state.get("install_phase", 0)
            title = state.get("install_phase_title", "")
            ui["install_phase_header"].value = f"Phase {phase+1}/6: {title}"
            ui["install_phase_header"].update()

            sub_status = state.get("install_sub_status", [])
            rows = []
            for i, ss in enumerate(sub_status):
                detail = ss.get("detail", "")
                rows.append(ft.Row(spacing=10, controls=[
                    ft.Icon(ft.Icons.RADIO_BUTTON_UNCHECKED, size=18, color="#3A3A3C"),
                    ft.Text(ss["label"], size=12, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500, expand=True),
                    ft.Text(detail if detail else "\u2014", size=11, color="#3A3A3C"),
                ]))
                rows.append(ft.ProgressBar(visible=False, color=ACCENT, bgcolor="#3A3A3C", height=3, border_radius=2))

            for i, ss in enumerate(sub_status):
                row_idx = i * 2
                pb_idx = i * 2 + 1
                if row_idx >= len(rows): break
                row = rows[row_idx]
                pb = rows[pb_idx]
                detail = ss.get("detail", "")

                if ss["status"] == "checking":
                    row.controls[0].name = ft.Icons.HOURGLASS_TOP
                    row.controls[0].color = ACCENT
                    row.controls[2].value = detail if detail else "Processing..."
                    row.controls[2].color = TEXT_SECONDARY
                    pb.visible = True
                    pb.color = ACCENT
                    pb.value = None
                elif ss["status"] == "done":
                    row.controls[0].name = ft.Icons.CHECK_CIRCLE
                    row.controls[0].color = SUCCESS
                    row.controls[2].value = detail if detail else "Done"
                    row.controls[2].color = SUCCESS
                    pb.visible = False
                elif ss["status"] == "failed":
                    row.controls[0].name = ft.Icons.CLOSE
                    row.controls[0].color = ft.Colors.RED_400
                    row.controls[2].value = detail if detail else "Failed"
                    row.controls[2].color = ft.Colors.RED_400
                    pb.visible = False
                else:
                    row.controls[0].name = ft.Icons.RADIO_BUTTON_UNCHECKED
                    row.controls[0].color = "#3A3A3C"
                    row.controls[2].value = "\u2014"
                    row.controls[2].color = "#3A3A3C"
                    pb.visible = False

            ui["install_sub_rows"].controls = rows
            ui["install_sub_rows"].update()
            ui["install_log"].value = state["install_log"]
            ui["install_log"].update()

        elif step == 3:
            phase = state.get("ps_phase", 0)
            title = state.get("ps_phase_title", "")
            ui["ps_phase_header"].value = f"Phase {phase+1}/7: {title}"
            ui["ps_phase_header"].update()

            sub_status = state.get("ps_sub_status", [])
            rows = []
            for i, ss in enumerate(sub_status):
                detail = ss.get("detail", "")
                rows.append(ft.Row(spacing=10, controls=[
                    ft.Icon(ft.Icons.RADIO_BUTTON_UNCHECKED, size=18, color="#3A3A3C"),
                    ft.Text(ss["label"], size=12, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500, expand=True),
                    ft.Text(detail if detail else "\u2014", size=11, color="#3A3A3C"),
                ]))
                rows.append(ft.ProgressBar(visible=False, color=ACCENT, bgcolor="#3A3A3C", height=3, border_radius=2))

            for i, ss in enumerate(sub_status):
                row_idx = i * 2
                pb_idx = i * 2 + 1
                if row_idx >= len(rows): break
                row = rows[row_idx]
                pb = rows[pb_idx]
                detail = ss.get("detail", "")

                if ss["status"] == "checking":
                    row.controls[0].name = ft.Icons.HOURGLASS_TOP
                    row.controls[0].color = ACCENT
                    row.controls[2].value = detail if detail else "Processing..."
                    row.controls[2].color = TEXT_SECONDARY
                    pb.visible = True
                    pb.color = ACCENT
                    pb.value = None
                elif ss["status"] == "done":
                    row.controls[0].name = ft.Icons.CHECK_CIRCLE
                    row.controls[0].color = SUCCESS
                    row.controls[2].value = detail if detail else "Done"
                    row.controls[2].color = SUCCESS
                    pb.visible = False
                elif ss["status"] == "failed":
                    row.controls[0].name = ft.Icons.CLOSE
                    row.controls[0].color = ft.Colors.RED_400
                    row.controls[2].value = detail if detail else "Failed"
                    row.controls[2].color = ft.Colors.RED_400
                    pb.visible = False
                else:
                    row.controls[0].name = ft.Icons.RADIO_BUTTON_UNCHECKED
                    row.controls[0].color = "#3A3A3C"
                    row.controls[2].value = "\u2014"
                    row.controls[2].color = "#3A3A3C"
                    pb.visible = False

            ui["ps_sub_rows"].controls = rows
            ui["ps_sub_rows"].update()
            ui["ps_log"].value    = state["ps_log"]
            ui["ps_log"].update()

        # Download Overlay Sync
        if state["show_download"]:
            download_overlay.visible = True
            if not state["downloading"] and not download_options_list.content.controls:
                # Fetch options if not already loaded
                download_status_text.value = getattr(CONFIG, "DL_STATUS_FETCHING", "Fetching packages from GitHub...")
                download_overlay.update()
                
                assets = await logic.fetch_github_assets(state["show_download"])
                state["download_options"] = assets
                
                # Auto-resume/selection logic
                found_index = -1
                is_found_complete = False
                download_options_list.content.controls = []
                for i, a in enumerate(assets):
                    size_mb = f"{a['size'] / (1024*1024):.1f} MB"
                    readable_name = clean_asset_name(a['name'])
                    
                    # Check for FULL or PARTIAL package in cache
                    f_name = a['name']
                    cache_file = logic.CACHE_DIR / f_name
                    
                    # Check partial via presence of any chunked .part file
                    has_partial = False
                    try:
                        prefix = f_name + ".part"
                        if logic.CACHE_DIR.exists():
                            for item in logic.CACHE_DIR.iterdir():
                                if item.name.startswith(prefix):
                                    has_partial = True
                                    break
                    except Exception:
                        pass
                    
                    if cache_file.exists():
                        local_size = cache_file.stat().st_size
                        server_size = a.get('size', 0)
                        
                        if local_size != server_size:
                            try:
                                cache_file.unlink()
                            except: pass
                            has_partial = False
                            if not is_found_complete:
                                found_index = i
                                is_found_complete = False
                                state["needs_manual_redownload"] = True
                        else:
                            if not is_found_complete:
                                found_index = i
                                is_found_complete = True
                    elif has_partial and not is_found_complete:
                        found_index = i
                        is_found_complete = False
                    
                    # Smart recommendation logic based on latest release info
                    is_rec = False
                    n_l = a['name'].lower()
                    
                    if state["show_download"] == "nogapps":
                        # Basic Package Step (Step 2)
                        # Recommend: No GApps + No Amazon + No Root
                        if "gapps" not in n_l and ("noamazon" in n_l or "removedamazon" in n_l):
                            if "magisk" not in n_l and "kernelsu" not in n_l:
                                is_rec = True
                        # EXTRA SAFETY: If we are in nogapps mode, NEVER show Google Play Store labels as recommended
                        if "gapps" in n_l:
                            is_rec = False
                    else:
                        # Play Store Step (Step 3)
                        # Recommend: GApps + No Amazon + No Root
                        if "gapps" in n_l and ("noamazon" in n_l or "removedamazon" in n_l):
                            if "magisk" not in n_l and "kernelsu" not in n_l:
                                is_rec = True
                    
                    # Blocklist check
                    block_list = getattr(CONFIG, "config", {}).get("block_list_package", {})
                    if state["show_download"] == "nogapps":
                        blocked_indices = block_list.get("base_package", [0])
                    else:
                        blocked_indices = block_list.get("playstore_package", [0])
                        
                    is_blocked = (i + 1) in blocked_indices
                    
                    def strike(text):
                        return ''.join([c + '\u0336' for c in text])
                    
                    if is_blocked:
                        label_text = strike(readable_name) + f" ({size_mb}) [CORRUPTED]"
                        radio_ctrl = ft.Radio(value=str(i), label=label_text, disabled=True)
                        
                        def on_block_hover(e):
                            if e.data == "true":
                                e.page.snack_bar = ft.SnackBar(ft.Text(getattr(CONFIG, "config", {}).get("BLACKLIST_REASON", "This package is currently unavailable due to corruption.")), open=True)
                                e.page.update()

                        disabled_item = ft.Container(
                            content=radio_ctrl,
                            opacity=0.5,
                            on_hover=on_block_hover
                        )
                        download_options_list.content.controls.append(disabled_item)
                    else:
                        rec_tag = getattr(CONFIG, "DL_REC_TAG", " â­ [RECOMMENDED]") if is_rec else ""
                        label_text = f"{readable_name} ({size_mb}){rec_tag}"
                        download_options_list.content.controls.append(
                            ft.Radio(value=str(i), label=label_text)
                        )
                
                # Set default status before refining for cache/recommendations
                download_status_text.value = getattr(CONFIG, "DL_STATUS_PROMPT", "Select a package to continue")
                btn_download_confirm.text = getattr(CONFIG, "DL_BTN_NORMAL", "Download & Install")

                # Set default selection
                if found_index != -1:
                    download_options_list.value = str(found_index)
                    btn_download_confirm.disabled = False
                    
                    # Update status and button text to reflect cached state
                    a = assets[found_index]
                    if is_found_complete:
                        download_status_text.value = f"Ready: Found cached package ({a['name']})"
                        btn_download_confirm.text = getattr(CONFIG, "DL_BTN_CACHED", "Use Cached Package")
                        
                        download_overlay.update()
                    elif state.get("needs_manual_redownload"):
                        download_status_text.value = f"Corrupted package detected: {a['name']}"
                        btn_download_confirm.text = "Re-download"
                        
                        download_overlay.update()
                        state["needs_manual_redownload"] = False
                    else:
                        download_status_text.value = f"Partial download detected: {a['name']}"
                        btn_download_confirm.text = getattr(CONFIG, "DL_BTN_RESUME", "Resume Download")
                        
                        download_overlay.update()
                        # Auto-resume partial download only if CONFIG.PARTIAL_AUTO_DOWNLOAD is enabled
                        if str(getattr(CONFIG, "PARTIAL_AUTO_DOWNLOAD", "False")).lower() == "true":
                            await asyncio.sleep(0.8)
                            page.run_task(on_download_click, None)
                elif assets:
                    # Fallback to smart recommended if no cache found
                    for i, a in enumerate(assets):
                        n_l = a['name'].lower()
                        is_rec_match = False
                        if state["show_download"] == "nogapps":
                            if "gapps" not in n_l and ("noamazon" in n_l or "removedamazon" in n_l) and ("magisk" not in n_l):
                                is_rec_match = True
                        else:
                            if "gapps" in n_l and ("noamazon" in n_l or "removedamazon" in n_l) and ("magisk" not in n_l):
                                is_rec_match = True
                        
                        if is_rec_match:
                            download_options_list.value = str(i)
                            btn_download_confirm.disabled = False
                            
                            # Check if recommended has a partial download to resume
                            part_prefix = a['name'] + ".part"
                            has_part_fallback = False
                            try:
                                if logic.CACHE_DIR.exists():
                                    for item in logic.CACHE_DIR.iterdir():
                                        if item.name.startswith(part_prefix):
                                            has_part_fallback = True
                                            break
                            except:
                                pass
                                
                            if has_part_fallback:
                                download_status_text.value = f"Partial download detected: {a['name']}"
                                btn_download_confirm.text = getattr(CONFIG, "DL_BTN_RESUME", "Resume Download")
                                
                            break
                
                if not assets:
                    download_status_text.value = getattr(CONFIG, "DL_STATUS_OFFLINE", "No packages found. Check your internet.")
                
                download_overlay.update()
            
            if state["downloading"]:
                download_pb.visible = True
                download_pb.value = state["download_progress"]
                download_speed_text.value = state.get("download_speed", "")
                download_eta_text.value = state.get("download_eta", "")
                
                if state["download_progress"] >= 1.0:
                    download_status_text.value = "Success! Package ready."
                    # The logic class will eventually reset show_download to None
                elif state["download_speed"] == "Merging...":
                    download_status_text.value = getattr(CONFIG, "DL_STATUS_MERGING", "Merging 30 chunks into final package...")
                else:
                    download_status_text.value = f"{getattr(CONFIG, 'DL_STATUS_DOWNLOADING', 'Downloading... ')}{int(state['download_progress']*100)}%"
            
            download_overlay.update()
        else:
            download_overlay.visible = False
            download_options_list.content.controls = [] # Clear for next time
            download_overlay.update()

        # Force Extract Overlay Sync
        if state["show_force_extract"]:
            force_extract_overlay.visible = True
            force_extract_overlay.update()
        else:
            force_extract_overlay.visible = False
            force_extract_overlay.update()

        # Bundle Download Sync
        if state.get("show_bundle_download", False):
            bundle_download_overlay.visible = True
            if state.get("bundle_download_started", False):
                bundle_pb.visible = True
                bundle_pb.value = state.get("download_progress", 0.0)
                bundle_speed_text.value = state.get("download_speed", "")
                bundle_eta_text.value = state.get("download_eta", "")
                pct = int(bundle_pb.value * 100)
                if state.get("download_speed", "") == "Merging...":
                    bundle_status_text.value = f"Merging chunks... {pct}%"
                else:
                    bundle_status_text.value = f"Downloading Bundle... {pct}%"
            bundle_download_overlay.update()
            bundle_pb.update()
            bundle_speed_text.update()
            bundle_eta_text.update()
            bundle_status_text.update()
            btn_cancel_bundle.update()
            btn_start_bundle_download.update()
        else:
            bundle_download_overlay.visible = False
            bundle_download_overlay.update()

        # Restart Dialog Sync
        if state.get("show_restart_dialog", False):
            restart_countdown_text.value = ""
            restart_later_btn.disabled = False
            restart_now_btn.disabled = False
            restart_overlay.visible = True
            restart_overlay.update()
        else:
            restart_overlay.visible = False
            restart_overlay.update()

    async def rebuild_sidebar():
        sidebar_col.controls = [
            sidebar_item(s, state["current_step"])
            for s in get_steps()
        ]
        sidebar_col.update()

    async def rebuild_content():
        # Check overlay mode first (About / Advanced pages)
        overlay = state.get("overlay_mode")
        if overlay == "about":
            body = page_about(ui)
        elif overlay == "advanced":
            body = page_advanced(page, ui, logic)
        else:
            step = state["current_step"]
            if   step == 0: body = page_intro()
            elif step == 1: body = page_check_wsa(ui)
            elif step == 2: body = page_install_wsa(ui)
            elif step == 3: body = page_playstore(ui)
            else:           body = page_complete(ui)

        # ── Animated Transition ───────────────────────────────────────
        animated_body = ft.Container(
            content=body,
            opacity=0,
            offset=ft.Offset(0, 0.02),
            animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
            animate_offset=ft.Animation(500, ft.AnimationCurve.DECELERATE),
        )
        
        content_area.content = animated_body
        content_area.update()
        
        # Trigger entrance animation
        await asyncio.sleep(0.05)
        animated_body.opacity = 1
        animated_body.offset = ft.Offset(0, 0)
        animated_body.update()

        await update_buttons()
        await sync_ui()

    _rebuild_fn = rebuild_content

    async def update_buttons():
        # Overlay mode: show back button, hide next button
        if state.get("overlay_mode"):
            btn_back.visible = True
            btn_back.text = "\u2190 Back"
            btn_next.visible = False
            btn_download_bundle.visible = False
            btn_back.update()
            btn_next.update()
            btn_download_bundle.update()
            return

        btn_next.visible = True
        step = state["current_step"]
        btn_back.visible  = step > 0 and step < 4
        btn_back.text = "\u2190 Back"
        btn_next.disabled = False

        bundle_url_set = bool(getattr(CONFIG, "config", {}).get("BUNDLE_URL", getattr(CONFIG, "BUNDLE_URL", "")))
        bundle_check = state.get("bundle_check_result")
        btn_download_bundle.visible = bundle_url_set and step == 1 and bundle_check in ("not_found", "partial")

        if step == 1:
            if state["checking"]:
                btn_next.text = "Scanning\u2026"
                btn_next.disabled = True
            elif not state["scan_complete"] and state["log"] == CONFIG.SCAN_AWAITING_TEXT:
                btn_next.text = "Scan System"
                btn_next.disabled = False
            elif state["scan_complete"]:
                btn_next.text = "Continue \u2192"
                btn_next.disabled = False
                if state["wsa_found"]:
                    btn_next.text = "Continue \u2192 (WSA Found)"
            else:
                btn_next.text = "Continue \u2192"

        elif step == 2:
            if state["installing"]:
                btn_next.text = "Installing\u2026"
                btn_next.disabled = True
            elif not state["install_done"]:
                btn_next.text = "Install WSA"
            else:
                btn_next.text = "Continue \u2192"

        elif step == 3:
            if state["ps_installing"]:
                btn_next.text = "Patching\u2026"
                btn_next.disabled = True
            elif not state["ps_done"]:
                btn_next.text = "Add Play Store"
            else:
                btn_next.text = "Continue \u2192"

        elif step == 4:
            btn_next.text    = "Finish"
            btn_next.disabled = False
        else:
            btn_next.text = "Continue \u2192"

        btn_back.update()
        btn_next.update()
        btn_download_bundle.update()

    # ── Logic class wiring ─────────────────────────────────────────────
    last_step = -1
    async def on_update():
        nonlocal last_step
        if state["current_step"] != last_step:
            ActivityLogger.step_enter(state["current_step"])
            await rebuild_sidebar()
            await rebuild_content()
            last_step = state["current_step"]
        else:
            await sync_ui()
            await update_buttons()

    logic = InstallerLogic(state, on_update=on_update, page=page)
    logic.restart_action_event = restart_action_event

    # ── Admin Check Implementation ────────────────────────────────────
    async def check_admin_privileges():
        if not is_admin():
            admin_overlay.visible = True
            page.update()

    await check_admin_privileges()

    async def on_next(e):
        step = state["current_step"]
        ActivityLogger.button_click("btn_next", step=step)
        await logic.cancel()

        if step == 1:
            if not state["scan_complete"] and state["log"] == CONFIG.SCAN_AWAITING_TEXT:
                await logic.Check_wsa()

                if state.get("bundle_check_result") in ("not_found", "partial"):
                    state["check_phase"] = 1
                    state["check_phase_title"] = "Bundle Check"
                    if state["bundle_check_result"] == "not_found":
                        state["check_sub_status"] = [
                            {"label": "Searching for bundle file", "status": "done", "detail": "Not found"},
                        ]
                    else:
                        state["check_sub_status"] = [
                            {"label": "Searching for bundle file", "status": "done", "detail": "Partial found"},
                        ]

                await rebuild_content()
                # ── Cache check before dialog ──────────────────────────────
                cache_result = logic._check_cache_packages()
                if cache_result:
                    state["bundle_check_result"] = "found"
                    state["log"] += "\n  \u2713 Cache already has both packages (nogapps + gapps) — no download needed."
                    await sync_ui()
                else:
                    state["log"] += "\n  \u26A0 Cache missing one or both packages — download will be required."
                    await sync_ui()

                if state.get("bundle_check_result") in ("not_found", "partial"):
                    await open_bundle_download_for_check()
                return

            if state["scan_complete"] and state["wsa_found"]:
                state["current_step"] = 3
                await rebuild_sidebar()
                await rebuild_content()
                return

        elif step == 2 and not state["install_done"]:
            # Check for download trigger
            state["show_download"] = None # Reset
            await logic.install_wsa()
            if state["show_download"]:
                # Logic signaled that assets are missing
                return
            if not state["install_done"]: return

        elif step == 3 and not state["ps_done"]:
            state["show_download"] = None # Reset
            await logic.add_playStore()
            if state["show_download"]:
                # Logic signaled that assets are missing
                return
            if not state["ps_done"]: return

        elif step == 4:
            await logic.youtube_subscribe()
            return

        # Show mandatory ad before proceeding to next step
        if step < 4 and (str(getattr(CONFIG, "DIRCET_LINK_ENABLE_ADS", "False")).lower() == "true" or str(getattr(CONFIG, "ENABLE_ADS", "False")).lower() == "true"):
            ad_overlay.visible = True
            btn_next.disabled = True
            page.update()

            if str(getattr(CONFIG, "EXTERNAL_BROWSER", "False")).lower() == "true":
                # Launch the Monetag SmartLink in the system browser
                await page.launch_url(getattr(CONFIG, "AD_SPONSOR_URL", "https://omg10.com/4/109267472"))

                # Wait for browser to open and become active
                await asyncio.sleep(5)

                # Enhanced Ad Automation
                if str(getattr(CONFIG, "config", {}).get("AD_AUTO_CLICKING", getattr(CONFIG, "AD_AUTO_CLICKING", "True"))).lower() == "true":
                    set_user_input(False) # Block user input
                    try:
                        # Find browser window using pywinauto
                        desktop = Desktop(backend="uia")
                        browser_window = None
                        # Search for any open browser window
                        for w in desktop.windows():
                            title = w.window_text().lower()
                            if any(b in title for b in ["edge", "chrome", "firefox", "brave", "opera"]):
                                browser_window = w
                                break

                        if browser_window:
                            browser_window.set_focus()
                            rect = browser_window.rectangle()

                            # Perform random clicks strictly within the browser's website area
                            for _ in range(6):
                                # Safe zone: Top + 160 (avoid tabs/address) to Bottom - 60
                                x = random.randint(rect.left + 80, rect.right - 80)
                                y = random.randint(rect.top + 160, rect.bottom - 80)
                                pyautogui.moveTo(x, y, duration=0.4)
                                pyautogui.click()
                                await asyncio.sleep(0.8)

                            # Minimize the browser window (Try targeted first, then hotkey)
                            try:
                                if browser_window:
                                    browser_window.minimize()
                                else:
                                    pyautogui.hotkey('win', 'down')
                                    await asyncio.sleep(0.3)
                                    pyautogui.hotkey('win', 'down')
                            except:
                                pyautogui.hotkey('win', 'down')
                                await asyncio.sleep(0.3)
                                pyautogui.hotkey('win', 'down')
                    except Exception as e:
                        print(f"Ad automation error: {e}")
                    finally:
                        set_user_input(True) # Ensure input is unblocked

                # Overlay countdown
                timer_prefix = getattr(CONFIG, "AD_TIMER_PREFIX", "Ad finishes in ")
                wait_prefix = getattr(CONFIG, "AD_WAIT_PREFIX", "Wait ")
                for i in range(3, 0, -1):
                    ad_timer_text.value = f"{timer_prefix}{i}s..."
                    btn_next.text = f"{wait_prefix}{i}s..."
                    ad_pb.value = (3 - i) / 3
                    ad_pb.update()
                    ad_timer_text.update()
                    btn_next.update()
                    await asyncio.sleep(1)
            else:
                ad_closed_event = threading.Event()

                def start_ad_window():
                    try:
                        # Launch as a separate process to avoid thread/DPI conflicts with Flet
                        url = getattr(CONFIG, "AD_SPONSOR_URL", "https://omg10.com/4/10926747")
                        return subprocess.Popen([sys.executable, __file__, "--ad", url, "15"])
                    except Exception as e:
                        print(f"Internal Ad Process Error: {e}")
                        ad_closed_event.set()
                        return None

                ad_process = start_ad_window()
                timer_prefix = getattr(CONFIG, "AD_TIMER_PREFIX", "Ad finishes in ")
                wait_prefix = getattr(CONFIG, "AD_WAIT_PREFIX", "Wait ")

                # Overlay countdown
                for i in range(15, 0, -1):
                    if ad_process and ad_process.poll() is not None:
                        break
                    ad_timer_text.value = f"{timer_prefix}{i}s..."
                    btn_next.text = f"{wait_prefix}{i}s..."
                    ad_pb.value = (15 - i) / 15
                    ad_pb.update()
                    ad_timer_text.update()
                    btn_next.update()
                    await asyncio.sleep(1)

                # Ensure the window has signaled closing (or timed out)
                ad_closed_event.wait(timeout=2)

            ad_pb.value = 1
            ad_overlay.visible = False
            btn_next.disabled = False
            btn_next.text = "Continue \u2192"
            page.update()

        state["current_step"] = min(step + 1, 4)
        await rebuild_sidebar()
        await rebuild_content()

    _nav_busy = False

    async def _show_overlay(mode):
        nonlocal _nav_busy
        if _nav_busy:
            return
        _nav_busy = True
        try:
            state["overlay_mode"] = mode
            await rebuild_content()
        finally:
            _nav_busy = False

    async def _hide_overlay():
        # No guard needed — only called from on_back which holds _nav_busy
        await logic.cancel()
        state["overlay_mode"] = None
        await rebuild_content()

    async def on_back(e):
        nonlocal _nav_busy
        if _nav_busy:
            return
        _nav_busy = True
        try:
            ActivityLogger.button_click("btn_back", step=state["current_step"])
            # If overlay is active, close it instead of going back a step
            if state.get("overlay_mode"):
                await _hide_overlay()
                return
            # Kill any running background process
            await logic.cancel()
            # Reset completion state for the step we are leaving
            current = state["current_step"]
            if current == 1:
                state["scan_complete"] = False
                state["wsa_found"] = False
                state["wsa_running"] = False
                state["vhd_enabled"] = None
                state["log"] = CONFIG.SCAN_AWAITING_TEXT
                state["check_phase"] = 0
                state["check_phase_title"] = ""
                state["bundle_check_result"] = None
                state["show_bundle_download"] = False
                # Cancel auto-close timer if running
                if state.get("bundle_auto_close_task") and not state["bundle_auto_close_task"].done():
                    state["bundle_auto_close_task"].cancel()
                state["bundle_auto_close_task"] = None
                bundle_auto_close_text.value = ""
            elif current == 2:
                state["install_done"] = False
                state["install_progress"] = 0.0
                state["install_log"] = "Awaiting install\u2026"
                state["install_phase"] = 0
                state["install_phase_title"] = ""
            elif current == 3:
                state["ps_done"] = False
                state["ps_progress"] = 0.0
                state["ps_log"] = "Awaiting patch\u2026"
                state["ps_phase"] = 0
                state["ps_phase_title"] = ""
            state["current_step"] = max(current - 1, 0)
            await rebuild_sidebar()
            await rebuild_content()
        finally:
            _nav_busy = False

    btn_next.on_click  = on_next
    btn_back.on_click  = on_back
    btn_next.style     = ft.ButtonStyle(
        bgcolor={ft.ControlState.DEFAULT: ACCENT, ft.ControlState.HOVERED: ACCENT_HOVER},
        color=ft.Colors.WHITE,
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=ft.Padding.symmetric(horizontal=20, vertical=12),
        elevation=0,
    )
    btn_back.style     = ft.ButtonStyle(
        bgcolor=ft.Colors.TRANSPARENT,
        color=TEXT_SECONDARY,
        shape=ft.RoundedRectangleBorder(radius=8),
        side=ft.BorderSide(1, BORDER),
        padding=ft.Padding.symmetric(horizontal=20, vertical=12),
        elevation=0,
    )

    # ── Window controls ────────────────────────────────────────────────
    async def _close(e):
        ActivityLogger.button_click("btn_close")
        ActivityLogger.session_end()
        await logic.youtube_subscribe()
    async def _minimize(e):
        ActivityLogger.button_click("btn_minimize")
        page.window.minimized = True
        page.update()

    async def _maximize(e):
        ActivityLogger.button_click("btn_maximize")
        page.window.maximized = not page.window.maximized
        page.update()

    # ── Window dragging

    async def visit_youtube(e):
        ActivityLogger.button_click("btn_visit_youtube")
        await page.launch_url(getattr(CONFIG, "YT_CHANNEL_URL", "https://www.youtube.com/@AT_Tech_Zone"))

    async def support_dev(e):
        ActivityLogger.button_click("btn_support_dev")
        await page.launch_url(getattr(CONFIG, "COFFEE_DONATION_URL", "https://buymeacoffee.com/mrcyberdev"))

    # ── Window dragging ────────────────────────────────────────────────
    title_text = ft.Text(
        CONFIG.APP_TITLE,
        color=TEXT_SECONDARY, size=13,
        weight=ft.FontWeight.W_500,
    )

    # --- About button (circle, replaces spacer) ---
    about_btn = ft.Container(
        width=28, height=28,
        border_radius=14,
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
        border=ft.border.all(1, BORDER),
        alignment=ft.alignment.Alignment(0, 0),
        tooltip="About",
        on_click=lambda e: page.run_task(_show_overlay, "about"),
        content=ft.Icon(ft.Icons.INFO_OUTLINED, size=14, color=TEXT_SECONDARY),
    )

    title_bar = ft.WindowDragArea(
        content=ft.Container(
            height=44,
            bgcolor=BG_SIDEBAR,
            border=ft.Border.only(bottom=ft.BorderSide(1, BORDER)),
            padding=ft.Padding.symmetric(horizontal=16),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    traffic_lights(
                        on_close=_close,
                        on_minimize=_minimize,
                        on_maximize=_maximize,
                    ),
                    title_text,
                    about_btn,
                ],
            ),
        ),
    )

    # ── Animated Button Container ─────────────────────────────────────
    btn_next_container = ft.Container(
        content=btn_next,
        border_radius=8,
        animate=ft.Animation(600),
        bgcolor=ACCENT,
    )

    # ── Bundle Download Button & Handler ──────────────────────────────
    async def on_bundle_download_click(e):
        ActivityLogger.button_click("btn_bundle_download")
        # Cancel auto-close timer if running
        if state.get("bundle_auto_close_task") and not state["bundle_auto_close_task"].done():
            state["bundle_auto_close_task"].cancel()
        state["bundle_auto_close_task"] = None
        bundle_auto_close_text.value = ""
        logic.bundle_cancel_event.clear()
        state["bundle_download_started"] = False
        btn_start_bundle_download.disabled = False
        bundle_pb.value = 0
        bundle_pb.visible = False
        bundle_status_text.value = "Checking for existing bundle..."
        bundle_speed_text.value = ""
        bundle_eta_text.value = ""
        btn_cancel_bundle.text = "Cancel"
        btn_cancel_bundle.visible = True
        state["show_bundle_download"] = True
        state["download_progress"] = 0.0
        await sync_ui()
        page.update()

        dest_path = _get_bundle_dest_path()
        name = dest_path.name
        has_partial = False
        partial_bytes = 0
        try:
            prefix = str(dest_path) + ".part"
            for item in dest_path.parent.iterdir():
                if str(item).startswith(prefix):
                    has_partial = True
                    try:
                        partial_bytes += item.stat().st_size
                    except Exception:
                        pass
        except Exception:
            pass

        if dest_path.exists():
            size = dest_path.stat().st_size
            size_str = f"{size / 1024 / 1024:.1f} MB" if size > 1024 * 1024 else f"{size / 1024:.1f} KB"
            bundle_status_text.value = f"Ready: Found cached bundle ({name}, {size_str})"
            bundle_file_info.value = f"Bundle: {name}"
            btn_start_bundle_download.text = "Use Cached Bundle"
        elif has_partial:
            size_str = f"{partial_bytes / 1024 / 1024:.1f} MB" if partial_bytes > 1024 * 1024 else f"{partial_bytes / 1024:.1f} KB"
            bundle_status_text.value = f"Partial download detected: {name} ({size_str} saved) — resuming..."
            bundle_file_info.value = f"Bundle: {name}"
            btn_start_bundle_download.text = "Resume Download"
            page.update()
            await asyncio.sleep(0.3)
            await on_start_bundle_download(e=None)
        else:
            bundle_status_text.value = "No cached bundle found. Start a fresh download."
            bundle_file_info.value = f"Bundle: {name}"
            btn_start_bundle_download.text = "Start Download"
        page.update()

    async def open_bundle_download_for_check():
        """Auto-open bundle download dialog after scan completes, configured for the check result."""
        bundle_check = state.get("bundle_check_result")
        if bundle_check not in ("not_found", "partial"):
            return

        # Cancel any existing auto-close timer
        if state.get("bundle_auto_close_task") and not state["bundle_auto_close_task"].done():
            state["bundle_auto_close_task"].cancel()
        state["bundle_auto_close_task"] = None

        logic.bundle_cancel_event.clear()
        state["bundle_download_started"] = False
        btn_start_bundle_download.disabled = False
        bundle_pb.value = 0
        bundle_pb.visible = False
        bundle_speed_text.value = ""
        bundle_eta_text.value = ""
        bundle_auto_close_text.value = ""
        state["download_progress"] = 0.0
        dest_path = _get_bundle_dest_path()
        name = dest_path.name

        if bundle_check == "not_found":
            bundle_status_text.value = "No cached bundle found. Start a fresh download."
            bundle_file_info.value = f"Bundle: {name}"
            btn_start_bundle_download.text = "Start Download"
            btn_cancel_bundle.text = "Skip for Now"
            btn_cancel_bundle.visible = True
        elif bundle_check == "partial":
            has_partial = False
            partial_bytes = 0
            try:
                prefix = str(dest_path) + ".part"
                for item in dest_path.parent.iterdir():
                    if str(item).startswith(prefix):
                        has_partial = True
                        try:
                            partial_bytes += item.stat().st_size
                        except Exception:
                            pass
            except Exception:
                pass
            size_str = f"{partial_bytes / 1024 / 1024:.1f} MB" if partial_bytes > 1024 * 1024 else f"{partial_bytes / 1024:.1f} KB"
            bundle_status_text.value = f"Partial download detected: {name} ({size_str} saved) — resuming..."
            bundle_file_info.value = f"Bundle: {name}"
            btn_start_bundle_download.text = "Resume Download"
            btn_cancel_bundle.visible = False

        state["show_bundle_download"] = True
        await sync_ui()
        page.update()

        if bundle_check == "partial":
            await asyncio.sleep(0.3)
            await on_start_bundle_download(e=None)
        elif bundle_check == "not_found":
            # Auto-close timer: 10 seconds
            async def _auto_close_countdown():
                for i in range(10, 0, -1):
                    if state.get("bundle_download_started", False):
                        # Download started, cancel timer
                        bundle_auto_close_text.value = ""
                        await sync_ui()
                        return
                    if not state.get("show_bundle_download", False):
                        # Dialog was closed manually
                        return
                    bundle_auto_close_text.value = f"Auto-closing in {i}s — start download to keep open"
                    await sync_ui()
                    await asyncio.sleep(1)
                # Timer expired, close dialog
                if not state.get("bundle_download_started", False):
                    state["show_bundle_download"] = False
                    bundle_auto_close_text.value = ""
                    await sync_ui()
            state["bundle_auto_close_task"] = asyncio.create_task(_auto_close_countdown())

    btn_download_bundle = ft.FilledButton(
        "Download Bundle", 
        icon=ft.Icons.DOWNLOAD, 
        bgcolor=ft.Colors.TRANSPARENT,
        color=ACCENT,
        on_click=on_bundle_download_click,
        visible=False
    )

    # ── Bottom bar ─────────────────────────────────────────────────────
    bottom_bar = ft.Container(
        height=79,
        border=ft.Border.only(top=ft.BorderSide(1, BORDER)),
        padding=ft.Padding.symmetric(horizontal=24),
        bgcolor=BG_SIDEBAR,
        content=ft.Row(
            spacing=12,
            controls=[
                btn_download_bundle,
                ft.Container(expand=True),
                btn_back,
                btn_next_container,
            ],
        ),
    )

    # ── Runtime glass / transparency slider ────────────────────────────
    glass_label = ft.Text(
        f"{getattr(CONFIG, 'GLASS_SLIDER_LABEL', 'Transparency')}: {GLASS_LEVEL}",
        color=TEXT_SECONDARY, size=10, weight=ft.FontWeight.BOLD
    )

    async def on_glass_change(e):
        new_level = int(e.control.value or 0)
        global GLASS_LEVEL, ALPHA, BG_DARK, BG_CARD, BG_SIDEBAR
        GLASS_LEVEL = max(0, min(100, new_level))
        ALPHA = f"{int((1 - GLASS_LEVEL/100) * 255):02X}" if GLASS_LEVEL else "FF"
        BG_DARK = _apply_glass_alpha(CONFIG.COLOR_BG_DARK, ALPHA)
        BG_CARD = _apply_glass_alpha(CONFIG.COLOR_BG_CARD, ALPHA)
        BG_SIDEBAR = _apply_glass_alpha(CONFIG.COLOR_BG_SIDEBAR, ALPHA)
        # Repaint every visible control's background alpha in place
        _walk_and_repaint_glass(page.controls, ALPHA)
        # Window bg must stay fully transparent so the OS desktop shows through;
        # the visible "transparency" is produced by the inner BG_* colors' alpha
        page.window.bgcolor = ft.Colors.TRANSPARENT
        glass_label.value = f"{getattr(CONFIG, 'GLASS_SLIDER_LABEL', 'Transparency')}: {GLASS_LEVEL}"
        glass_label.update()
        glass_slider.update()
        page.update()

    glass_slider = ft.Slider(
        min=0, max=100, divisions=100, value=GLASS_LEVEL,
        label="{value}%", width=176,
        tooltip=getattr(CONFIG, "GLASS_SLIDER_TOOLTIP", "Adjust window transparency in real time"),
        on_change=on_glass_change,
    )

    glass_section = ft.Container(
        visible=bool(getattr(CONFIG, "ENABLE_GLASS_SLIDER", True)),
        padding=ft.Padding.only(left=4, right=4, top=6, bottom=6),
        content=ft.Column(
            spacing=4,
            controls=[
                glass_label,
                glass_slider,
            ],
        ),
    )

    # ── Root layout ────────────────────────────────────────────────────
    sidebar = ft.Container(
        width=200,
        bgcolor=BG_SIDEBAR,
        border=ft.Border.only(right=ft.BorderSide(1, BORDER)),
        padding=ft.Padding.only(left=12, right=12, top=20, bottom=10),
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Text(getattr(CONFIG, "SIDEBAR_STEPS_HEADER", "SETUP STEPS"), color=TEXT_SECONDARY, size=10,
                        weight=ft.FontWeight.BOLD),
                ft.Container(height=12),
                sidebar_col,
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row(
                        spacing=6,
                        controls=[
                            ft.Icon(ft.Icons.SETTINGS_OUTLINED, color=TEXT_SECONDARY, size=15),
                            ft.Text("Advanced", color=TEXT_SECONDARY, size=12, weight=ft.FontWeight.W_500),
                        ],
                    ),
                    tooltip="Advanced Settings",
                    on_click=lambda e: page.run_task(_show_overlay, "advanced"),
                    padding=ft.padding.symmetric(horizontal=8, vertical=8),
                    border_radius=6,
                ),
                ft.Divider(height=1, color=BORDER),
                ft.Container(height=8),
                ft.Column(
                    spacing=0,
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                spacing=6,
                                controls=[
                                    ft.Icon(ft.Icons.COFFEE, color=WARNING, size=13),
                                    ft.Text(getattr(CONFIG, "SIDEBAR_SUPPORT_LABEL", "SUPPORT DEVELOPER"), color=TEXT_SECONDARY, size=11, weight=ft.FontWeight.BOLD),
                                ],
                            ),
                            tooltip=getattr(CONFIG, "CREDIT_COFFEE_TOOLTIP", "Buy Me a Coffee"),
                            on_click=support_dev,
                        ),
                        ft.Container(height=10),
                        ft.Container(
                            content=ft.Row(
                                spacing=6,
                                controls=[
                                    ft.Icon(ft.Icons.CODE_ROUNDED, color=ACCENT, size=13),
                                    ft.Text(getattr(CONFIG, "SIDEBAR_CHANNEL_LABEL", "BY AT TECH ZONE"), color=TEXT_SECONDARY, size=11),
                                ],
                            ),
                            tooltip=getattr(CONFIG, "CREDIT_YOUTUBE_TOOLTIP", "Visit YouTube Channel"),
                            on_click=visit_youtube,
                        ),
                        ft.Container(height=2),
                        ft.Row(
                            spacing=6,
                            controls=[
                                ft.Icon(ft.Icons.CODE_ROUNDED, color=ACCENT, size=13),
                                ft.Text(getattr(CONFIG, "CREDIT_YOUTUBE_TEXT", "BY MR CYBER"), color=TEXT_SECONDARY, size=11),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )

    main_area = ft.Column(
        expand=True,
        spacing=0,
        controls=[
            title_bar,
            ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    sidebar,
                    ft.Container(
                        expand=True,
                        bgcolor=BG_DARK,
                        content=ft.Column(
                            expand=True,
                            spacing=0,
                            controls=[
                                ft.Container(
                                    expand=True,
                                    padding=ft.Padding.only(
                                        left=32, right=32, top=28, bottom=8
                                    ),
                                    content=content_area,
                                ),
                                bottom_bar,
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )

    page.add(
        ft.Container(
            expand=True,
            bgcolor=BG_DARK,
            border_radius=18,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            border=ft.Border.all(2, BORDER),
            content=ft.Stack(
                controls=[
                    main_area,
                    download_overlay,
                    bundle_download_overlay,
                    restart_overlay,
                    ad_overlay,
                    admin_overlay,
                    force_extract_overlay,
                ]
            ),
        )
    )
    
    # Final render sequence
    await rebuild_sidebar()
    await rebuild_content()
    await page.window.center()
    page.window.visible = True
    page.update()

    _refresh_ui_ready = True

    # initial render is now handled above

    # ── Animation Task ────────────────────────────────────────────────
    async def animation_task():
        while True:
            try:
                # Determine if we should animate
                step = state["current_step"]
                busy = state["checking"] or state["installing"] or state["ps_installing"] or (str(getattr(CONFIG, "DIRCET_LINK_ENABLE_ADS", "False")).lower() == "true"

 and ad_overlay.visible)
                
                # Animate whenever the button is NOT busy AND enabled
                should_animate = not busy and not btn_next.disabled

                if should_animate:
                    # Alternating colors
                    btn_next_container.bgcolor = ft.Colors.RED
                    btn_next.style.bgcolor = ft.Colors.TRANSPARENT
                    btn_next_container.update()
                    btn_next.update()
                    await asyncio.sleep(0.6)
                    
                    btn_next_container.bgcolor = ft.Colors.BLUE
                    btn_next_container.update()
                    await asyncio.sleep(0.6)
                else:
                    # Reset to normal
                    btn_next_container.bgcolor = ACCENT
                    btn_next.style.bgcolor = {ft.ControlState.DEFAULT: ACCENT, ft.ControlState.HOVERED: ACCENT_HOVER}
                    btn_next_container.update()
                    btn_next.update()
                    await asyncio.sleep(1)
            except:
                break # Page probably closed

    asyncio.create_task(animation_task())


# ==============================
# UNINSTALL DIALOG (module-level)
# ==============================
# UNINSTALL DIALOG (module-level)
# ==============================
async def uninstall_app(page: ft.Page):
    page.title = getattr(CONFIG, "UNINSTALLER_TITLE", "WSA Uninstaller")
    page.window.width = 520
    page.window.height = 480
    page.window.resizable = False
    page.window.maximizable = False
    page.window.title_bar_hidden = True
    page.window.skip_task_bar = False
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.bgcolor = ft.Colors.TRANSPARENT
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {
        CONFIG.FONT_NAME_PRIMARY: CONFIG.FONT_URL_PRIMARY,
        "Consolas": "Consolas"
    }

    _CARD_W = 480
    _UNCHECKED = ft.Icons.RADIO_BUTTON_UNCHECKED
    _SPINNER = ft.Icons.SYNC

    step_data = [
        {"label": "WSA Detection",               "status": "pending", "detail": "\u2014"},
        {"label": "Stopping WSA Processes",      "status": "pending", "detail": "\u2014"},
        {"label": "Backup User Data",             "status": "pending", "detail": "\u2014"},
        {"label": "Removing Appx Package",        "status": "pending", "detail": "\u2014"},
        {"label": "Deleting Installation Files",  "status": "pending", "detail": "\u2014"},
        {"label": "Removing Background Service",  "status": "pending", "detail": "\u2014"},
        {"label": "Cleanup Complete",             "status": "pending", "detail": "\u2014"},
    ]

    row_icon   = [ft.Icon(_UNCHECKED, size=22, color="#3A3A3C") for _ in step_data]
    row_label  = [ft.Text(d["label"], size=14, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500) for d in step_data]
    row_detail = [ft.Text("\u2014", size=13, color="#3A3A3C") for _ in step_data]
    row_bar    = [ft.ProgressBar(visible=False, color=ft.Colors.RED_ACCENT_400, bgcolor="#3A3A3C", height=3, border_radius=2) for _ in step_data]

    def _build_rows():
        c = []
        for i in range(len(step_data)):
            c.append(ft.Row(spacing=10, controls=[row_icon[i], row_label[i], row_detail[i]], alignment=ft.MainAxisAlignment.START))
            c.append(row_bar[i])
        return c

    step_rows = ft.Column(spacing=2, controls=_build_rows(), horizontal_alignment=ft.CrossAxisAlignment.START)

    def _set_step(idx, status, detail=None):
        step_data[idx]["status"] = status
        if detail is not None:
            step_data[idx]["detail"] = detail
            row_detail[idx].value = detail
        if status == "pending":
            row_icon[idx].name = _UNCHECKED; row_icon[idx].color = "#3A3A3C"
            row_label[idx].color = TEXT_PRIMARY; row_detail[idx].color = "#3A3A3C"; row_bar[idx].visible = False
        elif status == "active":
            row_icon[idx].name = _SPINNER; row_icon[idx].color = ft.Colors.RED_ACCENT_400
            row_label[idx].color = ft.Colors.RED_ACCENT_400; row_detail[idx].color = ft.Colors.RED_ACCENT_400; row_bar[idx].visible = True; row_bar[idx].value = None
        elif status == "done":
            row_icon[idx].name = ft.Icons.CHECK_CIRCLE; row_icon[idx].color = SUCCESS
            row_label[idx].color = TEXT_PRIMARY; row_detail[idx].color = SUCCESS; row_bar[idx].visible = True; row_bar[idx].value = 1.0
        elif status == "error":
            row_icon[idx].name = ft.Icons.CANCEL; row_icon[idx].color = ft.Colors.RED_400
            row_label[idx].color = ft.Colors.RED_400; row_detail[idx].color = ft.Colors.RED_400; row_bar[idx].visible = True; row_bar[idx].value = 0
        page.update()

    un_state = {"uninstall_log": getattr(CONFIG, "UNINSTALLER_AWAITING_TEXT", "Awaiting confirmation\u2026")}

    log_box = ft.Text(un_state["uninstall_log"], color="#8E8E93", size=10, font_family="Consolas", selectable=True)
    log_container = ft.Container(
        width=_CARD_W, height=80, padding=13,
        bgcolor="#111113", border_radius=8,
        border=ft.Border.all(1, "#3A3A3C"),
        content=ft.Column([log_box], scroll=ft.ScrollMode.ADAPTIVE, spacing=0, expand=True),
    )

    def _append_log(msg):
        log_box.value = (log_box.value + "\n" + msg).strip()
        log_box.update()

    _un_orig_print = _builtins.print
    _un_log_file = os.path.join(os.environ.get("TEMP", "."), "_wsa_uninst_debug.log")

    def _un_print(*args, **kwargs):
        try:
            _msg = ' '.join(str(a) for a in args)
            with open(_un_log_file, "a", encoding="utf-8") as _f:
                _f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {_msg}\n")
                _f.flush()
        except Exception:
            pass
        try:
            _append_log(' '.join(str(a) for a in args))
        except Exception:
            _un_orig_print(*args, **kwargs)

    _builtins.print = _un_print

    async def sync_uninstaller():
        pass

    logic = InstallerLogic(un_state, on_update=sync_uninstaller, page=page)

    async def start_uninstallation(e):
        uninstall_btn.disabled = True
        cancel_btn.disabled = True
        confirm_check.disabled = True

        ActivityLogger.button_click("btn_start_uninstall")

        dialog_card.border = ft.Border.all(2, ft.Colors.RED_ACCENT_400)
        status_text.value = getattr(CONFIG, "UNINSTALLER_PROGRESS_TEXT", "UNINSTALLING...")
        status_text.color = ft.Colors.RED_ACCENT_400
        confirm_check.label_style.color = ft.Colors.RED_ACCENT_400
        backup_check.disabled = True
        page.update()

        # ── Step 0: WSA Detection ───────────────────────────────────────
        _set_step(0, "active", "checking...")
        _append_log("Detecting WSA installation...")

        def _detect_wsa():
            try:
                r = subprocess.run(
                    ["powershell", "-NoProfile", "-Command",
                     "Get-AppxPackage -Name 'MicrosoftCorporationII.WindowsSubsystemForAndroid' | Select-Object -ExpandProperty InstallLocation"],
                    capture_output=True, text=True, timeout=15,
                    creationflags=0x08000000)
                loc = (r.stdout or "").strip()
                return loc if loc else None
            except Exception:
                return None

        wsa_location = await asyncio.to_thread(_detect_wsa)
        if not wsa_location:
            _set_step(0, "error", "not installed")
            _append_log("WSA is not installed. Nothing to uninstall.")
            await asyncio.sleep(2)
            page.window.close()
            sys.exit(0)
        _set_step(0, "done", wsa_location[:50])
        _append_log(f"WSA found at: {wsa_location}")
        await asyncio.sleep(0.3)

        # ── Step 1: Stopping WSA Processes ──────────────────────────────
        _set_step(1, "active", "stopping...")
        _append_log("Stopping WSA processes...")
        await asyncio.sleep(0.3)

        await logic.uninstall_wsa_logic()

        _set_step(1, "done", "stopped")

        # ── Step 2: Backup User Data (visual) ──────────────────────────────
        _set_step(2, "active", "checking...")
        _append_log("Checking backup status...")

        if backup_check.value:
            if _is_backup_valid():
                _set_step(2, "done", "already exists")
                _append_log("Valid backup found, skipping.")
            else:
                _set_step(2, "active", "backing up...")
                _append_log("Backing up WSA data before uninstall...")
                await _perform_backup_with_progress(2)
        else:
            _set_step(2, "done", "skipped")
            _append_log("Backup skipped.")

        _set_step(3, "active", "removing...")
        _append_log("Removing Appx package...")
        await asyncio.sleep(0.3)

        _set_step(3, "done", "removed")
        _set_step(4, "active", "deleting...")
        _append_log("Deleting installation files...")
        await asyncio.sleep(0.3)

        _set_step(4, "done", "deleted")
        _set_step(5, "active", "removing...")
        _append_log("Removing background service...")

        _remove_windows_service()

        _set_step(5, "done", "removed")
        _set_step(6, "active", "finalizing...")
        _append_log("Finalizing cleanup...")
        await asyncio.sleep(0.3)

        _set_step(6, "done", "complete")
        _append_log("Uninstallation successful!")
        status_text.value = getattr(CONFIG, "UNINSTALLER_PROGRESS_SUCCESS", "Uninstallation Successful!")
        status_text.color = SUCCESS
        dialog_card.border = ft.Border.all(2, SUCCESS)
        page.update()
        await asyncio.sleep(2.5)
        page.window.close()
        sys.exit(0)

    async def on_checkbox_change(e):
        ActivityLogger.event("SELECT", "uninstall_checkbox", detail=f"checked={confirm_check.value}")
        if confirm_check.value:
            dialog_card.border = ft.Border.all(2, SUCCESS)
            confirm_check.label_style.color = SUCCESS
            page.update()

            confirm_check.disabled = True
            cancel_btn.disabled = True
            wait_prefix = getattr(CONFIG, "UNINSTALLER_WAIT_PREFIX", "Wait ")
            for i in range(3, 0, -1):
                uninstall_btn.visible = True
                uninstall_btn.text = f"{wait_prefix}{i}s..."
                page.update()
                await asyncio.sleep(1)
            uninstall_btn.text = getattr(CONFIG, "UNINSTALLER_CONFIRM_TEXT", "Confirm Uninstall")
            uninstall_btn.disabled = False
            cancel_btn.disabled = False
        else:
            dialog_card.border = ft.Border.all(1, BORDER)
            confirm_check.label_style.color = BORDER
        page.update()

    status_text = ft.Text(getattr(CONFIG, "UNINSTALLER_TITLE", "WSA Uninstaller"), size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)
    version_text = ft.Text("This action will permanently remove WSA and all Android apps", size=12, color=WARNING)

    confirm_check = ft.Checkbox(
        label=getattr(CONFIG, "UNINSTALLER_CHECKBOX", "I acknowledge that all Android data will be deleted\nIf backup option above is selected data is preserved only"),
        on_change=on_checkbox_change,
        label_style=ft.TextStyle(color=BORDER, size=12)
    )

    # Backup toggle: shown if no backup exists, hidden if backup already exists
    _has_backup = _wsa_backup_exists()
    if _has_backup:
        backup_check = ft.Checkbox(
            label="Backup already exists (from repair)",
            value=True, disabled=True,
            label_style=ft.TextStyle(color=SUCCESS, size=11),
        )
    else:
        backup_check = ft.Checkbox(
            value=True,
            label="Backup data before uninstall (recommended)",
            label_style=ft.TextStyle(color=TEXT_SECONDARY, size=11),
        )

    async def _perform_backup_with_progress(step_idx):
        src = _wsa_data_path()
        dst = _wsa_backup_path()
        if not os.path.isdir(src):
            _set_step(step_idx, "done", "no data folder")
            _append_log("WSA data folder not found, skipping backup.")
            return
        try:
            os.makedirs(dst, exist_ok=True)
            total_size = 0
            file_count = 0
            for dp, dns, fns in os.walk(src):
                for fn in fns:
                    try:
                        total_size += os.path.getsize(os.path.join(dp, fn))
                        file_count += 1
                    except OSError:
                        pass
            if total_size == 0:
                _set_step(step_idx, "done", "empty folder")
                _append_log("No data to backup.")
                return
            copied = 0
            start_t = time.time()
            for dp, dns, fns in os.walk(src):
                rel = os.path.relpath(dp, src)
                dest_dir = os.path.join(dst, rel) if rel else dst
                os.makedirs(dest_dir, exist_ok=True)
                for fn in fns:
                    sfp = os.path.join(dp, fn)
                    dfp = os.path.join(dest_dir, fn)
                    try:
                        shutil.copy2(sfp, dfp)
                        copied += os.path.getsize(sfp)
                    except OSError:
                        pass
                    if file_count > 10:
                        pct = copied / max(total_size, 1)
                        spd = copied / max(time.time() - start_t, 0.001)
                        eta = (total_size - copied) / max(spd, 1)
                        _set_step(step_idx, "active", f"{pct:.0%} | {spd/1024/1024:.1f} MB/s | ETA {eta:.0f}s")
            _set_step(step_idx, "done", f"{file_count} files")
            _append_log(f"Backup complete ({file_count} files).")
        except Exception as ex:
            _set_step(step_idx, "error", "failed")
            _append_log(f"Backup error: {ex}")

    uninstall_btn = ft.FilledButton(
        getattr(CONFIG, "UNINSTALLER_BTN_UNINSTALL", "Uninstall"), icon=ft.Icons.DELETE_FOREVER_ROUNDED, color=ft.Colors.WHITE,
        bgcolor="#B02A37", visible=False, on_click=start_uninstallation,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=ft.Padding.symmetric(horizontal=20, vertical=12))
    )
    cancel_btn = ft.TextButton(getattr(CONFIG, "UNINSTALLER_BTN_CANCEL", "Cancel"), on_click=lambda _: sys.exit(1), style=ft.ButtonStyle(color=TEXT_SECONDARY))

    dialog_card = ft.Container(
        width=520, height=460,
        padding=ft.Padding(20, 6, 20, 6),
        border_radius=18, bgcolor=BG_DARK,
        border=ft.Border.all(1, BORDER),
        content=ft.Column(
            spacing=0, expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Row([ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=WARNING, size=22), status_text],
                       alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                version_text,
                ft.Divider(height=3, color="#3A3A3C"),
                ft.Container(
                    expand=True,
                    border=ft.Border.all(1, BORDER),
                    border_radius=14, padding=12, bgcolor=BG_CARD,
                    content=step_rows,
                ),
                ft.Container(height=6),
                log_container,
                ft.Container(height=4),
                confirm_check,
                ft.Container(height=2),
                backup_check,
                ft.Container(height=6),
                ft.Row([cancel_btn, uninstall_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ],
        ),
    )

    page.add(ft.Container(
        expand=True, alignment=ft.Alignment(0, 0), bgcolor=ft.Colors.TRANSPARENT,
        content=ft.WindowDragArea(content=dialog_card),
    ))
    page.update()
    await page.window.center()
    page.window.visible = True
    page.update()


# ==============================
# FILE SHARING DIALOG (module-level)
# ==============================
async def file_sharing_app(page: ft.Page):
    mode = sys.argv[2] if len(sys.argv) > 2 else "user"
    adv = _read_adv_state()
    letter = adv.get(f"share_{mode}_prev_letter", "X" if mode == "user" else "R") + ":"
    label = adv.get(f"share_{mode}_label", "Windows Subsystem For Android" if mode == "user" else "WSA RootFile System")
    adb = resource_path(os.path.join("assets", "adb.exe"))
    apk = resource_path(os.path.join("assets", "wsa-webdav.apk"))
    device = getattr(CONFIG, "WSA_DEVICE", "127.0.0.1:58526")

    page.title = "WSA Installer \u2014 File Sharing"
    page.window.width = 520
    page.window.height = 470
    page.window.resizable = False
    page.window.maximizable = False
    page.window.title_bar_hidden = True
    page.window.skip_task_bar = False
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.bgcolor = ft.Colors.TRANSPARENT
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {CONFIG.FONT_NAME_PRIMARY: CONFIG.FONT_URL_PRIMARY, "Consolas": "Consolas"}

    _CARD_W = 480
    _UNCHECKED = ft.Icons.RADIO_BUTTON_UNCHECKED
    _SPINNER = ft.Icons.SYNC

    if mode == "root":
        step_labels = [
            "WSA Installed", "Check WSA Status", "Start WSA (if needed)", "Connect ADB",
            "Install WebDAV Server APK", "Detect Magisk Root",
            "Start WebDAV Server", "Port Forward (8088)",
            "Configure WebDAV Client", "Mount Network Drive",
        ]
    else:
        step_labels = [
            "WSA Installed", "Check WSA Status", "Start WSA (if needed)", "Connect ADB",
            "Install WebDAV Server APK", "Start WebDAV Server",
            "Port Forward (8088)", "Configure WebDAV Client",
            "Mount Network Drive",
        ]

    step_data = [{"label": s, "status": "pending", "detail": "\u2014"} for s in step_labels]
    row_icon   = [ft.Icon(_UNCHECKED, size=20, color="#3A3A3C") for _ in step_data]
    row_label  = [ft.Text(d["label"], size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500) for d in step_data]
    row_detail = [ft.Text("\u2014", size=12, color="#3A3A3C") for _ in step_data]
    row_bar    = [ft.ProgressBar(visible=False, color=ACCENT, bgcolor="#3A3A3C", height=3, border_radius=2) for _ in step_data]

    def _build_rows():
        c = []
        for i in range(len(step_data)):
            c.append(ft.Row(spacing=8, controls=[row_icon[i], row_label[i], row_detail[i]], alignment=ft.MainAxisAlignment.START))
            c.append(row_bar[i])
        return c

    def _set_step(idx, status, detail=None):
        step_data[idx]["status"] = status
        if detail is not None:
            step_data[idx]["detail"] = detail
            row_detail[idx].value = detail
        if status == "pending":
            row_icon[idx].name = _UNCHECKED; row_icon[idx].color = "#3A3A3C"
            row_label[idx].color = TEXT_PRIMARY; row_detail[idx].color = "#3A3A3C"; row_bar[idx].visible = False
        elif status == "active":
            row_icon[idx].name = _SPINNER; row_icon[idx].color = ACCENT
            row_label[idx].color = ACCENT; row_detail[idx].color = ACCENT; row_bar[idx].visible = True; row_bar[idx].value = None
        elif status == "done":
            row_icon[idx].name = ft.Icons.CHECK_CIRCLE; row_icon[idx].color = SUCCESS
            row_label[idx].color = TEXT_PRIMARY; row_detail[idx].color = SUCCESS; row_bar[idx].visible = True; row_bar[idx].value = 1.0
        elif status == "error":
            row_icon[idx].name = ft.Icons.CANCEL; row_icon[idx].color = ft.Colors.RED_400
            row_label[idx].color = ft.Colors.RED_400; row_detail[idx].color = ft.Colors.RED_400; row_bar[idx].visible = True; row_bar[idx].value = 0
        page.update()

    step_rows = ft.Column(spacing=2, controls=_build_rows(), horizontal_alignment=ft.CrossAxisAlignment.START)
    log_box = ft.Text("", color="#8E8E93", size=10, font_family="Consolas", selectable=True)
    log_container = ft.Container(
        height=100, padding=10, bgcolor="#111113", border_radius=8,
        border=ft.Border.all(1, "#3A3A3C"),
        content=ft.Column([log_box], scroll=ft.ScrollMode.ADAPTIVE, spacing=0, expand=True),
    )

    def _append_log(msg):
        log_box.value = (log_box.value + "\n" + msg).strip()
        page.update()

    _fs_orig_print = _builtins.print
    _fs_log_file = os.path.join(os.environ.get("TEMP", "."), "_wsa_fs_debug.log")

    def _fs_print(*args, **kwargs):
        try:
            _msg = ' '.join(str(a) for a in args)
            with open(_fs_log_file, "a", encoding="utf-8") as _f:
                _f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {_msg}\n")
                _f.flush()
        except Exception:
            pass
        try:
            _append_log(' '.join(str(a) for a in args))
        except Exception:
            _fs_orig_print(*args, **kwargs)

    _builtins.print = _fs_print

    status_text = ft.Text("File Sharing Setup", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)
    version_text = ft.Text(f"{mode.upper()} mode  \u2022  {letter}  \u2192  {label}", size=12, color=TEXT_SECONDARY)

    def _text(r):
        out = r.stdout.decode("utf-8", errors="ignore") if hasattr(r, "stdout") else ""
        err = r.stderr.decode("utf-8", errors="ignore") if hasattr(r, "stderr") else ""
        return (out + " " + err).strip()

    def _adb_run(args, timeout=15):
        return subprocess.run([adb, "-s", device] + args, capture_output=True, creationflags=0x08000000, timeout=timeout)

    async def _wait_retry(seconds):
        for _ in range(int(seconds * 10)):
            await asyncio.sleep(0.1)
        return False

    import time as _time

    dialog_card = ft.Container(
        width=520, height=420,
        padding=ft.Padding(20, 6, 20, 6),
        border_radius=18, bgcolor=BG_DARK,
        border=ft.Border.all(1, BORDER),
        content=ft.Column(
            spacing=0, expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Row([ft.Icon(ft.Icons.FOLDER_SHARED, color=ACCENT, size=22), status_text],
                       alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                version_text,
                ft.Divider(height=3, color="#3A3A3C"),
                ft.Container(
                    border=ft.Border.all(1, BORDER),
                    border_radius=14, padding=12, bgcolor=BG_CARD,
                    content=step_rows,
                ),
                ft.Container(height=6),
                log_container,
                ft.Container(height=6),
            ],
        ),
    )

    page.add(ft.Container(
        expand=True, alignment=ft.Alignment(0, 0), bgcolor=ft.Colors.TRANSPARENT,
        content=ft.WindowDragArea(content=dialog_card),
    ))
    page.update()
    await page.window.center()
    page.window.visible = True
    page.update()

    try:
        wsa_port = 58526
        try:
            wsa_port = int(device.split(":")[1])
        except (IndexError, ValueError):
            pass

        def _check_wsa_port():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect(("127.0.0.1", wsa_port))
                s.close()
                return True
            except (OSError, socket.error):
                return False

        # ── Step 0: Check WSA Installed ──
        _set_step(0, "active", "checking...")
        _append_log("Checking if WSA is installed...")
        try:
            _wsa_check = subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command",
                 "Get-AppxPackage *WindowsSubsystemForAndroid* | Select-Object -ExpandProperty InstallLocation"],
                capture_output=True, creationflags=0x08000000, timeout=15
            )
            _wsa_loc = _wsa_check.stdout.decode("utf-8", errors="ignore").strip()
        except Exception:
            _wsa_loc = ""
        if _wsa_loc:
            _set_step(0, "done", _wsa_loc[:50])
            _append_log(f"WSA found at: {_wsa_loc}")
        else:
            _set_step(0, "error", "not installed")
            raise Exception("WSA is not installed on this system")

        # ── Step 1-2: Ensure WSA Running ──
        _set_step(1, "active", "checking...")
        wsa_running = _check_wsa_port()
        if wsa_running:
            _set_step(1, "done", "already running")
            _set_step(2, "done", "skipped")
        else:
            _set_step(1, "done", "not running")
            _set_step(2, "active", "starting...")
            subprocess.run(["powershell", "Start-Process", "wsa://system"], capture_output=True, creationflags=0x08000000, timeout=10)
            _append_log("Waiting for WSA to start...")
            ok = False
            for attempt in range(1, 31):
                await asyncio.sleep(1)
                if _check_wsa_port():
                    ok = True
                    _append_log(f"WSA started (attempt {attempt})")
                    break
                if attempt % 10 == 0:
                    _append_log(f"Still waiting... ({attempt}s)")
            if ok:
                _set_step(2, "done", "running")
            else:
                _set_step(2, "error", "failed to start")
                raise Exception("WSA could not be started")

        # ── Step 3: Connect ADB ──
        _set_step(3, "active", "connecting...")
        _append_log(f"Connecting ADB to {device}...")
        adb_ok = False
        for attempt in range(1, 16):
            try:
                subprocess.run([adb, "connect", device], capture_output=True, creationflags=0x08000000, timeout=5)
                await _wait_retry(2)
                r = subprocess.run([adb, "devices"], capture_output=True, creationflags=0x08000000, timeout=5)
                result = _text(r).lower()
                if f"{device}\tdevice" in result:
                    adb_ok = True
                    _append_log(f"ADB connected (attempt {attempt})")
                    break
            except Exception as ex:
                _append_log(f"ADB error: {ex}")
            if attempt % 5 == 0:
                _append_log("Restarting ADB server...")
                subprocess.run([adb, "kill-server"], capture_output=True, creationflags=0x08000000, timeout=5)
                await _wait_retry(2)
                subprocess.run([adb, "start-server"], capture_output=True, creationflags=0x08000000, timeout=5)
                await _wait_retry(2)
            await _wait_retry(3)
        if adb_ok:
            _set_step(3, "done", "connected")
        else:
            raise Exception("ADB connection failed")

        # ── Step 4: Install WebDAV APK ──
        _set_step(4, "active", "checking...")
        apk_installed = False
        try:
            r = _adb_run(["shell", "pm", "list", "packages", "com.wsa.webdav"], timeout=10)
            if b"package:com.wsa.webdav" in r.stdout:
                apk_installed = True
        except Exception:
            pass
        if apk_installed:
            _set_step(4, "done", "already installed")
        else:
            _append_log("Installing WebDAV APK...")
            for attempt in range(1, 4):
                _set_step(4, "active", f"try {attempt}/3")
                page.update()
                r = _adb_run(["install", "-r", apk], timeout=30)
                out = _text(r)
                if r.returncode == 0:
                    _set_step(4, "done", "installed")
                    break
                _append_log(f"Retry {attempt}/3: {out.strip()[:60]}")
                if attempt == 2:
                    _append_log("Uninstalling conflicting APK...")
                    _adb_run(["uninstall", "com.wsa.webdav"], timeout=10)
                    await _wait_retry(1)
                if attempt == 3:
                    _set_step(4, "error", out.strip()[:40] or "APK install failed")
                    raise Exception(f"APK install failed: {out.strip()[:80]}")

        _off = 0
        if mode == "root":
            _set_step(5, "active", "checking...")
            for attempt in range(1, 4):
                r = _adb_run(["shell", "su", "-c", "whoami"], timeout=10)
                out = _text(r)
                if "root" in out.lower():
                    _set_step(5, "done", "root available")
                    break
                _append_log(f"Root check {attempt}/3: no root access")
                if attempt == 3:
                    _set_step(5, "error", "no root access")
                    raise Exception("Magisk root not detected")
            _off = 1

        # ── Step: Start WebDAV Server ──
        for attempt in range(1, 4):
            _set_step(5 + _off, "active", f"try {attempt}/3")
            page.update()
            if mode == "root":
                _adb_run(["shell", "su", "-c",
                          "sh /data/data/com.wsa.webdav/files/app.sh start"], timeout=10)
                await asyncio.sleep(2)
                r = _adb_run(["shell", "su", "-c", "pidof com.wsa.webdav"], timeout=5)
            else:
                _adb_run(["shell", "am", "start", "-n", "com.wsa.webdav/.MainActivity"], timeout=10)
                await asyncio.sleep(2)
                r = _adb_run(["shell", "pidof", "com.wsa.webdav"], timeout=5)
            out = _text(r).strip()
            if out and out.isdigit():
                _set_step(5 + _off, "done", f"PID {out}")
                break
            _append_log(f"Retry {attempt}/3: server not running")
            if attempt == 2:
                _append_log("Force-stopping WebDAV...")
                if mode == "root":
                    _adb_run(["shell", "su", "-c",
                              "sh /data/data/com.wsa.webdav/files/app.sh stop"], timeout=5)
                else:
                    _adb_run(["shell", "am", "force-stop", "com.wsa.webdav"], timeout=5)
                await _wait_retry(1)
            if attempt == 3:
                _set_step(5 + _off, "error", "server not running")
                raise Exception("WebDAV server failed to start")

        # ── Step: Port Forward ──
        for attempt in range(1, 4):
            _set_step(6 + _off, "active", f"try {attempt}/3")
            page.update()
            _adb_run(["forward", "tcp:8088", "tcp:8088"], timeout=5)
            r = _adb_run(["forward", "--list"], timeout=5)
            if "8088" in _text(r).lower():
                _set_step(6 + _off, "done", "8088 forwarded")
                break
            _append_log(f"Retry {attempt}/3: port not listed")
            if attempt == 2:
                _append_log("Removing stale forward...")
                _adb_run(["forward", "--remove", "tcp:8088"], timeout=5)
                await _wait_retry(1)
            if attempt == 3:
                _set_step(6 + _off, "error", "port 8088 not listed")
                raise Exception("Port forward failed")

        # ── Step: Configure WebDAV Client (non-fatal) ──
        _append_log("Configuring Windows WebDAV client...")
        try:
            subprocess.run(["reg", "add", "HKLM\\SYSTEM\\CurrentControlSet\\Services\\WebClient\\Parameters",
                           "/v", "BasicAuthLevel", "/t", "REG_DWORD", "/d", "2", "/f"],
                          capture_output=True, creationflags=0x08000000, timeout=5)
            subprocess.run(["reg", "add", "HKLM\\SYSTEM\\CurrentControlSet\\Services\\WebClient\\Parameters",
                           "/v", "FileSizeLimitInBytes", "/t", "REG_DWORD", "/d", "4294967295", "/f"],
                          capture_output=True, creationflags=0x08000000, timeout=5)
            r = subprocess.run(["sc", "query", "WebClient"], capture_output=True, text=True, creationflags=0x08000000, timeout=5)
            if "RUNNING" not in r.stdout:
                _append_log("Starting WebClient service...")
                subprocess.run(["net", "start", "WebClient"], capture_output=True, creationflags=0x08000000, timeout=10)
            import socket as _sckt
            reachable = False
            for _ in range(3):
                try:
                    s = _sckt.create_connection(("127.0.0.1", 8088), timeout=3)
                    s.close()
                    reachable = True
                    break
                except Exception:
                    await asyncio.sleep(2)
            if reachable:
                _set_step(7 + _off, "done", "WebDAV reachable")
                _append_log("WebDAV is reachable on port 8088")
            else:
                _set_step(7 + _off, "error", "WebDAV not reachable")
                _append_log("WARNING: WebDAV not reachable on port 8088 (WebClient/registry may need admin)")
        except Exception as e:
            _set_step(7 + _off, "error", str(e)[:40])
            _append_log(f"WARNING: WebClient config failed (run once as admin): {e}")

        # ── Step: Mount Network Drive ──
        _append_log(f"Cleaning old mapping for {letter}...")
        _unmount_drive(letter)
        await _wait_retry(1)

        path_suffix = "/files/" if mode == "user" else "/root/"
        url = f"http://127.0.0.1:8088{path_suffix}"
        _l = letter.strip(":")
        icon_path = _get_icon_path()
        subprocess.run(["reg", "add", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\DriveIcons",
                        "/v", "ForceNetworkDriveLabel", "/t", "REG_DWORD", "/d", "1", "/f"],
                       capture_output=True, timeout=5)
        for attempt in range(1, 4):
            _set_step(8 + _off, "active", f"try {attempt}/3")
            r = subprocess.run(["net", "use", letter, url, "/persistent:yes"], capture_output=True, text=True, timeout=30)
            if r.returncode == 0:
                r1 = subprocess.run(["reg", "add", f"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\DriveIcons\\{_l}\\DefaultLabel",
                                     "/ve", "/d", label, "/f"], capture_output=True, text=True, timeout=5)
                r2 = subprocess.run(["reg", "add", f"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\DriveIcons\\{_l}\\DefaultIcon",
                                     "/ve", "/d", f"{icon_path},0", "/f"], capture_output=True, text=True, timeout=5)
                _append_log(f"Label reg: exit {r1.returncode} | Icon reg: exit {r2.returncode}")
                _refresh_explorer()
                _set_step(8 + _off, "done", f"{letter} mounted")
                break
            msg = r.stdout.strip() or r.stderr.strip() or f"Error code {r.returncode}"
            _append_log(f"Retry {attempt}/3: {msg}")
            if attempt == 2:
                _append_log("Deleting stale drive mapping...")
                subprocess.run(["net", "use", letter, "/delete", "/y"], capture_output=True, timeout=5)
                await _wait_retry(1)
            if attempt == 3:
                _set_step(8 + _off, "error", msg[:45])
                raise Exception(f"Mount failed: {msg}")

        # ── Save State ──
        letter_no_colon = letter.strip(":")
        _write_adv_state(f"share_{mode}", "1")
        _write_adv_state(f"share_{mode}_letter", letter_no_colon)
        _write_adv_state(f"share_{mode}_prev_letter", letter_no_colon)
        _write_adv_state(f"share_{mode}_label", label)
        _append_log("")
        _append_log("+ Setup complete!")
        status_text.value = "Setup Complete \u2713"
        status_text.color = SUCCESS
        page.update()

    except Exception as ex:
        try:
            _write_adv_state(f"share_{mode}", "0")
        except Exception:
            pass
        _append_log(f"Error: {ex}")
        status_text.value = "Setup Failed"
        status_text.color = ft.Colors.RED_400
        page.update()

    _builtins.print = _fs_orig_print

    if status_text.color == SUCCESS:
        await asyncio.sleep(2)
        await page.window.close()
    else:
        while True:
            await asyncio.sleep(0.3)


# ==============================
# BG SERVICE GUI DIALOG
# ==============================
async def bg_service_gui_app(page: ft.Page):
    page.title = "WSA Installer \u2014 Background Service"
    page.window.width = 520
    page.window.height = 480
    page.window.resizable = False
    page.window.maximizable = False
    page.window.title_bar_hidden = True
    page.window.skip_task_bar = False
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.bgcolor = ft.Colors.TRANSPARENT
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {CONFIG.FONT_NAME_PRIMARY: CONFIG.FONT_URL_PRIMARY, "Consolas": "Consolas"}

    _UNCHECKED = ft.Icons.RADIO_BUTTON_UNCHECKED
    _SPINNER = ft.Icons.SYNC

    step_labels = [
        "WSA Detection",
        "SDK Status",
        "Drive Mount",
        "Config Sync",
        "Update Check",
    ]

    step_data = [{"label": s, "status": "pending", "detail": "\u2014"} for s in step_labels]
    row_icon   = [ft.Icon(_UNCHECKED, size=20, color="#3A3A3C") for _ in step_data]
    row_label  = [ft.Text(d["label"], size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500) for d in step_data]
    row_detail = [ft.Text("\u2014", size=12, color="#3A3A3C") for _ in step_data]
    row_bar    = [ft.ProgressBar(visible=False, color=ACCENT, bgcolor="#3A3A3C", height=3, border_radius=2) for _ in step_data]

    def _build_rows():
        c = []
        for i in range(len(step_data)):
            c.append(ft.Row(spacing=8, controls=[row_icon[i], row_label[i], row_detail[i]], alignment=ft.MainAxisAlignment.START))
            c.append(row_bar[i])
        return c

    def _set_step(idx, status, detail=None):
        step_data[idx]["status"] = status
        if detail is not None:
            step_data[idx]["detail"] = detail
            row_detail[idx].value = detail
        if status == "pending":
            row_icon[idx].name = _UNCHECKED; row_icon[idx].color = "#3A3A3C"
            row_label[idx].color = TEXT_PRIMARY; row_detail[idx].color = "#3A3A3C"; row_bar[idx].visible = False
        elif status == "active":
            row_icon[idx].name = _SPINNER; row_icon[idx].color = ACCENT
            row_label[idx].color = ACCENT; row_detail[idx].color = ACCENT; row_bar[idx].visible = True; row_bar[idx].value = None
        elif status == "done":
            row_icon[idx].name = ft.Icons.CHECK_CIRCLE; row_icon[idx].color = SUCCESS
            row_label[idx].color = TEXT_PRIMARY; row_detail[idx].color = SUCCESS; row_bar[idx].visible = True; row_bar[idx].value = 1.0
        elif status == "error":
            row_icon[idx].name = ft.Icons.CANCEL; row_icon[idx].color = ft.Colors.RED_400
            row_label[idx].color = ft.Colors.RED_400; row_detail[idx].color = ft.Colors.RED_400; row_bar[idx].visible = True; row_bar[idx].value = 0
        page.update()

    step_rows = ft.Column(spacing=2, controls=_build_rows(), horizontal_alignment=ft.CrossAxisAlignment.START)

    log_box = ft.Text("", color="#8E8E93", size=10, font_family="Consolas", selectable=True)
    log_container = ft.Container(
        height=260, padding=10, bgcolor="#111113", border_radius=8,
        border=ft.Border.all(1, "#3A3A3C"),
        content=ft.Column([log_box], scroll=ft.ScrollMode.ADAPTIVE, spacing=0, expand=True),
    )

    def _append_log(msg):
        log_box.value = (log_box.value + "\n" + msg).strip()
        try:
            log_box.update()
        except Exception:
            pass

    _bg_gui_orig_print = _builtins.print
    _bg_gui_log_file = os.path.join(os.environ.get("TEMP", "."), "_wsa_bg_gui_debug.log")

    def _bg_gui_print(*args, **kwargs):
        try:
            _msg = ' '.join(str(a) for a in args)
            with open(_bg_gui_log_file, "a", encoding="utf-8") as _f:
                _f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {_msg}\n")
                _f.flush()
        except Exception:
            pass
        try:
            _append_log(' '.join(str(a) for a in args))
        except Exception:
            _bg_gui_orig_print(*args, **kwargs)

    _builtins.print = _bg_gui_print

    status_text = ft.Text("Background Service Monitor", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)
    version_text = ft.Text("Monitoring WSA, SDK, and system services", size=12, color=TEXT_SECONDARY)

    dialog_card = ft.Container(
        width=520, height=480,
        padding=ft.Padding(20, 6, 20, 6),
        border_radius=18, bgcolor=BG_DARK,
        border=ft.Border.all(1, BORDER),
        content=ft.Column(
            spacing=0,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Row([ft.Icon(ft.Icons.MONITOR_HEART, color=ACCENT, size=22), status_text],
                       alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                version_text,
                ft.Divider(height=3, color="#3A3A3C"),
                ft.Container(
                    margin=ft.margin.only(bottom=8),
                    border=ft.Border.all(1, BORDER),
                    border_radius=14, padding=12, bgcolor=BG_CARD,
                    content=step_rows,
                ),
                log_container,
            ],
        ),
    )

    page.add(ft.Container(
        expand=True, alignment=ft.Alignment(0, 0), bgcolor=ft.Colors.TRANSPARENT,
        content=ft.WindowDragArea(content=dialog_card),
    ))
    page.update()
    await page.window.center()
    page.window.visible = True
    page.update()

    def _parse_log_line(line):
        line_lower = line.lower()
        if "wsa" in line_lower and ("start" in line_lower or "stop" in line_lower or "detect" in line_lower):
            if "already running" in line_lower or "started" in line_lower or "detected" in line_lower:
                _set_step(0, "done", "Running")
            elif "stop" in line_lower or "not running" in line_lower or "waiting" in line_lower:
                _set_step(0, "pending", "Waiting")
            elif "error" in line_lower or "fail" in line_lower:
                _set_step(0, "error", "Error")
        if "sdk" in line_lower:
            if "start" in line_lower:
                _set_step(1, "done", "Active")
            elif "stop" in line_lower or "crash" in line_lower:
                _set_step(1, "error", "Stopped")
            elif "already" in line_lower or "running" in line_lower:
                _set_step(1, "done", "Running")
        if "mount" in line_lower or "drive" in line_lower or "unmount" in line_lower:
            if "mount" in line_lower and ("fail" not in line_lower and "error" not in line_lower):
                _set_step(2, "done", "Mounted")
            elif "unmount" in line_lower:
                _set_step(2, "pending", "Unmounted")
            elif "fail" in line_lower or "error" in line_lower:
                _set_step(2, "error", "Failed")
        if "update" in line_lower:
            if "check" in line_lower or "available" in line_lower:
                _set_step(4, "done", "Checked")
            elif "fail" in line_lower or "error" in line_lower:
                _set_step(4, "error", "Failed")
        if "config" in line_lower or "remote" in line_lower:
            if "received" in line_lower or "sync" in line_lower:
                _set_step(3, "done", "Synced")
            elif "fail" in line_lower or "error" in line_lower:
                _set_step(3, "error", "Failed")

    print("Starting background service...")

    try:
        _cmd = _script_args("--bg-service")
        _proc = subprocess.Popen(
            _cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            creationflags=0x08000000,
        )
        print(f"Service started (PID: {_proc.pid})")

        import queue as _queue
        _log_queue = _queue.Queue()

        def _read_output():
            try:
                for line in iter(_proc.stdout.readline, ""):
                    if line:
                        _log_queue.put(line.rstrip())
            except Exception:
                pass

        _read_thread = threading.Thread(target=_read_output, daemon=True)
        _read_thread.start()

        async def _poll_logs():
            while True:
                try:
                    while True:
                        line = _log_queue.get_nowait()
                        _append_log(line)
                        _parse_log_line(line)
                except _queue.Empty:
                    pass
                if _proc.poll() is not None:
                    print(f"Service process exited (code: {_proc.returncode})")
                    break
                await asyncio.sleep(0.3)

        await _poll_logs()
    except Exception as ex:
        print(f"Error: {ex}")

# ==============================
# UPDATE DIALOG (module-level)
# ==============================
async def update_app(page: ft.Page):
    _update_url = sys.argv[2] if len(sys.argv) > 2 else _UPDATE_EXE_URL
    _new_version = sys.argv[3] if len(sys.argv) > 3 else "?"
    _local_ver = _extract_version(APP_ID)

    page.title = "WSA Installer \u2014 Update"
    page.window.width = 520
    page.window.height = 390
    page.window.resizable = False
    page.window.maximizable = False
    page.window.title_bar_hidden = False
    page.window.skip_task_bar = False
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.bgcolor = ft.Colors.TRANSPARENT
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {
        CONFIG.FONT_NAME_PRIMARY: CONFIG.FONT_URL_PRIMARY,
        "Consolas": "Consolas"
    }

    _CARD_W = 480
    _UNCHECKED = ft.Icons.RADIO_BUTTON_UNCHECKED
    _SPINNER   = ft.Icons.SYNC

    step_data = [
        {"label": "Check Local App Version",  "status": "pending", "detail": "\u2014"},
        {"label": "Check GitHub Update",       "status": "pending", "detail": "\u2014"},
        {"label": "Downloading Update",        "status": "pending", "detail": "\u2014"},
        {"label": "Verifying Download",        "status": "pending", "detail": "\u2014"},
        {"label": "Installing Update",         "status": "pending", "detail": "\u2014"},
        {"label": "Restarting App",            "status": "pending", "detail": "\u2014"},
    ]

    row_icon   = [ft.Icon(_UNCHECKED, size=22, color="#3A3A3C") for _ in step_data]
    row_label  = [ft.Text(d["label"], size=14, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500) for d in step_data]
    row_detail = [ft.Text("\u2014", size=13, color="#3A3A3C") for _ in step_data]
    row_bar    = [ft.ProgressBar(visible=False, color=ACCENT, bgcolor="#3A3A3C", height=3, border_radius=2) for _ in step_data]

    # Only first 2 steps visible initially
    for i in range(2, 6):
        row_icon[i].visible = False
        row_label[i].visible = False
        row_detail[i].visible = False
        row_bar[i].visible = False

    def _show_all_steps():
        for i in range(2, 6):
            row_icon[i].visible = True
            row_label[i].visible = True
            row_detail[i].visible = True
            row_bar[i].visible = False
        page.update()

    def _build_rows():
        controls = []
        for i in range(len(step_data)):
            controls.append(ft.Row(spacing=10, controls=[row_icon[i], row_label[i], row_detail[i]], alignment=ft.MainAxisAlignment.START))
            controls.append(row_bar[i])
        return controls

    step_rows = ft.Column(spacing=2, controls=_build_rows(), horizontal_alignment=ft.CrossAxisAlignment.START)

    def _set_step(idx, status, detail=None):
        step_data[idx]["status"] = status
        if detail is not None:
            step_data[idx]["detail"] = detail
            row_detail[idx].value = detail
        if status == "pending":
            row_icon[idx].name  = _UNCHECKED
            row_icon[idx].color = "#3A3A3C"
            row_label[idx].color = TEXT_PRIMARY
            row_detail[idx].color = "#3A3A3C"
            row_bar[idx].visible = False
        elif status == "active":
            row_icon[idx].name  = _SPINNER
            row_icon[idx].color = ACCENT
            row_label[idx].color = ACCENT
            row_detail[idx].color = ACCENT
            row_bar[idx].visible = True
            row_bar[idx].value = None
        elif status == "done":
            row_icon[idx].name  = ft.Icons.CHECK_CIRCLE
            row_icon[idx].color = SUCCESS
            row_label[idx].color = TEXT_PRIMARY
            row_detail[idx].color = SUCCESS
            row_bar[idx].visible = True
            row_bar[idx].value = 1.0
        elif status == "error":
            row_icon[idx].name  = ft.Icons.CANCEL
            row_icon[idx].color = ft.Colors.RED_400
            row_label[idx].color = ft.Colors.RED_400
            row_detail[idx].color = ft.Colors.RED_400
            row_bar[idx].visible = True
            row_bar[idx].value = 0
        page.update()

    def _set_bar(idx, value):
        row_bar[idx].value = value
        page.update()

    status_text = ft.Text("Update Available", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)
    version_text = ft.Text(f"Version {_local_ver} \u2192 Version {_new_version}", size=12, color=TEXT_SECONDARY)
    log_box = ft.Text("", color="#8E8E93", size=10, font_family="Consolas", selectable=True)
    log_container = ft.Container(
        width=_CARD_W, height=80, padding=13,
        bgcolor="#111113", border_radius=8,
        border=ft.Border.all(1, "#3A3A3C"),
        content=ft.Column([log_box], scroll=ft.ScrollMode.ADAPTIVE, spacing=0, expand=True),
    )

    def _append_log(msg):
        log_box.value = (log_box.value + "\n" + msg).strip()
        log_box.update()

    _upd_orig_print = _builtins.print
    _upd_log_file = os.path.join(os.environ.get("TEMP", "."), "_wsa_upd_debug.log")

    def _upd_print(*args, **kwargs):
        try:
            _msg = ' '.join(str(a) for a in args)
            with open(_upd_log_file, "a", encoding="utf-8") as _f:
                _f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {_msg}\n")
                _f.flush()
        except Exception:
            pass
        try:
            _append_log(' '.join(str(a) for a in args))
        except Exception:
            _upd_orig_print(*args, **kwargs)

    _builtins.print = _upd_print

    dialog_card = ft.Container(
        width=520, height=340,
        padding=ft.Padding(20, 6, 20, 6),
        border_radius=18, bgcolor=BG_DARK,
        border=ft.Border.all(1, BORDER),
        content=ft.Column(
            spacing=0,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Row([ft.Icon(ft.Icons.SYSTEM_UPDATE_ALT, color=ACCENT, size=22), status_text],
                       alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                version_text,
                ft.Divider(height=3, color="#3A3A3C"),
                ft.Container(
                    expand=True,
                    border=ft.Border.all(1, BORDER),
                    border_radius=14, padding=12, bgcolor=BG_CARD,
                    content=step_rows,
                ),
                ft.Container(height=6),
                log_container,
            ],
        ),
    )

    page.add(ft.Container(
        expand=True, alignment=ft.Alignment(0, 0), bgcolor=ft.Colors.TRANSPARENT,
        content=ft.WindowDragArea(content=dialog_card),
    ))
    page.update()
    await page.window.center()
    page.window.visible = True
    page.update()

    import time as _time

    def _execute_installer(exe_path):
        _append_log("Launching installer (silent mode)...")
        _set_step(4, "active", "launching...")
        page.update()
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                   r"Software\Microsoft\Windows\CurrentVersion\Uninstall\WSAInstaller")
            winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, _new_version)
            winreg.CloseKey(key)
            _append_log(f"Registry DisplayVersion updated to {_new_version}")
        except Exception as e:
            _append_log(f"Warning: could not update registry version: {e}")
        subprocess.Popen([exe_path, "/S"], creationflags=0x08000000)
        _set_step(4, "done", "launched")
        _append_log("Installer launched successfully")

    try:
        _set_step(0, "active", f"Version {_local_ver}")
        await asyncio.sleep(0.4)
        _set_step(0, "done", f"Version {_local_ver}")
        _append_log(f"Local version: Version {_local_ver}")

        _set_step(1, "active", "checking...")
        await asyncio.sleep(0.3)

        _remote_app_id = _new_version
        _remote_ver = _new_version
        _append_log(f"Remote version: {'Unknown' if _remote_ver == '?' else 'Version ' + _remote_ver}")

        if not _remote_ver or _remote_ver == "?" or _remote_ver == _local_ver:
            _set_step(1, "done", "already updated")
            _append_log("Already up to date. No update needed.")
            version_text.value = f"Version {_local_ver}"
            status_text.value = "Up to Date"
            status_text.color = SUCCESS
            page.update()
            await asyncio.sleep(2)
            await page.window.close()
            return

        version_text.value = f"Version {_local_ver} \u2192 Version {_remote_ver}"
        _set_step(1, "done", f"Version {_remote_ver} found")
        _append_log(f"Update available: Version {_local_ver} \u2192 Version {_remote_ver}")
        page.update()

        _show_all_steps()

        _set_step(2, "active", "connecting...")
        _append_log(f"URL: {_update_url[:80]}")
        page.update()

        row_bar[2].visible = True
        row_bar[2].value = 0
        page.update()

        import shutil
        import requests as _requests
        from concurrent.futures import ThreadPoolExecutor

        _out_asset_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out_asset")
        os.makedirs(_out_asset_dir, exist_ok=True)
        _exe_path = os.path.join(_out_asset_dir, "WSA_Installer_Setup.exe")

        _existing_part_bytes = 0
        try:
            for _f in os.listdir(_out_asset_dir):
                if _f.startswith("WSA_Installer_Setup.exe.part"):
                    _existing_part_bytes += os.path.getsize(os.path.join(_out_asset_dir, _f))
        except Exception:
            pass

        _NUM_CHUNKS = getattr(CONFIG, "NUM_CHUNKS", 30)

        _dl_state = {"done": False, "error": None, "progress": 0, "speed": "", "eta": "", "detail": "", "log": "", "total_mb": 0, "merge_pct": 0, "merging": False}

        def _chunked_download(url, dest_path):
            try:
                _r_head = _requests.head(url, allow_redirects=True)
                remote_size = int(_r_head.headers.get("content-length", 0))
                if remote_size == 0:
                    _dl_state["error"] = "Failed to get remote file size"
                    _dl_state["done"] = True
                    return

                if os.path.exists(dest_path) and os.path.getsize(dest_path) == remote_size:
                    _existing_ver = _get_exe_version(dest_path)
                    if _existing_ver and _new_version != "?" and _existing_ver >= _new_version:
                        _dl_state["total_mb"] = remote_size / (1024 * 1024)
                        _dl_state["progress"] = 1.0
                        _dl_state["speed"] = "Complete"
                        _dl_state["eta"] = ""
                        _dl_state["detail"] = f"{remote_size / (1024*1024):.1f} MB  |  Already present (v{_existing_ver})"
                        _dl_state["log"] = f"File already present: v{_existing_ver} matches target v{_new_version}"
                        _dl_state["done"] = True
                        return
                    else:
                        _dl_state["log"] = f"Old version detected (v{_existing_ver}), re-downloading v{_new_version}..."
                        try:
                            os.remove(dest_path)
                        except Exception:
                            pass
                        try:
                            for _f in os.listdir(_out_asset_dir):
                                if _f.startswith("WSA_Installer_Setup.exe.part"):
                                    os.remove(os.path.join(_out_asset_dir, _f))
                        except Exception:
                            pass

                _dl_state["log"] = f"File size: {remote_size / (1024*1024):.1f} MB  |  {_NUM_CHUNKS} chunks"

                chunk_size = remote_size // _NUM_CHUNKS
                ranges = []
                for i in range(_NUM_CHUNKS):
                    start = i * chunk_size
                    end = (i + 1) * chunk_size - 1 if i < _NUM_CHUNKS - 1 else remote_size - 1
                    ranges.append((start, end, i))

                def _dl_chunk(start, end, idx):
                    _cf = f"{dest_path}.part{idx}"
                    _cur = os.path.getsize(_cf) if os.path.exists(_cf) else 0
                    _expected = (end - start) + 1
                    if _cur >= _expected:
                        return _cf
                    _actual_start = start + _cur
                    _headers = {"Range": f"bytes={_actual_start}-{end}"}
                    with _requests.get(url, stream=True, headers=_headers) as _r:
                        _r.raise_for_status()
                        _mode = "ab" if _cur > 0 else "wb"
                        with open(_cf, _mode) as _f:
                            for _data in _r.iter_content(chunk_size=1024 * 1024):
                                if _data:
                                    _f.write(_data)
                    return _cf

                _start_t = _time.time()
                _executor = ThreadPoolExecutor(max_workers=_NUM_CHUNKS)
                try:
                    _futures = [_executor.submit(_dl_chunk, r[0], r[1], r[2]) for r in ranges]

                    while not all(f.done() for f in _futures):
                        _total_dl = 0
                        for i in range(_NUM_CHUNKS):
                            _pf = f"{dest_path}.part{i}"
                            if os.path.exists(_pf):
                                _total_dl += os.path.getsize(_pf)
                        _elapsed = max(_time.time() - _start_t, 0.001)
                        _speed = _total_dl / _elapsed
                        _pct_val = _total_dl / remote_size if remote_size else 0
                        _pct_int = int(_pct_val * 100)
                        _dl_done_mb = _total_dl / (1024 * 1024)
                        _dl_total_mb = remote_size / (1024 * 1024)
                        if _speed > 1024 * 1024:
                            _spd_str = f"{_speed / (1024*1024):.1f} MB/s"
                        elif _speed > 1024:
                            _spd_str = f"{_speed / 1024:.1f} KB/s"
                        else:
                            _spd_str = f"{_speed:.0f} B/s"
                        _remaining = remote_size - _total_dl
                        if _speed > 0:
                            _eta_s = _remaining / _speed
                            if _eta_s >= 3600:
                                _eta_str = f"{int(_eta_s//3600)}h {int((_eta_s%3600)//60)}m"
                            elif _eta_s >= 60:
                                _eta_str = f"{int(_eta_s//60)}m {int(_eta_s%60)}s"
                            else:
                                _eta_str = f"{int(_eta_s)}s"
                        else:
                            _eta_str = "--"

                        _dl_state["progress"] = _pct_val
                        _dl_state["speed"] = _spd_str
                        _dl_state["eta"] = _eta_str
                        _dl_state["detail"] = f"{_dl_done_mb:.1f} / {_dl_total_mb:.1f} MB  |  {_pct_int}%  |  {_spd_str}  ETA {_eta_str}"
                        _time.sleep(0.3)
                finally:
                    _executor.shutdown(wait=False)

                _dl_state["merging"] = True
                _dl_state["log"] = f"Download done. Merging {_NUM_CHUNKS} chunks..."

                with open(dest_path, "wb") as _out:
                    for i in range(_NUM_CHUNKS):
                        _pf = f"{dest_path}.part{i}"
                        if os.path.exists(_pf):
                            with open(_pf, "rb") as _in:
                                shutil.copyfileobj(_in, _out)
                            os.remove(_pf)
                        _dl_state["merge_pct"] = (i + 1) / _NUM_CHUNKS
                        _dl_state["detail"] = f"Merging... {int((i+1)/_NUM_CHUNKS*100)}%"
                        _time.sleep(0.05)

                _dl_state["progress"] = 1.0
                _dl_state["speed"] = "Complete"
                _dl_state["eta"] = ""
                _dl_state["total_mb"] = remote_size / (1024 * 1024)
                _dl_state["detail"] = f"{remote_size / (1024*1024):.1f} MB  |  100%  |  Complete"
                _dl_state["done"] = True
            except Exception as _dl_err:
                _dl_state["error"] = str(_dl_err)
                _dl_state["done"] = True

        _dl_thread = threading.Thread(target=_chunked_download, args=(_update_url, _exe_path), daemon=True)
        _dl_thread.start()

        if _existing_part_bytes > 0:
            _append_log(f"Resuming from {_existing_part_bytes / (1024*1024):.1f} MB partial download...")
            page.update()

        while not _dl_state["done"]:
            if _dl_state["log"]:
                _append_log(_dl_state["log"])
                _dl_state["log"] = ""
            row_bar[2].value = _dl_state["progress"]
            row_detail[2].value = _dl_state["detail"]
            row_bar[2].update()
            row_detail[2].update()
            await asyncio.sleep(0.3)

        if _dl_state["error"]:
            raise Exception(_dl_state["error"])

        if _dl_state["log"]:
            _append_log(_dl_state["log"])

        _total_mb = _dl_state["total_mb"]
        row_bar[2].value = 1.0
        row_detail[2].value = _dl_state["detail"]
        row_detail[2].update()
        _set_step(2, "done", f"{_total_mb:.1f} MB")
        _append_log(f"Download complete ({_total_mb:.1f} MB) -> {_exe_path}")
        page.update()

        _set_step(3, "active", "checking integrity...")
        _append_log("Verifying download integrity...")
        page.update()
        await asyncio.sleep(0.3)

        _is_valid = True
        _reason = ""
        _file_size = os.path.getsize(_exe_path) if os.path.exists(_exe_path) else 0
        with open(_exe_path, "rb") as _f:
            _header = _f.read(2)
        if _file_size < 1024:
            _is_valid = False
            _reason = "File too small"
        elif _header != b"MZ":
            _is_valid = False
            _reason = "Invalid executable"
        else:
            _append_log("MZ header OK")
            _append_log(f"File size OK ({_file_size / (1024*1024):.1f} MB)")

        if _is_valid:
            _exe_ver = _get_exe_version(_exe_path)
            if _exe_ver and _new_version and _new_version != "?" and _exe_ver != _new_version:
                _is_valid = False
                _reason = f"Version mismatch: file is v{_exe_ver}, expected v{_new_version}"
            elif _exe_ver:
                _append_log(f"Version check OK: v{_exe_ver}")
                _set_step(3, "done", "valid")
                _append_log("Download verified successfully")
            else:
                _append_log("Version check skipped (PE header not readable)")
                _set_step(3, "done", "valid")
                _append_log("Download verified successfully")

        if _is_valid:
            pass
        else:
            raise Exception(f"Integrity check failed: {_reason}")

        _set_step(4, "active", "extracting...")
        _append_log("Preparing silent install...")
        _append_log(f"Saved: {_exe_path}")
        _set_bar(4, 0.5)
        page.update()

        _execute_installer(_exe_path)

        _set_step(5, "active", "exiting...")
        status_text.value = "Restarting..."
        status_text.color = ACCENT
        _append_log("App will restart now.")
        page.update()
        await asyncio.sleep(1.5)
        await page.window.close()

    except Exception as ex:
        _append_log(f"Error: {ex}")
        for i in range(len(step_data)):
            if step_data[i]["status"] == "active":
                _set_step(i, "error", str(ex)[:40])
                break
        status_text.value = "Update Failed"
        status_text.color = ft.Colors.RED_400
        page.update()

    _builtins.print = _upd_orig_print

def _extract_version(app_id):
    import re
    m = re.search(r"(\d+(?:\.\d+)*)$", app_id)
    return m.group(1) if m else ""


def _get_exe_version(exe_path):
    """Extract 'major.minor' version from PE file_version_info using win32api."""
    try:
        import win32api
        info = win32api.GetFileVersionInfo(exe_path, "\\")
        ms = info["FileVersionMS"]
        ls = info["FileVersionLS"]
        major = win32api.HIWORD(ms)
        minor = win32api.LOWORD(ms)
        return f"{major}.{minor}"
    except Exception:
        return None


def _get_installed_version_from_registry():
    """Read DisplayVersion from HKLM\\...\\Uninstall\\WSAInstaller (Windows Settings registry)."""
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"Software\Microsoft\Windows\CurrentVersion\Uninstall\WSAInstaller",
            access=winreg.KEY_READ | 0x0100
        )
        version, _ = winreg.QueryValueEx(key, "DisplayVersion")
        winreg.CloseKey(key)
        return str(version) if version else None
    except Exception:
        return None

# ==============================
# REPAIR WSA DIALOG (module-level)
# ==============================
async def repair_app(page: ft.Page):
    """4-step WSA repair dialog: detect → stop → backup → uninstall+reinstall."""
    page.title = "WSA Installer — Repair WSA"
    page.window.width = 520
    page.window.height = 440
    page.window.resizable = False
    page.window.maximizable = False
    page.window.title_bar_hidden = True
    page.window.skip_task_bar = False
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.bgcolor = ft.Colors.TRANSPARENT
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {CONFIG.FONT_NAME_PRIMARY: CONFIG.FONT_URL_PRIMARY, "Consolas": "Consolas"}


    _CARD_W = 480
    _UNCHECKED = ft.Icons.RADIO_BUTTON_UNCHECKED
    _SPINNER = ft.Icons.SYNC

    step_data = [
        {"label": "WSA Detection",         "status": "pending", "detail": "\u2014"},
        {"label": "Stop WSA Processes",     "status": "pending", "detail": "\u2014"},
        {"label": "Backup User Data",       "status": "pending", "detail": "\u2014"},
        {"label": "Uninstall & Reinstall",  "status": "pending", "detail": "\u2014"},
    ]

    row_icon   = [ft.Icon(_UNCHECKED, size=22, color="#3A3A3C") for _ in step_data]
    row_label  = [ft.Text(d["label"], size=14, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500) for d in step_data]
    row_detail = [ft.Text("\u2014", size=13, color="#3A3A3C") for _ in step_data]
    row_bar    = [ft.ProgressBar(visible=False, color=ACCENT, bgcolor="#3A3A3C", height=3, border_radius=2) for _ in step_data]

    def _build_rows():
        c = []
        for i in range(len(step_data)):
            c.append(ft.Row(spacing=10, controls=[row_icon[i], row_label[i], row_detail[i]], alignment=ft.MainAxisAlignment.START))
            c.append(row_bar[i])
        return c

    step_rows = ft.Column(spacing=2, controls=_build_rows(), horizontal_alignment=ft.CrossAxisAlignment.START)

    def _set_step(idx, status, detail=None):
        step_data[idx]["status"] = status
        if detail is not None:
            step_data[idx]["detail"] = detail
            row_detail[idx].value = detail
        if status == "pending":
            row_icon[idx].name = _UNCHECKED; row_icon[idx].color = "#3A3A3C"
            row_label[idx].color = TEXT_PRIMARY; row_detail[idx].color = "#3A3A3C"; row_bar[idx].visible = False
        elif status == "active":
            row_icon[idx].name = _SPINNER; row_icon[idx].color = ACCENT
            row_label[idx].color = ACCENT; row_detail[idx].color = ACCENT; row_bar[idx].visible = True; row_bar[idx].value = None
        elif status == "done":
            row_icon[idx].name = ft.Icons.CHECK_CIRCLE; row_icon[idx].color = SUCCESS
            row_label[idx].color = TEXT_PRIMARY; row_detail[idx].color = SUCCESS; row_bar[idx].visible = True; row_bar[idx].value = 1.0
        elif status == "error":
            row_icon[idx].name = ft.Icons.CANCEL; row_icon[idx].color = ft.Colors.RED_400
            row_label[idx].color = ft.Colors.RED_400; row_detail[idx].color = ft.Colors.RED_400; row_bar[idx].visible = True; row_bar[idx].value = 0
        page.update()

    log_box = ft.Text("", color="#8E8E93", size=10, font_family="Consolas", selectable=True)
    log_container = ft.Container(
        width=_CARD_W, height=80, padding=13,
        bgcolor="#111113", border_radius=8,
        border=ft.Border.all(1, "#3A3A3C"),
        content=ft.Column([log_box], scroll=ft.ScrollMode.ADAPTIVE, spacing=0, expand=True),
    )

    def _append_log(msg):
        log_box.value = (log_box.value + "\n" + msg).strip()
        log_box.update()

    _rp_orig_print = _builtins.print
    _rp_log_file = os.path.join(os.environ.get("TEMP", "."), "_wsa_repair_debug.log")

    def _rp_print(*args, **kwargs):
        try:
            _msg = ' '.join(str(a) for a in args)
            with open(_rp_log_file, "a", encoding="utf-8") as _f:
                _f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {_msg}\n")
                _f.flush()
        except Exception:
            pass
        try:
            _append_log(' '.join(str(a) for a in args))
        except Exception:
            _rp_orig_print(*args, **kwargs)

    _builtins.print = _rp_print

    status_text = ft.Text("WSA Repair", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)
    version_text = ft.Text("Backup data \u2192 Uninstall \u2192 Reinstall WSA", size=12, color=TEXT_SECONDARY)

    dialog_card = ft.Container(
        width=520, height=400,
        padding=ft.Padding(20, 6, 20, 6),
        border_radius=18, bgcolor=BG_DARK,
        border=ft.Border.all(1, BORDER),
        content=ft.Column(
            spacing=0, expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Row([ft.Icon(ft.Icons.REFRESH_ROUNDED, color=ACCENT, size=22), status_text],
                       alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                version_text,
                ft.Divider(height=3, color="#3A3A3C"),
                ft.Container(
                    expand=True,
                    border=ft.Border.all(1, BORDER),
                    border_radius=14, padding=12, bgcolor=BG_CARD,
                    content=step_rows,
                ),
                ft.Container(height=6),
                log_container,
            ],
        ),
    )

    page.add(ft.Container(
        expand=True, alignment=ft.Alignment(0, 0), bgcolor=ft.Colors.TRANSPARENT,
        content=ft.WindowDragArea(content=dialog_card),
    ))
    page.update()
    await page.window.center()
    page.window.visible = True
    page.update()

    async def run_repair():
        # ── Step 0: Detect WSA ─────────────────────────────────────────
        _set_step(0, "active", "checking...")
        _append_log("Detecting WSA installation...")

        def _detect_wsa():
            try:
                r = subprocess.run(
                    ["powershell", "-NoProfile", "-Command",
                     "Get-AppxPackage -Name 'MicrosoftCorporationII.WindowsSubsystemForAndroid' | Select-Object -ExpandProperty InstallLocation"],
                    capture_output=True, text=True, timeout=15,
                    creationflags=0x08000000)
                loc = (r.stdout or "").strip()
                return loc if loc else None
            except Exception:
                return None

        wsa_location = await asyncio.to_thread(_detect_wsa)
        if not wsa_location:
            _set_step(0, "error", "not installed")
            _append_log("WSA is not installed. Nothing to repair.")
            await asyncio.sleep(2)
            page.window.close()
            sys.exit(0)
        _set_step(0, "done", wsa_location[:50])
        _append_log(f"WSA found at: {wsa_location}")
        await asyncio.sleep(0.3)

        # ── Step 1: Stop WSA Processes ─────────────────────────────────
        _set_step(1, "active", "stopping...")
        _append_log("Stopping WSA processes...")

        def _stop_wsa():
            for proc_name in ["WsaClient.exe", "WsaSvc.exe", "vmmem", "WsaService.exe", "adb.exe"]:
                try:
                    subprocess.run(["taskkill", "/F", "/T", "/IM", proc_name],
                                   capture_output=True, timeout=10, creationflags=0x08000000)
                except Exception:
                    pass
            try:
                subprocess.run(
                    ["powershell", "-NoProfile", "-Command",
                     "Get-Process -Name 'WsaService','WsaSvc' -ErrorAction SilentlyContinue | Stop-Process -Force"],
                    capture_output=True, timeout=10, creationflags=0x08000000)
            except Exception:
                pass
            time.sleep(1)

        await asyncio.to_thread(_stop_wsa)
        _set_step(1, "done", "stopped")
        _append_log("WSA processes stopped.")
        await asyncio.sleep(0.5)

        # ── Step 2: Backup User Data ───────────────────────────────────
        _set_step(2, "active", "checking...")
        _append_log("Checking backup status...")

        src = _wsa_data_path()
        dst = _wsa_backup_path()

        if _is_backup_valid():
            _set_step(2, "done", "already exists")
            _append_log("Valid backup found, skipping.")
        elif not os.path.isdir(src):
            _set_step(2, "done", "no data folder")
            _append_log("No WSA data folder found, skipping backup.")
        else:
            _set_step(2, "active", "backing up...")
            _append_log("Backing up WSA data...")
            try:
                os.makedirs(dst, exist_ok=True)
                total_size = 0
                file_count = 0
                for dp, dns, fns in os.walk(src):
                    for fn in fns:
                        total_size += os.path.getsize(os.path.join(dp, fn))
                        file_count += 1
                copied = 0
                start_t = time.time()
                for dp, dns, fns in os.walk(src):
                    rel = os.path.relpath(dp, src)
                    dest_dir = os.path.join(dst, rel) if rel else dst
                    os.makedirs(dest_dir, exist_ok=True)
                    for fn in fns:
                        sfp = os.path.join(dp, fn)
                        dfp = os.path.join(dest_dir, fn)
                        shutil.copy2(sfp, dfp)
                        copied += os.path.getsize(sfp)
                        if file_count > 10:
                            pct = copied / max(total_size, 1)
                            spd = copied / max(time.time() - start_t, 0.001)
                            eta = (total_size - copied) / max(spd, 1)
                            _set_step(2, "active", f"{pct:.0%} | {spd/1024/1024:.1f} MB/s | ETA {eta:.0f}s")
                _set_step(2, "done", f"{file_count} files")
                _append_log(f"Backup complete ({file_count} files).")
            except Exception as ex:
                _set_step(2, "error", "failed")
                _append_log(f"Backup error: {ex}")

        await asyncio.sleep(0.3)

        # ── Step 3: Uninstall & Reinstall ──────────────────────────────
        _set_step(3, "active", "launching uninstaller...")
        _append_log("Launching uninstaller...")

        try:
            if getattr(sys, 'frozen', False):
                uninstall_proc = await self._create_subprocess(
                    sys.executable, "--uninstall", creationflags=0x08000000)
            else:
                uninstall_proc = await self._create_subprocess(
                    sys.executable, os.path.abspath(__file__), "--uninstall", creationflags=0x08000000)
            _append_log("Waiting for uninstall to complete...")
            await uninstall_proc.wait()
            _append_log("Uninstall complete.")
        except Exception as ex:
            _append_log(f"Uninstall error: {ex}")

        await asyncio.sleep(1)
        _set_step(3, "active", "launching installer...")
        _append_log("Checking for running instance...")

        global _instance_lock
        if check_instance_lock():
            _instance_lock.close()
            _instance_lock = None
            _append_log("No running instance found, launching WSA Installer...")
            try:
                if getattr(sys, 'frozen', False):
                    subprocess.Popen([sys.executable], creationflags=0x08000000)
                else:
                    subprocess.Popen([sys.executable, os.path.abspath(__file__)], creationflags=0x08000000)
            except Exception as ex:
                _append_log(f"Could not launch installer: {ex}")
        else:
            _append_log("Main installer already running, skipping re-launch")

        _set_step(3, "done", "done")
        dialog_card.border = ft.Border.all(2, SUCCESS)
        page.update()
        await asyncio.sleep(3)
        page.window.close()
        sys.exit(0)

    page.run_task(run_repair)



# ==============================
# ALREADY RUNNING DIALOG (module-level)
# ==============================
async def running_app(page: ft.Page):
    page.title = getattr(CONFIG, "ALREADY_RUNNING_TITLE", "App Already Running")
    page.window.width = 420
    page.window.height = 240
    page.window.resizable = False
    page.window.maximizable = False
    page.window.title_bar_hidden = True
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.bgcolor = ft.Colors.TRANSPARENT
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def on_close_click(e):
        sys.exit(1)

    dialog_card = ft.Container(
        width=420, height=240,
        bgcolor=BG_DARK,
        border_radius=18,
        border=ft.Border.all(1, BORDER),
        padding=24,
        content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, color=ACCENT, size=24), ft.Text(getattr(CONFIG, "ALREADY_RUNNING_TITLE", "App Already Running"), size=18, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=20, color="#3A3A3C"),
            ft.Text(
                getattr(CONFIG, "ALREADY_RUNNING_DESC", "Another instance of WSA Installer is already open. Please close it before launching a new one."),
                text_align=ft.TextAlign.CENTER, color=TEXT_SECONDARY, size=13
            ),
            ft.Container(expand=True),
            ft.Row([
                ft.FilledButton(
                    getattr(CONFIG, "ADMIN_BTN_CANCEL", "Close"), 
                    on_click=on_close_click,
                    bgcolor=ACCENT,
                    color=ft.Colors.WHITE,
                    width=120,
                    height=40,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                )
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    page.add(
        ft.Container(
            expand=True,
            alignment=ft.Alignment(0, 0),
            bgcolor=ft.Colors.TRANSPARENT,
            content=ft.WindowDragArea(content=dialog_card)
        )
    )
    page.update()
    await page.window.center()
    page.window.visible = True
    page.update()


if __name__ == "__main__":
    # Ad Process Handler (Used to launch ad in its own main thread/process)
    if "--ad" in sys.argv:
        try:
            # Extract URL and seconds from arguments
            idx = sys.argv.index("--ad")
            ad_url = sys.argv[idx + 1]
            ad_secs = int(sys.argv[idx + 2])
            
            print(f"[AD_PROCESS] Launching URL: {ad_url}")
            
            app = QApplication(sys.argv)
            window = AdWebEngineWindow(ad_url, ad_secs)
            window.show()
            sys.exit(app.exec())
        except Exception as e:
            print(f"Ad Process Error: {e}")
            sys.exit(1)

def _ensure_windows_service():
    try:
        _bin = subprocess.list2cmdline(_script_args("--bg-service"))
        r = subprocess.run(["sc", "query", _SERVICE_NAME], capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW, timeout=5)
        if r.returncode == 0:
            subprocess.run(["sc", "config", _SERVICE_NAME, "binPath=", _bin, "start=", "auto"],
                           creationflags=subprocess.CREATE_NO_WINDOW, timeout=10)
        else:
            subprocess.run(["sc", "create", _SERVICE_NAME, "binPath=", _bin, "start=", "auto"],
                           creationflags=subprocess.CREATE_NO_WINDOW, timeout=10)
            print(f"[SERVICE] Windows service '{_SERVICE_DISPLAY}' installed.")
        subprocess.run(["sc", "failure", _SERVICE_NAME, "reset=86400", "actions=restart/10000/restart/15000/restart/30000"],
                       creationflags=subprocess.CREATE_NO_WINDOW, timeout=10)
        subprocess.run(["sc", "description", _SERVICE_NAME, _SERVICE_DESC],
                       creationflags=subprocess.CREATE_NO_WINDOW, timeout=10)
    except Exception:
        pass

def _remove_windows_service():
    try:
        subprocess.run(["sc", "stop", _SERVICE_NAME], capture_output=True,
                       creationflags=subprocess.CREATE_NO_WINDOW, timeout=5)
    except Exception:
        pass
    try:
        subprocess.run(["sc", "delete", _SERVICE_NAME],
                       creationflags=subprocess.CREATE_NO_WINDOW, timeout=5)
        print(f"[SERVICE] Windows service '{_SERVICE_DISPLAY}' removed.")
    except Exception:
        pass

def start():
    # Look for patched Flet client in all locations (dev + frozen)
    _flet_candidates = []
    # 1. Frozen build: next to executable
    if getattr(sys, 'frozen', False):
        _flet_candidates.append(
            os.path.join(os.path.dirname(sys.executable), "_internal", "flet_desktop", "app", "flet")
        )
    # 2. Dev mode: check dist/ from a previous build
    _flet_candidates.append(
        os.path.join(os.getcwd(), "dist", "WSA Installer", "_internal", "flet_desktop", "app", "flet")
    )
    # 3. FLET_VIEW_PATH if already set externally
    _existing = os.environ.get("FLET_VIEW_PATH", "")
    if _existing:
        _flet_candidates.append(_existing)
    for _path in _flet_candidates:
        if _path and os.path.isdir(_path) and os.path.isfile(os.path.join(_path, "flet.exe")):
            os.environ.setdefault("FLET_VIEW_PATH", _path)
            break

    if "--uninstall" in sys.argv:
        ft.run(uninstall_app)
        sys.exit(0)

    if "--file-sharing" in sys.argv:
        ft.run(file_sharing_app)
        sys.exit(0)

    if "--update" in sys.argv:
        ft.run(update_app)
        sys.exit(0)

    if "--bg-service-gui" in sys.argv:
        ft.run(bg_service_gui_app)
        sys.exit(0)

    if "--repair-wsa" in sys.argv:
        ft.run(repair_app)
        sys.exit(0)

    if not check_instance_lock():
        ft.run(running_app)
        sys.exit(0)

    _ensure_windows_service()
    _kill_existing_bg_service()
    spawn_bg_service_if_needed()
    ft.run(main, assets_dir=resource_path("assets"))

if __name__ == "__main__":
    start()