# Repair Guide

WSA Installer includes a built-in repair feature that can fix common WSA issues without requiring a complete reinstall.

## When to Use Repair

Use the repair feature when:

- WSA won't start
- WSA crashes frequently
- Play Store is not working
- WSA settings are corrupted
- After a Windows update breaks WSA
- Background service is not running

## How to Repair

### Method 1: From Windows Settings

1. Open **Settings** → **Apps** → **Installed apps**
2. Find **WSA Installer** in the list
3. Click the three dots (**) → **Modify**
4. Select **Repair / Reinstall**
5. Follow the repair wizard

### Method 2: From WSA Installer

1. Open WSA Installer
2. Click **Advanced** in the sidebar
3. Click **Repair WSA** button
4. Follow the repair wizard

### Method 3: Command Line

```cmd
WSA_Installer.exe --repair-wsa
```

## Repair Process

The repair wizard performs 4 steps:

### Step 1: Detect WSA

The installer runs `Get-AppxPackage` via PowerShell to find the WSA installation location. If WSA is not found, the repair cannot proceed.

### Step 2: Stop WSA Processes

All WSA-related processes are terminated:

- `WsaClient.exe`
- `WsaSvc`
- `vmmem`
- `WsaService`
- `adb.exe`

This ensures files are not locked during repair.

### Step 3: Backup User Data

Your WSA data (installed apps, settings) is backed up to a safe location. This backup is used to restore your data after reinstall.

The backup includes:
- App data
- User settings
- Developer Mode configuration

### Step 4: Reinstall WSA

1. The existing WSA installation is removed
2. A fresh WSA installation is created
3. Your backed-up data is restored
4. Play Store is re-patched if previously installed
5. Background service is restarted

## Backup Location

Your WSA backup is stored at:

```
%LOCALAPPDATA%\WSA Installer\backup\
```

### Restore from Backup

If you need to manually restore from backup:

1. Stop WSA: `taskkill /F /IM WsaClient.exe`
2. Copy the backup contents to the WSA data folder
3. Restart WSA

## Repair vs Reinstall

| Feature | Repair | Reinstall |
|:--------|:-------|:----------|
| Preserves app data | Yes | No |
| Preserves Play Store | Yes | No |
| Fixes corrupted files | Yes | Yes |
| Time required | 2-5 minutes | 10-15 minutes |
| Requires re-download | No | Yes |

## Troubleshooting Repair

### Repair Fails

1. Try running as administrator
2. Ensure no other WSA processes are running
3. Check that you have enough disk space
4. Try the manual kill steps below, then retry repair

### Manual WSA Kill

If WSA won't stop:

```cmd
taskkill /F /IM WsaService.exe
taskkill /F /IM WsaClient.exe
taskkill /F /IM WsaSettings.exe
```

### Backup Corrupted

If the backup is corrupted, the repair will skip the restore step. You'll need to reinstall your apps manually.

### Repair Stuck

If the repair process appears stuck:

1. Wait 5 minutes — some operations take time
2. Check the log output in the UI
3. If still stuck, force-close and retry
4. As a last resort, use the full uninstall and reinstall
