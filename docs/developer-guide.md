# Developer Guide

This guide is for developers who want to contribute to WSA Installer or understand its internals.

## Prerequisites

- Python 3.14
- Windows 10/11
- Git
- Administrator privileges (for testing)

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/WSA-Installer/wsa-installer.git
cd wsa-installer
```

### Set Up Development Environment

```bash
# Run the development launcher
run.bat
```

This will:
1. Create a Python virtual environment
2. Install all dependencies
3. Launch the application

### Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

## Project Structure

```
wsa-installer/
├── app.py                    # Main application (~12.6K lines)
├── run.py                    # Entry point: import app; app.start()
├── WSARepair.py              # Windows Settings proxy
├── patch_flet.py             # Flet client patcher
├── launcher.cs               # C# launcher for Nuitka builds
│
├── assets/                   # Runtime resources
│   ├── adb.exe               # ADB binary
│   ├── AppxManifest.xml      # WSA manifest
│   ├── Run.bat               # MagiskOnWSALocal launcher
│   ├── settings.dat          # Pre-patched WSA settings
│   ├── ApkIconShlExt.dll     # C++ APK icon shell extension
│   ├── wsa-webdav.apk        # WebDAV server APK
│   └── icon.ico              # Application icon
│
├── native/                   # Rust native modules
│   ├── widget_ui.pyd         # Security gateway
│   └── playstore_patcher_mem.pyd  # Play Store SDK
│
├── net_provider/             # Rust network provider + WSA init
├── shell_ext/                # C++ APK shell extension
├── emb_py/                   # Embedded Python 3.14
├── scripts/                  # Build/utility scripts
├── build/                    # Build scripts
├── docs/                     # Documentation
└── tests/                    # Tests
```

## Key Files

### app.py

The main application file containing:

- **Flet GUI** — User interface with 5-step wizard and 3-phase system check
- **InstallerLogic** — Core engine with 30-chunk parallel downloads
- **WSA Pacman** — Double-click APK installer (`wsa_pacman_install_app`)
- **APK Handler** — Windows Registry file association (`_register_apk_handler`)
- **ConfigController** — Configuration management with source tracking
- **RemoteConfigManager** — Server sync with hash deduplication
- **Background Service** — Windows SCM service with WSA monitoring
- **Virtualization Bypass** — System-level compatibility fixes
- **Dialog Functions** — Uninstall, update, repair, file sharing

### run.py

Simple entry point:
```python
import app
app.start()
```

### WSARepair.py

Proxy for Windows Settings Repair/Uninstall buttons. Finds the installer via 4 registry search methods.

## Code Conventions

### Python Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings for public functions
- Type hints where appropriate

### Commit Messages

Follow Conventional Commits:
```
feat(scope): description
fix(scope): description
docs(scope): description
```

### Branch Naming

- `feature/description` — New features
- `fix/description` — Bug fixes
- `docs/description` — Documentation

## Building

### Primary Build

```cmd
build.bat
```

Produces `dist/WSA_Installer_Setup.exe`.

### Build Requirements

- Python 3.14 with pip
- Nuitka: `pip install nuitka`
- PyInstaller: `pip install pyinstaller`
- NSIS: [nsis.sourceforge.io](https://nsis.sourceforge.io)

### Build Pipeline

1. Clean previous builds
2. Install dependencies
3. Update version numbers
4. Nuitka: Compile `app.py` → `app.pyd`
5. PyInstaller: Bundle to `dist/WSA Installer/`
6. Patch Flet client
7. NSIS: Build installer

## Testing

### Manual Testing

1. Run the application: `run.bat`
2. Test each wizard step
3. Test repair and uninstall flows
4. Test on both Windows 10 and 11

### Test Checklist

- [ ] Fresh installation works
- [ ] Play Store installs correctly
- [ ] Repair flow completes
- [ ] Uninstall removes everything
- [ ] Background service starts
- [ ] File sharing mounts drive
- [ ] Self-update works
- [ ] UI renders correctly

## Debugging

### Enable Debug Logging

Edit `app.py` and set debug flags:

```python
DEBUG = True
```

### View Logs

- `wsa_activity.log` — Session activity
- `debug.log` — Debug output
- UI Log Box — In-app logging

### Common Debug Scenarios

**Download issues:**
- Check network connectivity
- Verify GitHub releases are accessible
- Check download progress in UI

**ADB issues:**
- Ensure WSA is running
- Check Developer Mode is enabled
- Verify port 58526 is accessible

**Service issues:**
- Check Windows Event Viewer
- Verify service permissions
- Review service failure recovery

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

## Architecture

See [architecture.md](architecture.md) for detailed architecture documentation.
