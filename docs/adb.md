# ADB Reference

ADB (Android Debug Bridge) is used by WSA Installer to communicate with WSA for Play Store installation and management.

## ADB in WSA Installer

WSA Installer automates ADB operations for:

- Connecting to WSA
- Authorizing USB debugging
- Installing Play Store (GApps)
- Verifying package installation
- Managing WSA developer options

## ADB Connection

### Port

WSA exposes ADB on port **58526** by default.

### Connect Command

```cmd
adb connect 127.0.0.1:58526
```

### Connection Process

WSA Installer automatically:

1. Checks if WSA is running
2. Probes port 58526
3. Connects via ADB
4. Handles authorization (if needed)

## ADB Authorization

When connecting to WSA for the first time, you'll see an "Allow USB debugging" popup.

### Automatic Authorization

WSA Installer automates this process using `pywinauto`:

1. Detects the "Allow USB debugging" window
2. Clicks "Always allow from this computer"
3. Clicks "Allow"

### Manual Authorization

If automatic authorization fails:

1. Check the WSA window for the popup
2. Check "Always allow from this computer"
3. Click "Allow"

## Common ADB Commands

### Check Connected Devices

```cmd
adb devices
```

### Install APK

```cmd
adb install -r package.apk
```

### Uninstall Package

```cmd
adb uninstall com.package.name
```

### List Installed Packages

```cmd
adb shell pm list packages
```

### Check Specific Package

```cmd
adb shell pm list packages com.android.vending
```

### Start Activity

```cmd
adb shell am start -n com.package/.Activity
```

### Send Broadcast

```cmd
adb shell am broadcast -a com.action.NAME
```

## Troubleshooting ADB

### "Device unauthorized"

1. Check the WSA window for the authorization popup
2. Enable Developer Mode in WSA Settings
3. Disconnect and reconnect ADB:
   ```cmd
   adb disconnect
   adb connect 127.0.0.1:58526
   ```

### "Connection refused"

1. Ensure WSA is running
2. Check that Developer Mode is enabled
3. Restart WSA:
   ```cmd
   taskkill /F /IM WsaClient.exe
   wsa://system
   ```
4. Wait 30 seconds, then retry

### "Device offline"

1. Disconnect ADB: `adb disconnect`
2. Kill ADB server: `adb kill-server`
3. Restart ADB server: `adb start-server`
4. Reconnect: `adb connect 127.0.0.1:58526`

### Port Changed

If WSA uses a different port:

1. Check WSA Settings → Developer → Wireless debugging
2. Note the port number
3. Connect with the correct port:
   ```cmd
   adb connect 127.0.0.1:PORT_NUMBER
   ```

### Multiple ADB Instances

If you have multiple ADB installations:

1. Use the full path to the WSA Installer's ADB:
   ```
   assets\adb.exe connect 127.0.0.1:58526
   ```

## ADB in WSA WebDev

The WSA WebDev project uses ADB for server control:

```bash
# Start WebDAV server
adb shell am broadcast -a com.wsa.webdav.START

# Stop WebDAV server
adb shell am broadcast -a com.wsa.webdav.STOP

# Check status
adb shell am broadcast -a com.wsa.webdav.STATUS
```

See the [WebDAV documentation](webdav.md) for details.
