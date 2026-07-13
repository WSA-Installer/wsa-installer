# Uninstall Guide

WSA Installer provides a complete uninstallation process that removes WSA, the background service, shortcuts, and registry entries.

## How to Uninstall

### Method 1: From Windows Settings

1. Open **Settings** → **Apps** → **Installed apps**
2. Find **WSA Installer** in the list
3. Click the three dots (**) → **Uninstall**
4. Follow the uninstall wizard

### Method 2: From WSA Installer

1. Open WSA Installer
2. Click **Advanced** in the sidebar
3. Click **Uninstall WSA** button
4. Follow the uninstall wizard

### Method 3: Command Line

```cmd
WSAInstaller.exe --uninstall
```

### Method 4: From Start Menu

1. Open the Start Menu
2. Find **WSA Installer** folder
3. Click **Uninstall**

## Uninstall Process

The uninstall wizard performs 7 steps:

### Step 1: Detect WSA

Locates the WSA installation using `Get-AppxPackage`.

### Step 2: Stop WSA Processes

Terminates all WSA-related processes:
- `WsaClient.exe`
- `WsaService.exe`
- `WsaSvc`
- `vmmem`
- `adb.exe`

### Step 3: Backup User Data (Optional)

You can choose to back up your WSA data before uninstalling. This preserves:
- Installed apps
- App data
- Settings

### Step 4: Remove Appx Package

Runs `Remove-AppxPackage` to remove WSA from Windows. If this fails, it retries with `-AllUsers`.

### Step 5: Delete Installation Files

Removes the WSA installation directory and all associated files.

### Step 6: Remove Background Service

Stops and deletes `WSABackgroundService` from Windows Services.

### Step 7: Cleanup

Final cleanup of:
- Desktop shortcuts
- Start Menu shortcuts
- Registry entries
- Temporary files

## What Gets Removed

| Component | Removed? |
|:----------|:---------|
| WSA installation | Yes |
| WSA app data | Optional (backup available) |
| Background service | Yes |
| Desktop shortcuts | Yes |
| Start Menu shortcuts | Yes |
| Registry entries | Yes |
| WSA Installer | Yes |
| Downloaded bundles | No (preserved for reinstall) |

## Preserved Data

The following data is NOT removed during uninstall:

- Downloaded `bundle.wsa` files
- WSA backup (if created)
- Activity logs (`wsa_activity.log`)

## Silent Uninstall

For automated uninstall:

```cmd
Uninstall.exe /S
```

## Canceling Uninstall

The uninstall wizard includes a confirmation step with a countdown timer. You must:

1. Check the confirmation checkbox
2. Wait 3 seconds
3. Click **Confirm Uninstall**

You can cancel at any time before confirming. If you cancel after confirmation has started, the uninstall will stop at the current step.

## Troubleshooting

### Uninstall Fails

1. Try running as administrator
2. Ensure no other applications are using WSA files
3. Manually stop the service: `sc stop WSABackgroundService`
4. Manually kill processes: `taskkill /F /IM WsaClient.exe`
5. Retry uninstall

### Files Remain After Uninstall

If some files remain after uninstall:

1. Restart your computer
2. Navigate to the installation directory
3. Delete remaining files manually
4. Remove the directory

### Service Won't Delete

If `WSABackgroundService` won't delete:

```cmd
sc stop WSABackgroundService
sc delete WSABackgroundService
```

Then retry the uninstall.
