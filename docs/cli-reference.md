# CLI Reference

WSA Installer supports various command-line arguments for automation and advanced usage.

## Basic Usage

```cmd
WSA Installer.exe [OPTIONS]
```

## Command Line Arguments

| Argument | Description |
|:---------|:------------|
| `--install-service` | Install WSABackgroundService |
| `--uninstall-service` | Remove WSABackgroundService |
| `--bg-service` | Run as background service (SYSTEM context) |
| `--bg-service-gui` | Background service with visible console |
| `--uninstall` | Launch uninstall dialog |
| `--update <url> <ver>` | Self-update dialog |
| `--repair-wsa` | 4-step WSA repair |
| `--file-sharing` | File sharing (WebDAV mount) dialog |
| `--file-sharing root` | File sharing with root access |
| `--ad <url> <secs>` | Spawn ad overlay |
| `--sdk` | Start Play Store patcher SDK |

## NSIS Installer Arguments

| Argument | Description |
|:---------|:------------|
| `/S` | Silent installation |
| `/S /repair` | Silent repair from Windows Settings |

## Examples

### Silent Installation

```cmd
WSA_Installer_Setup.exe /S
```

Installs WSA Installer to `C:\Program Files\WSA Installer` without showing any UI.

### Install Background Service

```cmd
WSA Installer.exe --install-service
```

Creates and starts the `WSABackgroundService` Windows service.

### Uninstall Background Service

```cmd
WSA Installer.exe --uninstall-service
```

Stops and removes the `WSABackgroundService`.

### Launch Uninstaller

```cmd
WSA Installer.exe --uninstall
```

Opens the uninstall wizard with 7-step visual progress.

### Repair WSA

```cmd
WSA Installer.exe --repair-wsa
```

Opens the 4-step repair wizard (detect → stop → backup → reinstall).

### File Sharing (User Mode)

```cmd
WSA Installer.exe --file-sharing
```

Opens the file sharing setup dialog for user storage access.

### File Sharing (Root Mode)

```cmd
WSA Installer.exe --file-sharing root
```

Opens the file sharing setup dialog with root filesystem access.

### Self-Update

```cmd
WSA Installer.exe --update https://example.com/new.exe 1.3.0
```

Downloads and installs the specified update version.

### Background Service Mode

```cmd
WSA Installer.exe --bg-service
```

Runs as a Windows Service in SYSTEM context (no GUI).

### Background Service with GUI

```cmd
WSA Installer.exe --bg-service-gui
```

Runs as background service with a visible console window for debugging.

## Windows Service Management

### Using sc Commands

```cmd
# Install service
sc create WSABackgroundService binPath= "C:\Program Files\WSA Installer\WSA Installer.exe --bg-service" start= auto

# Configure failure recovery
sc failure WSABackgroundService reset=86400 actions=restart/10000/restart/15000/restart/30000

# Start service
sc start WSABackgroundService

# Stop service
sc stop WSABackgroundService

# Delete service
sc delete WSABackgroundService
```

### Service Properties

| Property | Value |
|:---------|:------|
| Name | WSABackgroundService |
| Display Name | WSA Background Service |
| Start Type | Automatic |
| Recovery | Restart after 10s, 15s, 30s |
| Reset Period | 86400 seconds (24 hours) |

## Environment Variables

| Variable | Description |
|:---------|:------------|
| `FLET_VIEW_PATH` | Custom path to Flet client executable |

## Exit Codes

| Code | Description |
|:-----|:------------|
| 0 | Success |
| 1 | Error or cancellation |
