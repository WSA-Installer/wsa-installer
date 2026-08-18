# WSA Installer — Download Edition

This document covers the complete WSA Installer application, including all features available in the Download Edition (v1.2).

---

## Table of Contents

- [Overview](#overview)
- [New Features (Download Edition)](#new-features-download-edition)
- [CLI Reference](#cli-reference)
- [System Requirements](#system-requirements)
- [Installation Modes](#installation-modes)
- [3-Phase System Check](#3-phase-system-check)
- [WSA Pacman (APK Installer)](#wsa-pacman-apk-installer)
- [APK File Handler](#apk-handler)
- [Background Service](#background-service)
- [File Sharing (WebDAV)](#file-sharing-webdav)
- [Virtualization Bypass](#virtualization-bypass)
- [Configuration System](#configuration-system)
- [Security Architecture](#security-architecture)
- [Build Pipeline](#build-pipeline)

---

## Overview

WSA Installer is a professional one-click tool for installing **Windows Subsystem for Android** with **Google Play Store** on Windows 10 and Windows 11.

### What's Included

| Component | Description |
|-----------|-------------|
| **5-Step Wizard** | System Check → Bundle Check → Install WSA → Add Play Store → Complete |
| **3-Phase System Check** | System validation → Bundle detection → Virtualization bypass |
| **APK Pacman** | Double-click any APK to install directly into WSA |
| **Background Service** | Monitors WSA status, manages file sharing, handles auto-updates |
| **File Sharing** | WebDAV-based drive mounting for WSA user/root filesystems |
| **Self-Update** | Automatic update checking and silent installation |
| **Repair/Uninstall** | Complete WSA management from Windows Settings |

---

## New Features (Download Edition)

### 1. WSA Pacman — APK Double-Click Install

Double-click any `.apk`, `.xapk`, `.apks`, `.apkm`, or `.aab` file to install it directly into WSA.

**How it works:**
- Windows calls `app.py --wsa-pacman "C:\path\to\app.apk"`
- App parses APK metadata (name, package, version, icon)
- Automatically detects: install / update / downgrade / reinstall
- Shows a 6-step progress dialog
- Creates desktop shortcuts with watermarked icons

**Supported formats:**

| Format | Description | Install Method |
|--------|-------------|----------------|
| `.apk` | Standard Android package | `adb install -r` |
| `.xapk` | XAPK bundle | Extract → `adb install-multiple` |
| `.apks` | Split APK archive | Extract → `adb install-multiple` |
| `.apkm` | APKMirror bundle | Extract → `adb install-multiple` |
| `.aab` | Android App Bundle | Requires bundletool (not supported) |

### 2. APK File Handler Registration

WSA Installer registers itself as the Windows handler for APK files.

**Registration includes:**
- Windows Registry file associations for 5 formats
- Custom ProgIDs (`wsa-installer.apk`, etc.)
- `ApkIconShlExt.dll` — C++ shell extension for per-file APK icons in Explorer

**Commands:**
```cmd
app.py --register-apk      # Register file associations
app.py --unregister-apk    # Remove file associations
```

### 3. 3-Phase System Check

The installer now uses a 3-phase system check before installation:

| Phase | Purpose | Duration |
|-------|---------|----------|
| **Phase 1: System Check** | Windows version, virtualization, features, WSA status | ~10s |
| **Phase 2: Bundle Check** | Find bundle, check cache, extract if needed | ~30s |
| **Phase 3: System-Level Fixes** | Virtualization bypass, registry fixes, WSL2 | ~60s |

Each phase pauses for user confirmation before proceeding.

### 4. Virtualization Bypass

The installer automatically fixes common WSA compatibility issues:

| Fix | Description |
|-----|-------------|
| Hyper-V Enable | Ensures Hyper-V, VirtualMachinePlatform, HypervisorPlatform are enabled |
| KB Uninstall | Removes known problematic Windows Updates (KB5062553, KB5064081, etc.) |
| WSL2 Install | Installs WSL2 if not present |
| Defender Exclusion | Adds WSA folder to Windows Defender exclusion list |
| VBS Disable | Disables Virtualization-Based Security via registry |
| FsDepends Disable | Disables FsDepends service to fix virtual disk conflicts |

If any fix requires a restart, the installer:
1. Creates a RunOnce registry key
2. Shows a restart dialog
3. Automatically resumes after restart

### 5. Win10/Win11 Detection

The installer detects the Windows version and uses appropriate download sources:

| Windows | GitHub Source | Notes |
|---------|---------------|-------|
| Windows 11 | `CONFIG.GITHUB_API_URL` | Configurable via server |
| Windows 10 | MustardChef/WSABuilds | Fixed LTS release tag |

---

## CLI Reference

### Application Modes

| Argument | Description |
|----------|-------------|
| *(none)* | Launch 5-step installation wizard |
| `--wsa-pacman <path>` | Install APK from given path |
| `--register-apk` | Register APK file associations |
| `--unregister-apk` | Unregister APK file associations |
| `--repair-wsa` | Launch 4-step WSA repair wizard |
| `--uninstall` | Launch uninstall dialog |
| `--file-sharing` | File sharing setup (user mode) |
| `--file-sharing root` | File sharing setup (root mode) |
| `--update <url> <ver>` | Self-update dialog |
| `--bg-service` | Run as Windows background service |
| `--bg-service-gui` | Background service with visible console |
| `--install-service` | Register WSABackgroundService |
| `--uninstall-service` | Unregister WSABackgroundService |
| `--sdk` | Start Play Store patcher SDK |
| `--flet-patch` | Patch Flet client and exit |
| `--help`, `-h` | Show help message |

### NSIS Installer Arguments

| Argument | Description |
|----------|-------------|
| `/S` | Silent installation |
| `/S /repair` | Silent repair from Windows Settings |

---

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| OS | Windows 10 (build 19041+) or Windows 11 | Windows 11 22H2+ |
| RAM | 8 GB | 16 GB |
| Disk Space | 10 GB free | SSD with 20 GB free |
| Internet | Required for initial download | Broadband recommended |
| Privileges | Administrator | Administrator |
| Virtualization | Enabled in BIOS/UEFI | Intel VT-x or AMD-V |

### Windows Features Required

| Feature | How Installer Handles It |
|---------|-------------------------|
| Hyper-V | Auto-enabled |
| VirtualMachinePlatform | Auto-enabled |
| HypervisorPlatform | Auto-enabled |
| Windows Subsystem for Linux | Auto-enabled |

---

## Installation Modes

### Mode 1: With Bundle (Offline)

1. Download `WSA_Installer_Setup.exe` and `bundle.wsa`
2. Place both in the same folder
3. Run installer as administrator
4. Installer detects bundle automatically
5. Extracts and installs without internet

### Mode 2: Without Bundle (Online)

1. Download `WSA_Installer_Setup.exe` only
2. Run installer as administrator
3. Installer downloads WSA packages from GitHub
4. Supports resume on interrupted downloads

### Mode 3: Silent Installation

```cmd
WSA_Installer_Setup.exe /S
```

- Installs to `C:\Program Files\WSA Installer`
- Registers Windows service
- Creates shortcuts
- No UI shown

---

## 3-Phase System Check

### Phase 1: System Check

```
┌─────────────────────────────────────────────────┐
│  Phase 1: System Check                          │
├─────────────────────────────────────────────────┤
│  ✓ Windows Version          → Windows 11        │
│  ✓ Hardware Virtualization  → Ready             │
│  ✓ Hyper-V                  → Ready             │
│  ✓ Virtual Machine Platform → Ready             │
│  ✓ Hypervisor Platform      → Ready             │
│  ✓ Windows Subsystem Linux  → Ready             │
│  ✓ WSA Installed            → Running           │
└─────────────────────────────────────────────────┘
```

- Detects Windows version (10 vs 11)
- Checks BIOS virtualization (5 fallback methods)
- Verifies/enables 4 required Windows features
- Detects existing WSA installation

### Phase 2: Bundle Check

```
┌─────────────────────────────────────────────────┐
│  Phase 2: Bundle Check                          │
├─────────────────────────────────────────────────┤
│  ✓ Bundle in installer path → bundle.wsa        │
│  ✓ Cache folder             → Complete found    │
│  ✓ Basic package            → Found             │
│  ✓ PlayStore package        → Found             │
│  ✓ Download folder          → Skipped           │
│  ✓ Prepare cache            → Ready             │
│  ✓ Extract packages         → Extracted         │
│  ✓ Basic after extraction   → Found             │
│  ✓ PlayStore after extract  → Found             │
│  ✓ Clean up archive         → Removed           │
└─────────────────────────────────────────────────┘
```

Searches for bundle in:
1. Installer path (`out_asset/`)
2. `~/Downloads/` folder
3. Cache folder (`out_asset/cache/`)

### Phase 3: System-Level Fixes

```
┌─────────────────────────────────────────────────┐
│  Phase 3: System-Level Fixes                    │
├─────────────────────────────────────────────────┤
│  ✓ Hyper-V features         → All enabled       │
│  ✓ Problematic Updates      → OK                │
│  ✓ WSL2                     → OK                │
│  ✓ Defender exclusion       → Excluded          │
│  ✓ Registry fix (VBS)       → Applied           │
│  ✓ Registry fix (FsDepends) → Applied           │
└─────────────────────────────────────────────────┘
```

---

## WSA Pacman (APK Installer)

### Usage

Double-click any APK file in Windows Explorer, or:

```cmd
app.py --wsa-pacman "C:\Downloads\app.apk"
```

### Install Dialog

```
┌──────────────────────────────────────────────┐
│  📦 Install Android App                      │
├──────────────────────────────────────────────┤
│  ┌──────────────────────────────────────┐    │
│  │ [icon] App Name                      │    │
│  │        com.package.name              │    │
│  │        APK  ·  25.4 MB               │    │
│  └──────────────────────────────────────┘    │
│                                              │
│  ✓ WSA Installed          Found              │
│  ✓ Check WSA Status      Running            │
│  ✓ Start WSA             Skipped            │
│  ✓ Connect ADB           Connected          │
│  ○ Install App Name      Installing...      │
│  ○ Create Desktop Shortcut  —               │
│                                              │
│  ┌──────────────────────────────────────┐    │
│  │ > Installing com.package.name...     │    │
│  │ > Success                            │    │
│  └──────────────────────────────────────┘    │
│                                              │
│  ☑ Create Desktop shortcut                   │
│                                              │
│  [Cancel]                    [Install]       │
└──────────────────────────────────────────────┘
```

### Auto-Detection

The installer automatically detects the appropriate action:

| Scenario | Action | Button Text |
|----------|--------|-------------|
| App not installed | Install | "Install" |
| App installed, newer version | Update | "Update" |
| App installed, older version | Downgrade | "Downgrade" |
| App installed, same version | Reinstall | "Reinstall" |

---

## APK Handler

### Registration

When WSA Installer starts normally, it automatically registers APK file associations:

```
HKLM\Software\Classes\
├── .apk → wsa-installer.apk
├── .xapk → wsa-installer.xapk
├── .apks → wsa-installer.apks
├── .apkm → wsa-installer.apkm
├── .aab → wsa-installer.aab
│
├── wsa-installer.apk
│   ├── (Default) = "WSA Android Package"
│   └── shell\open\command = 'app.py' --wsa-pacman "%1"
│
└── (ApkIconShlExt.dll registered for icons)
```

### Shell Extension

`ApkIconShlExt.dll` provides per-file APK icons in Windows Explorer:
- Registers as IExtractIcon / IThumbnailProvider handler
- Shows the actual APK icon instead of generic file icon
- Works for `.apk`, `.xapk`, `.apks`, `.apkm` files

---

## Background Service

### WSABackgroundService

| Property | Value |
|----------|-------|
| Name | WSABackgroundService |
| Display Name | WSA Background Service |
| Start Type | Automatic |
| Recovery | Restart after 10s, 15s, 30s |
| Context | SYSTEM |

### Capabilities

- **WSA Monitoring**: Checks ADB port (58526) every second
- **SDK Lifecycle**: Starts/stops Play Store patcher SDK
- **File Sharing**: Auto-mounts/unmounts WebDAV drives
- **Config Sync**: Fetches remote configuration periodically
- **Auto-Update**: Checks for new versions and launches update dialog
- **User Session**: Spawns processes in logged-in user session via `CreateProcessAsUserW`

### Service Management

```cmd
# Install
app.py --install-service

# Uninstall
app.py --uninstall-service

# Run directly (for debugging)
app.py --bg-service-gui
```

---

## File Sharing (WebDAV)

### Modes

| Mode | Access | Requirements |
|------|--------|-------------|
| User Mode | `/storage/emulated/0` | WSA installed |
| Root Mode | `/` (full filesystem) | WSA + Magisk root |

### Setup

```cmd
# User mode
app.py --file-sharing

# Root mode
app.py --file-sharing root
```

### Process

1. Check WSA installed
2. Ensure WSA running
3. Connect ADB (15 attempts)
4. Install WebDAV APK (`com.wsa.webdav`)
5. Start WebDAV server (port 8088)
6. Configure Windows WebClient
7. Mount network drive (`net use X: http://127.0.0.1:8088/files/`)
8. Set drive icon and label

### Web File Manager

Access files via browser: `http://127.0.0.1:8088`

Features:
- Grid/list views
- Drag-and-drop upload
- Hex viewer
- Terminal access
- Bookmarks
- Batch rename

---

## Virtualization Bypass

The installer applies these system-level fixes automatically:

### 1. Hyper-V Features

```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -All
Enable-WindowsOptionalFeature -Online -FeatureName HypervisorPlatform -All
```

### 2. Problematic Windows Updates

Detects and uninstalls:
- KB5062553
- KB5064081
- KB5072033
- KB5094126

### 3. WSL2 Installation

```cmd
wsl --install --no-distribution
```

### 4. Defender Exclusion

```powershell
Add-MpPreference -ExclusionPath 'C:\...\Window Subsystem For Android'
```

### 5. Registry Fixes

```
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System
└── EnableVirtualizationBasedSecurity = 0

HKLM\SYSTEM\CurrentControlSet\Services\FsDepends
└── Start = 0
```

---

## Configuration System

### Config Sources (Priority Order)

```
Default Config → Developer Mode Config → Server Config
```

### ConfigController

- Source-tracked values (knows where each value came from)
- Validation against allowed types/values
- Server-side updates via `RemoteConfigManager`
- Hash-based deduplication (skips unchanged configs)

### RemoteConfigManager

- Polls server JSON every `CONFIG_SYNC_INTERVAL` ms
- Validates via `widget_ui.pyd` (Rust security gateway)
- Applies config changes with hash deduplication
- Quick retry on failure (5s interval)

### Developer Mode

If `developer_mode.py` exists with a `CONFIG` dict, it's applied as an overlay on top of default config.

---

## Security Architecture

```
┌──────────────────────────────────────────────────────┐
│                  Security Layers                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Layer 1: widget_ui.pyd (Rust)                      │
│  ├── Zero-trust config gateway                      │
│  ├── Signature verification                         │
│  └── Encrypted config parsing                       │
│                                                      │
│  Layer 2: Socket-based Instance Locks               │
│  ├── Single instance enforcement (port 65432)       │
│  └── BG service lock (port 65433)                   │
│                                                      │
│  Layer 3: Windows Service                           │
│  ├── SYSTEM-level service                           │
│  ├── Auto-restart on failure                        │
│  └── User session process spawning                  │
│                                                      │
│  Layer 4: Source Protection                         │
│  ├── Nuitka compilation (app.py → app.pyd)          │
│  ├── PyInstaller bundling                           │
│  └── Binary string obfuscation                      │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## Build Pipeline

### Primary Build (build.bat)

```
Step 1: Clean
    └── Removes dist/, build/, app.pyd

Step 2: Dependencies
    └── pip install -r requirements.txt

Step 3: Version Update
    └── PowerShell replaces version in app.py + file_version_info.txt

Step 4: Nuitka Module
    ├── Compiles app.py → app.pyd (source protection)
    └── Renames app.py → wsa.py to hide source

Step 5: PyInstaller Onedir
    ├── Uses WSA_Installer_Download_onedir.spec
    └── Restores app.py from wsa.py

Step 6: WSARepair.exe
    └── PyInstaller --onefile

Step 7: Flet Client Patch
    ├── Patches flet.exe icon + version info
    └── Creates patched flet-windows.zip

Step 8: NSIS Installer
    └── Builds WSA_Installer_Setup.exe
```

### Build Requirements

- Python 3.14 with pip
- Nuitka: `pip install nuitka`
- PyInstaller: `pip install pyinstaller`
- NSIS: [nsis.sourceforge.io](https://nsis.sourceforge.io)

---

## Related Documentation

- [Flow Guide](flow.md) — Complete user flow documentation
- [Architecture Guide](architecture.md) — Technical architecture
- [CLI Reference](cli-reference.md) — Command-line arguments
- [Installation Guide](installation.md) — Step-by-step installation
- [File Sharing Guide](webdav.md) — WebDAV setup
- [Troubleshooting Guide](troubleshooting.md) — Common issues
- [Developer Guide](developer-guide.md) — Contributing guide
