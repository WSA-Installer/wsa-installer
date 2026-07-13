# File Sharing (WebDAV) Guide

WSA Installer includes a WebDAV-based file sharing feature that mounts your WSA file system as a Windows network drive, allowing you to access Android files directly from File Explorer.

## Overview

File sharing uses a WebDAV server running inside WSA to serve files over HTTP. Windows mounts this as a network drive, making Android files accessible like any other folder.

### Modes

| Mode | Access | Requirements |
|:-----|:-------|:-------------|
| User Mode | `/storage/emulated/0` (user storage) | WSA installed |
| Root Mode | `/` (full filesystem) | WSA + Magisk root |

## How to Enable

### Method 1: From WSA Installer

1. Open WSA Installer
2. Click **Advanced** in the sidebar
3. Select the file sharing mode (User or Root)
4. Choose a drive letter
5. Toggle the switch to enable

### Method 2: Command Line

```cmd
WSA Installer.exe --file-sharing
WSA Installer.exe --file-sharing root
```

## Setup Process

The file sharing setup performs these steps:

### Step 1: Check WSA

Verifies WSA is installed on the system.

### Step 2: Ensure WSA Running

Starts WSA if not already running. Waits for the ADB port (58526) to become available.

### Step 3: Connect ADB

Establishes an ADB connection to WSA (15 attempts with server restart).

### Step 4: Install WebDAV APK

Installs `com.wsa.webdav` APK via ADB. This APK contains:
- WebDAV server
- Web file manager SPA
- Shell control script

### Step 5: Detect Root (Root Mode Only)

Checks if Magisk is installed and root access is available via `su -c whoami`.

### Step 6: Start WebDAV Server

**User Mode:**
```cmd
adb shell am start -n com.wsa.webdav/.MainActivity
```

**Root Mode:**
```cmd
adb shell su -c "sh /data/data/com.wsa.webdav/files/app.sh start"
```

### Step 7: Port Forwarding

Forwards port 8088 from WSA to localhost:
```cmd
adb forward tcp:8088 tcp:8088
```

### Step 8: Configure Windows WebClient

Configures Windows to support WebDAV:
- Sets `BasicAuthLevel=2` (allows basic auth over HTTP)
- Sets `FileSizeLimitInBytes=4GB`
- Starts the WebClient service

### Step 9: Mount Network Drive

Mounts the WebDAV share as a Windows drive:
```cmd
net use X: http://127.0.0.1:8088/files/ /persistent:yes
```

### Step 10: Set Drive Icon and Label

Configures the drive icon and label in Windows Registry:
- `DriveIcons\X\DefaultLabel` = "WSA Files"
- `DriveIcons\X\DefaultIcon` = custom icon

## Using File Sharing

### Access Files

1. Open File Explorer
2. Look for the mounted drive (e.g., "WSA Files (X:)")
3. Browse and manage files like any other drive

### Web File Manager

You can also access files via web browser:

1. Open `http://127.0.0.1:8088` in your browser
2. Use the web file manager interface
3. Upload, download, and manage files

### Root File System (Root Mode)

In root mode, the root filesystem is mounted at:
```
X:\root\
```

User storage is at:
```
X:\files\
```

## Configuration

### Config File

The WebDAV server configuration is at:
```
/data/data/com.wsa.webdav/files/config.json
```

### Default Settings

| Setting | Value |
|:--------|:------|
| Port | 8088 |
| Host | 127.0.0.1 |
| Root Access | true |
| Anonymous Access | true |
| Max Connections | 50 |

### Changing the Port

1. Edit `config.json` in WSA
2. Restart the WebDAV server
3. Update the port forward:
   ```cmd
   adb forward tcp:NEW_PORT tcp:NEW_PORT
   ```
4. Remount with the new port

## Troubleshooting

### Drive Won't Mount

1. Ensure WSA is running
2. Check ADB connection: `adb devices`
3. Verify WebDAV server is running: `curl http://127.0.0.1:8088`
4. Check WebClient service: `services.msc` → WebDAV Redirector

### "Network Error" in Browser

1. Check if port 8088 is forwarded: `adb forward --list`
2. Re-establish forwarding: `adb forward tcp:8088 tcp:8088`
3. Check firewall settings

### Slow Performance

1. Use USB instead of WiFi ADB
2. Reduce the number of concurrent connections
3. Close other network-intensive applications

### Root Access Denied

1. Ensure Magisk is installed in WSA
2. Open Magisk app and grant root to WSA WebDAV
3. Check `su -c whoami` returns "root"

### Files Not Updating

1. The WebDAV server may need a restart
2. Disconnect and remount the drive:
   ```cmd
   net use X: /delete
   net use X: http://127.0.0.1:8088/files/ /persistent:yes
   ```

## Stopping File Sharing

To stop file sharing:

1. Open WSA Installer → Advanced
2. Toggle file sharing off

Or manually:
```cmd
net use X: /delete
adb shell am broadcast -a com.wsa.webdav.STOP
adb forward --remove tcp:8088
```
