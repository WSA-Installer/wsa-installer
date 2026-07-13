# Installation Guide

This guide walks you through installing WSA Installer on your Windows 10 or Windows 11 system.

## Prerequisites

| Requirement | Minimum | Recommended |
|:------------|:--------|:------------|
| OS | Windows 10 (build 19041+) or Windows 11 | Windows 11 22H2+ |
| RAM | 8 GB | 16 GB |
| Disk Space | 10 GB free | SSD with 20 GB free |
| Internet | Required for initial download | Broadband recommended |
| Privileges | Administrator | Administrator |
| Virtualization | Enabled in BIOS/UEFI | Intel VT-x or AMD-V |

### Windows Features Required

The following Windows features must be enabled. WSA Installer can enable them automatically:

- **Hyper-V** — Microsoft's hardware virtualization
- **VirtualMachinePlatform** — Required for WSA
- **HypervisorPlatform** — Hypervisor interface
- **Windows Subsystem for Linux** — Required for WSA

## Download

### Option A: Installer Only

Download `WSA_Installer_Setup.exe` (~228 MB) from the [latest release](https://github.com/WSA-Installer/wsa-installer/releases/latest).

The installer will download WSA packages directly from GitHub during installation.

### Option B: Installer + Bundle

Download both:
1. `WSA_Installer_Setup.exe` (~228 MB)
2. `bundle.wsa` (~1.21 GB)

Place both files in the same folder. The installer will detect the bundle automatically.

## Installation Steps

### Step 1: Run the Installer

1. Right-click `WSA_Installer_Setup.exe`
2. Select **Run as administrator**
3. Accept the UAC (User Account Control) prompt

### Step 2: Welcome Screen

The installer will display a welcome page with information about the installation process. Click **Next** to continue.

### Step 3: System Check

The installer automatically scans your system for:

- Virtualization support (VT-x/AMD-V)
- Hyper-V status
- VirtualMachinePlatform status
- HypervisorPlatform status
- WSL status

If any required features are missing, the installer will offer to enable them. You may need to restart your computer after enabling features.

### Step 4: Install WSA

The installer proceeds through 6 phases:

| Phase | Description |
|:------|:------------|
| 1. Locate Package | Finds WSA package (from bundle or GitHub download) |
| 2. Verify Assets | Validates archive integrity |
| 3. Prepare System | Extracts files, copies to installation directory |
| 4. Apply Patches | Developer Mode settings, registry fixes, WsaClient patches |
| 5. Register Package | Registers WSA with Windows |
| 6. Finalize | Creates shortcuts, configures background service |

### Step 5: Add Play Store (Optional)

If you selected the Play Store option, the installer proceeds through 7 additional phases:

| Phase | Description |
|:------|:------------|
| 1. Prerequisites | Checks WSA is running and Developer Mode is enabled |
| 2. Enable Dev Mode | Patches settings.dat for Developer Mode |
| 3. Connect ADB | Establishes ADB connection to WSA |
| 4. Prepare Package | Locates and verifies GApps package |
| 5. Apply Patches | Merges Play Store files into WSA |
| 6. Run Installer | Executes Run.bat via ADB |
| 7. Finalize | Verifies Play Store, cleans up, restarts WSA |

### Step 6: Complete

Once installation is complete:

- **Play Store** shortcut appears in Start Menu
- **Windows Subsystem for Android** shortcut appears on Desktop
- **WSABackgroundService** is installed and running
- You can now launch Android apps directly from the Start Menu

## Silent Installation

For automated deployment:

```cmd
WSA_Installer_Setup.exe /S
```

The silent installer:
- Installs to `C:\Program Files\WSA Installer`
- Registers the Windows service
- Creates desktop and Start Menu shortcuts
- Does NOT show any UI

## Post-Installation

### Verify WSA is Working

1. Open the Start Menu
2. Search for "Windows Subsystem for Android"
3. Launch the WSA Settings app
4. Enable Developer Mode if not already enabled

### Verify Play Store

1. Open the Start Menu
2. Search for "Play Store"
3. Sign in with your Google account
4. Install Android apps

### Check Background Service

1. Open Windows Services (`services.msc`)
2. Find `WSABackgroundService`
3. Verify it's running

## Troubleshooting

### Installation Fails

1. Ensure you're running as administrator
2. Check that virtualization is enabled in BIOS/UEFI
3. Try enabling Hyper-V manually: `dism.exe /Online /Enable-Feature /FeatureName:Microsoft-Hyper-V /All`

### WSA Won't Start

1. Restart your computer after installation
2. Check that all Windows features are enabled
3. Run the installer again and use the Repair option

### Play Store Not Working

1. Ensure Developer Mode is enabled in WSA Settings
2. Wait a few minutes for Play Store to initialize
3. Try signing out and back into your Google account

For more troubleshooting, see the [Troubleshooting Guide](troubleshooting.md).
