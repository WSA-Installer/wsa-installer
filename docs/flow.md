# Application Flow Guide

This document describes how `app.py` works end-to-end — covering every user flow from launch to completion.

---

## Table of Contents

- [Main Application Launch](#main-application-launch)
- [Installation Flow — With Bundle](#installation-flow--with-bundle)
- [Installation Flow — Without Bundle](#installation-flow--without-bundle)
- [APK Pacman Flow (Double-Click Install)](#apk-pacman-flow-double-click-install)
- [Background Service Flow](#background-service-flow)
- [Update Flow](#update-flow)
- [Repair Flow](#repair-flow)
- [Uninstall Flow](#uninstall-flow)
- [File Sharing Flow](#file-sharing-flow)
- [APK Handler Registration](#apk-handler-registration)

---

## Main Application Launch

When `app.py` starts (via `run.py` or directly), the `start()` function executes:

```
start()
├── Set FLET_VIEW_PATH (patched Flet client detection)
├── Route to specific mode based on CLI args:
│   ├── --uninstall        → uninstall_app()
│   ├── --file-sharing     → file_sharing_app()
│   ├── --update           → update_app()
│   ├── --bg-service-gui   → bg_service_gui_app()
│   ├── --repair-wsa       → repair_app()
│   ├── --register-apk     → _register_apk_handler()
│   ├── --unregister-apk   → _unregister_apk_handler()
│   ├── --wsa-pacman       → wsa_pacman_install_app()
│   └── (no args)          → main() [5-step wizard]
├── check_instance_lock() (single-instance enforcement)
├── _ensure_windows_service()
├── _register_apk_handler() (auto-register APK file associations)
└── ft.run(main) (launch Flet GUI)
```

### Configuration Loading

Before the GUI starts, the app loads configuration through a security pipeline:

```
load_secure_initial_config()
├── widget_ui.load() (Rust security gateway)
│   ├── Signature verification
│   ├── Encrypted config parsing
│   └── Schema validation
├── Force AD_SPONSOR_URL and APP_ID
└── Return config_data

ConfigController(config_data)
├── Apply default values
├── Load developer mode overlay (if developer_mode.py exists)
├── Start RemoteConfigManager
│   ├── Poll server JSON every CONFIG_SYNC_INTERVAL
│   ├── Validate via widget_ui.pyd
│   ├── Apply config changes with hash deduplication
│   └── Refresh UI on config change
└── Report all config values with source tracking
```

---

## Installation Flow — With Bundle

The installation uses a **3-Phase** system check before installing:

### Phase 1: System Check (`_run_system_check`)

```
System Check
├── Phase 0: Clean up RunOnce key (if resuming after restart)
├── Row 0: Windows Version Detection
│   ├── Win11 → uses CONFIG.GITHUB_API_URL
│   └── Win10 → uses MustardChef/WSABuilds API
├── Row 1: BIOS Virtualization (VT-x/AMD-V)
│   ├── Method 1: WMI VirtualizationFirmwareEnabled
│   ├── Method 2: systeminfo hypervisor detection
│   ├── Method 3: Get-ComputerInfo
│   ├── Method 4: Hyper-V feature active check
│   └── Method 5: Registry VmMonitorModeExtensions
├── Rows 2-5: Required Windows Features
│   ├── Microsoft-Hyper-V
│   ├── VirtualMachinePlatform
│   ├── HypervisorPlatform
│   └── Microsoft-Windows-Subsystem-Linux
│   (Auto-enables if missing, with DISM fallback)
├── Row 6: WSA Installation Check
│   ├── Detect install location
│   └── Check if WSA is running
└── Pause → scan_stage = "system_done" → User clicks Continue
```

### Phase 2: Bundle Check (`_run_bundle_check`)

```
Bundle Check
├── Row 0: Check WSA installer path (out_asset/)
│   └── Search for: bundle.wsa, bundle.7z, bundle.zip
├── Row 4: Check ~/Downloads folder
│   └── Same candidate names
├── Row 1: Check cache folder (out_asset/cache/)
│   ├── Detect nogapps package
│   ├── Detect gapps package
│   └── Report: complete / partial / empty
├── Rows 2-3: Package status display
├── Row 5: Prepare cache folder (if bundle found)
├── Row 6: Extract bundle → cache/
│   └── Uses 7z.exe for extraction
├── Rows 7-8: Verify packages after extraction
├── Row 9: Clean up bundle archive
└── Pause → scan_stage = "bundle_done" → User clicks Continue
```

### Phase 3: System-Level Fixes (`_apply_system_fixes`)

```
System-Level Fixes (Virtualization Bypass)
├── Row 0: Ensure Hyper-V features
├── Row 1: Uninstall problematic Windows Updates
│   └── KB5062553, KB5064081, KB5072033, KB5094126
├── Row 2: Ensure WSL2
├── Row 3: Add Defender exclusion
├── Row 4: Registry fix (VBS — Disable Virtualization-Based Security)
├── Row 5: Registry fix (FsDepends — Disable FsDepends service)
└── If restart needed → Create RunOnce key → Show restart dialog
```

### Phase 4-7: WSA Installation (`install_wsa`)

```
WSA Installation (6 Phases)
├── Phase 1: Locate Package
│   ├── Check unified destination (out_asset/Window Subsystem For Android/)
│   ├── Check legacy folder (WSA Basic Package/)
│   ├── Check bundled assets
│   ├── Check cached archive
│   └── Extract if needed
├── Phase 2: Verify Assets
│   ├── Read filelist.txt
│   └── Verify all required files exist
├── Phase 3: Prepare System
│   ├── Kill WSA processes (graceful + force)
│   ├── Deploy desktop shortcut
│   └── Copy files to destination
├── Phase 4: Apply Patches
│   ├── Patch Run.bat
│   ├── Patch WsaClient.exe (crash fix)
│   ├── Patch AppxManifest.xml (Repair → WSARepair.exe)
│   └── Install WSARepair proxy
├── Phase 5: Run Installer
│   ├── Cleanup temp files
│   ├── Run Install.ps1
│   └── Register WSA package
└── Phase 6: Finalize
    ├── Verify installation
    ├── Install WSABackgroundService
    ├── Configure auto-start
    └── Create shortcuts
```

### Phase 8: Add Play Store (`add_playStore`)

```
Play Store Integration (7 Phases)
├── Phase 1: Prerequisites
│   ├── Check WSA is running
│   └── Verify Developer Mode
├── Phase 2: Enable Dev Mode
│   └── Patch settings.dat
├── Phase 3: Connect ADB
│   ├── 15 connection attempts
│   ├── Server restart on failure
│   └── Automate ADB authorization popup
├── Phase 4: Prepare Package
│   ├── Locate GApps archive
│   └── Verify package integrity
├── Phase 5: Apply Patches
│   └── Merge GApps into WSA
├── Phase 6: Run Installer
│   └── Execute Run.bat via ADB
└── Phase 7: Finalize
    ├── Verify Play Store installed
    ├── Copy Play Store icon
    ├── Clean up temporary files
    └── Restart WSA
```

---

## Installation Flow — Without Bundle

When no bundle is found, the installer downloads from GitHub:

```
No Bundle Found
├── Bundle Check Result: "not_found" or "partial"
├── User clicks "Install WSA Basic"
│   ├── Show download overlay
│   ├── fetch_github_assets("nogapps")
│   │   ├── Win11: CONFIG.GITHUB_API_URL (MustardChef/WSABuilds)
│   │   └── Win10: MustardChef/WSABuilds Windows_10 tag
│   ├── User selects version from list
│   └── download_asset()
│       ├── HEAD request → get remote size
│       ├── Split into 30 chunks
│       ├── ThreadPoolExecutor parallel download
│       ├── HTTP Range headers for resume
│       ├── .part files preserved on cancel
│       └── Merge chunks → final file
├── Extract to unified destination
└── Continue with install_wsa() (same as above)
```

For Play Store (if selected):

```
User clicks "Add Play Store"
├── Check if GApps in cache
│   ├── Yes → use cached
│   └── No → download from GitHub
│       ├── fetch_github_assets("gapps")
│       ├── User selects version
│       └── download_asset()
├── Extract to unified destination
└── Continue with add_playStore() (same as above)
```

---

## APK Pacman Flow (Double-Click Install)

When a user double-clicks an `.apk`, `.xapk`, `.apks`, `.apkm`, or `.aab` file:

```
Double-Click APK File
├── Windows calls: app.py --wsa-pacman "C:\path\to\app.apk"
├── wsa_pacman_install_app(page)
│   ├── Parse APK metadata
│   │   ├── _parse_apk() → name, package, version, icon, size, type
│   │   └── Detect file type (APK/XAPK/APKS/APKM/AAB)
│   ├── Build install dialog UI
│   │   ├── App info card (icon, name, package, size)
│   │   ├── 6-step progress tracker
│   │   ├── Log box
│   │   └── Action buttons (Install/Open/Done/Cancel)
│   │
│   ├── Step 0: Check WSA Installed
│   │   ├── _ensure_wsa_installed() → search registry, paths
│   │   └── If not found → show "Open WSA Installer" button
│   │
│   ├── Step 1: Check WSA Status
│   │   └── _check_port() → socket connect to port 58526
│   │
│   ├── Step 2: Start WSA (if needed)
│   │   ├── powershell Start-Process wsa://system
│   │   └── Wait up to 30 seconds for port to open
│   │
│   ├── Step 3: Connect ADB
│   │   ├── 15 connection attempts
│   │   ├── Detect existing installation
│   │   └── Determine action: install / update / downgrade / reinstall
│   │
│   ├── [User clicks Install button]
│   │
│   ├── Step 4: Install APK
│   │   ├── APK → adb install -r
│   │   ├── XAPK/APKS → extract with 7z → adb install-multiple
│   │   ├── AAB → error (requires bundletool)
│   │   └── Support --downgrade flag
│   │
│   └── Step 5: Create Desktop Shortcut
│       ├── Find WsaClient.exe path
│       ├── Create .lnk shortcut with: /launch wsa://<package>
│       └── Watermark icon with WSA Installer branding
│
└── Show success dialog with Open/Done buttons
```

---

## Background Service Flow

The background service runs as a Windows SCM service (`WSABackgroundService`):

```
Service Start
├── Single-instance lock (port 65433, SO_EXCLUSIVEADDRUSE)
├── Load config from widget_ui.load()
├── Fetch initial remote config
├── Install Windows service (if not exists)
│
├── Main Monitor Loop (1-second polling):
│   ├── Check WSA ADB port (58526)
│   ├── Detect WSA state changes (started/stopped)
│   │   ├── WSA Started →
│   │   │   ├── Start SDK process
│   │   │   ├── Wait 15s for full initialization
│   │   │   └── Auto-mount file shares
│   │   └── WSA Stopped →
│   │       ├── Stop SDK process
│   │       └── Auto-unmount (if auto_unmount=1)
│   │
│   ├── Check file sharing toggle (every 5s)
│   │   ├── share_user toggled ON → mount user drive
│   │   ├── share_user toggled OFF → unmount user drive
│   │   ├── share_root toggled ON → mount root drive
│   │   └── share_root toggled OFF → unmount root drive
│   │
│   ├── Ensure drives are mounted (if WSA running)
│   │   ├── Check drive connectivity
│   │   ├── Check WebDAV port 8088
│   │   └── Auto-remount if disconnected
│   │
│   ├── Fetch remote config (CONFIG_SYNC_INTERVAL)
│   │   └── Apply config changes with hash dedup
│   │
│   ├── Check for app updates (CONFIG_SYNC_INTERVAL)
│   │   ├── Compare remote APP_ID version vs local
│   │   └── Launch update dialog if newer version available
│   │
│   └── Verify drive labels (every 5s)
│
├── SDK Manager
│   ├── start() → CreateProcessAsUserW in user session
│   ├── stop() → Terminate SDK process
│   └── reset_if_crashed() → Detect and cleanup crashed SDK
│
└── File Sharing Mount Flow
    ├── Connect ADB
    ├── Install WebDAV APK (if not present)
    ├── Start WebDAV server
    │   ├── User mode: am start -n com.wsa.webdav/.MainActivity
    │   └── Root mode: su -c "sh app.sh start"
    ├── Forward port 8088
    ├── Start WebClient service
    ├── Mount network drive: net use X: http://127.0.0.1:8088/files/
    ├── Set drive icon and label in registry
    └── Refresh Explorer
```

---

## Update Flow

```
Self-Update Process
├── RemoteConfigManager polls server
│   └── Fetches JSON config with APP_ID and UPDATE_EXE_URL
├── _check_for_app_update()
│   ├── Extract version from remote APP_ID
│   ├── Get installed version from registry
│   ├── Compare versions (remote > local)
│   └── If newer → launch update dialog
├── Update Dialog (--update)
│   ├── Download new EXE from UPDATE_EXE_URL
│   ├── Verify download
│   └── Execute silent installer
└── Service auto-restart after update
```

---

## Repair Flow

```
WSA Repair (--repair-wsa)
├── Step 1: Detect WSA installation
├── Step 2: Stop WSA processes
├── Step 3: Backup current WSA data
│   └── _wsa_backup_path() → LOCALAPPDATA/.../backup/
├── Step 4: Reinstall WSA
│   ├── Use cached packages or download fresh
│   └── Run full install_wsa() flow
└── Step 5: Restore backup data
    └── Restore user settings and data
```

---

## Uninstall Flow

```
WSA Uninstall (--uninstall)
├── Step 1: Stop WSA processes
├── Step 2: Unregister WSA package
├── Step 3: Remove WSA files
├── Step 4: Stop and remove WSABackgroundService
├── Step 5: Clean up file sharing
│   ├── Unmount all drives
│   └── Remove drive icons from registry
├── Step 6: Remove shortcuts
├── Step 7: Unregister APK handler
└── Step 8: Clean up registry entries
```

---

## File Sharing Flow

```
File Sharing Setup (--file-sharing)
├── Step 1: Check WSA installed
├── Step 2: Ensure WSA running
├── Step 3: Connect ADB (15 attempts)
├── Step 4: Install WebDAV APK
├── Step 5: Detect Root (Root mode only)
│   └── su -c whoami
├── Step 6: Start WebDAV Server
│   ├── User mode: am start
│   └── Root mode: su -c "sh app.sh start"
├── Step 7: Port forwarding (tcp:8088)
├── Step 8: Configure Windows WebClient
│   ├── BasicAuthLevel=2
│   ├── FileSizeLimitInBytes=4GB
│   └── Start WebClient service
├── Step 9: Mount network drive
│   └── net use X: http://127.0.0.1:8088/files/ /persistent:yes
└── Step 10: Set drive icon and label
```

---

## APK Handler Registration

When the app starts normally (no CLI args), it auto-registers APK file associations:

```
APK Handler Registration
├── Register ProgIDs in HKLM\Software\Classes:
│   ├── wsa-installer.apk   → .apk
│   ├── wsa-installer.xapk  → .xapk
│   ├── wsa-installer.apks  → .apks
│   ├── wsa-installer.apkm  → .apkm
│   └── wsa-installer.aab   → .aab
├── Set open command:
│   └── "app.py" --wsa-pacman "%1"
├── Register ApkIconShlExt.dll (regsvr32)
│   └── Provides per-file APK icons in Explorer
└── Notify Explorer of changes (SHChangeNotify)
```

To unregister:
```cmd
app.py --unregister-apk
```

---

## State Dictionary Keys

The `InstallerLogic` class uses a state dictionary with 40+ keys:

| Key | Type | Description |
|-----|------|-------------|
| `current_step` | int | Active wizard step (1-5) |
| `checking` | bool | System scan in progress |
| `installing` | bool | WSA installation in progress |
| `ps_installing` | bool | Play Store installation in progress |
| `scan_stage` | str | "system_done" / "bundle_done" / "complete" |
| `scan_complete` | bool | All 3 phases completed |
| `wsa_found` | bool | WSA detected on system |
| `wsa_running` | bool | WSA ADB port accessible |
| `windows_version` | str | "10" / "11" / "unknown" |
| `bundle_check_result` | str | "cached" / "found" / "partial" / "not_found" |
| `show_download` | str | "nogapps" / "gapps" / None |
| `download_progress` | float | 0.0 to 1.0 |
| `download_speed` | str | Formatted speed (e.g., "5.2 MB/s") |
| `download_eta` | str | Formatted time (e.g., "2m 15s remaining") |
| `install_log` | str | Installation log text |
| `ps_log` | str | Play Store log text |
| `install_phase` | int | Current installation phase (0-5) |
| `install_phase_title` | str | Phase title |
| `install_sub_status` | list | Phase step statuses |
| `check_sub_status` | list | System check step statuses |
| `show_restart_dialog` | bool | Restart prompt visible |
| `show_force_extract` | str | Re-download prompt archive name |

---

## Async Architecture

The application uses Python's `asyncio` for non-blocking operations:

```
Main Thread (Flet UI)
├── ft.run(main) → Flet event loop
├── RemoteConfigManager.fetch() → AsyncWorker
├── InstallerLogic methods → asyncio.create_subprocess
└── _MockTimer → Background polling

Worker Threads
├── AsyncWorker (QThread wrapper)
│   ├── Network fetches
│   └── Config updates
├── Download threads (ThreadPoolExecutor)
│   └── 30 parallel chunk downloads
└── Service monitor thread
    └── 1-second polling loop
```

### Signal System

Custom signal/slot system for thread-safe UI updates:

```python
class Signal:
    callbacks = []
    def connect(callback)
    def emit(*args, **kwargs)

class _MockTimer:
    timeout = Signal()
    def start(ms)
    def stop()
    def singleShot(ms, callback)
```

---

## Error Recovery

| Scenario | Recovery |
|----------|----------|
| Download cancelled | .part files preserved for resume |
| ADB connection fails | 15 retry attempts with server restart |
| WSA extraction fails | Force re-extract dialog with re-download option |
| WSA validation fails | Up to 2 retries before marking package broken |
| Service crash | SCM auto-restart (10s → 15s → 30s intervals) |
| Config fetch fails | Fallback to default/dev config, quick retry (5s) |
| Process lock | taskkill /F /T /PID tree termination |
| RunOnce resume | Auto-detect and clean up after restart |
