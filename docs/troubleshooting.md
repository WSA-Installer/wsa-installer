# Troubleshooting Guide

This guide covers common issues and their solutions when using WSA Installer.

## Table of Contents

- [Installation Issues](#installation-issues)
- [WSA Issues](#wsa-issues)
- [Play Store Issues](#play-store-issues)
- [Background Service Issues](#background-service-issues)
- [File Sharing Issues](#file-sharing-issues)
- [Update Issues](#update-issues)
- [UI Issues](#ui-issues)

---

## Installation Issues

### "Virtualization not detected"

**Symptoms:** The system check fails to detect virtualization support.

**Solutions:**

1. **Enable in BIOS/UEFI:**
   - Restart your computer
   - Enter BIOS/UEFI (usually F2, F10, or Del)
   - Find "Virtualization Technology" or "Intel VT-x" / "AMD-V"
   - Enable it
   - Save and exit

2. **Check Windows Features:**
   ```cmd
   dism /online /get-features /format:table | findstr Hyper
   ```

3. **Enable Hyper-V:**
   ```cmd
   dism.exe /Online /Enable-Feature /FeatureName:Microsoft-Hyper-V /All
   ```

### "Hyper-V won't enable"

**Solutions:**

1. Check if WSL2 is installed:
   ```cmd
   wsl --status
   ```

2. Set hypervisor launch type:
   ```cmd
   bcdedit /set hypervisorlaunchtype auto
   ```

3. Restart your computer

### "Installation fails with error"

**Solutions:**

1. Run as administrator
2. Check available disk space (10 GB minimum)
3. Temporarily disable antivirus
4. Check Windows Event Viewer for errors

### "Download fails or is slow"

**Solutions:**

1. Check internet connection
2. Try downloading `bundle.wsa` manually
3. Place `bundle.wsa` in the same folder as the installer
4. Check firewall settings

---

## WSA Issues

### "WSA won't start"

**Solutions:**

1. Restart your computer
2. Check Windows Features are enabled
3. Run the installer's Repair feature
4. Manually start WSA:
   ```cmd
   wsa://system
   ```

### "WSA crashes immediately"

**Solutions:**

1. Check for Windows updates
2. Run the installer's Repair feature
3. Clear WSA data:
   - Settings → Apps → WSA → Advanced options → Reset
4. Reinstall WSA

### "WSA is very slow"

**Solutions:**

1. Ensure you have enough RAM (8 GB minimum, 16 GB recommended)
2. Close unnecessary applications
3. Use an SSD instead of HDD
4. Check Task Manager for resource usage

### "WSA settings won't open"

**Solutions:**

1. Try: `wsa://settings`
2. Restart WSA: `taskkill /F /IM WsaClient.exe`
3. Run the installer's Repair feature

### "Developer Mode is disabled"

**Solutions:**

1. Open WSA Settings
2. Go to Developer tab
3. Enable Developer Mode
4. If the toggle won't stick, the installer can patch `settings.dat`

---

## Play Store Issues

### "Play Store not appearing"

**Solutions:**

1. Ensure you selected "Add Play Store" during installation
2. Check if the Play Store package is installed:
   ```cmd
   adb shell pm list packages com.android.vending
   ```
3. Run the installer's Repair feature and re-add Play Store

### "Play Store won't open"

**Solutions:**

1. Clear Play Store cache:
   ```cmd
   adb shell pm clear com.android.vending
   ```
2. Clear Google Play Services cache:
   ```cmd
   adb shell pm clear com.google.android.gms
   ```
3. Restart WSA

### "Can't sign in to Google account"

**Solutions:**

1. Ensure date and time are correct
2. Check internet connection
3. Try a different Google account
4. Clear Google account data and retry

### "Apps won't install from Play Store"

**Solutions:**

1. Check available storage in WSA
2. Clear Play Store cache
3. Check internet connection
4. Try installing a different app

### "ADB authorization popup not appearing"

**Solutions:**

1. Ensure Developer Mode is enabled
2. Disconnect and reconnect ADB:
   ```cmd
   adb disconnect
   adb connect 127.0.0.1:58526
   ```
3. Manually check the WSA window for the popup

---

## Background Service Issues

### "Service won't start"

**Solutions:**

1. Run as administrator:
   ```cmd
   WSA Installer.exe --install-service
   ```

2. Check service status:
   ```cmd
   sc query WSABackgroundService
   ```

3. Check Windows Event Viewer for errors

### "Service keeps restarting"

**Solutions:**

1. Check the service logs
2. Ensure WSA is installed correctly
3. Reinstall the service:
   ```cmd
   WSA Installer.exe --uninstall-service
   WSA Installer.exe --install-service
   ```

### "Service not monitoring WSA"

**Solutions:**

1. Ensure the service is running
2. Check that WSA is installed
3. Restart the service:
   ```cmd
   sc stop WSABackgroundService
   sc start WSABackgroundService
   ```

---

## File Sharing Issues

### "Drive won't mount"

**Solutions:**

1. Ensure WSA is running
2. Check ADB connection:
   ```cmd
   adb devices
   ```
3. Verify WebDAV server is running:
   ```cmd
   curl http://127.0.0.1:8088
   ```
4. Check WebClient service:
   - Open `services.msc`
   - Find "WebDAV Redirector"
   - Ensure it's running

### "Permission denied accessing drive"

**Solutions:**

1. Ensure you have the correct mode (User vs Root)
2. Check folder permissions in WSA
3. Try accessing a different folder

### "Slow file transfer"

**Solutions:**

1. Use USB instead of WiFi for ADB
2. Transfer large files as a batch
3. Close other network-intensive applications

### "Drive disconnects randomly"

**Solutions:**

1. Check network stability
2. Ensure WSA stays running
3. Disable power saving for USB devices
4. Check for conflicts with other network drives

---

## Update Issues

### "Update fails to download"

**Solutions:**

1. Check internet connection
2. Try downloading manually from GitHub Releases
3. Run the installer as administrator

### "Update fails to install"

**Solutions:**

1. Run as administrator
2. Close all WSA Installer instances
3. Stop the background service temporarily
4. Try the manual update method

---

## UI Issues

### "Window is transparent/invisible"

**Solutions:**

1. Press Alt+Tab to find the window
2. Adjust the glass transparency slider
3. Check if the Flet client is properly patched

### "Buttons not responding"

**Solutions:**

1. Wait a few seconds — the UI may be loading
2. Press Alt+F4 to close and restart
3. Check Task Manager for unresponsive processes

### "UI looks broken or misaligned"

**Solutions:**

1. Check display scaling settings (100% recommended)
2. Update display drivers
3. Try a different display resolution

---

## Getting More Help

If your issue isn't covered here:

1. Check the [GitHub Issues](https://github.com/WSA-Installer/wsa-installer/issues) for similar problems
2. Open a new [Bug Report](https://github.com/WSA-Installer/wsa-installer/issues/new?template=bug_report.yml)
3. Join the [GitHub Discussions](https://github.com/WSA-Installer/wsa-installer/discussions)
4. Watch video tutorials on [YouTube](https://www.youtube.com/@AT_Tech_Zone)

## Log Files

When reporting issues, include relevant logs:

- **Activity Log:** `wsa_activity.log`
- **Debug Log:** `debug.log`
- **UI Log Box:** Available in all installer dialogs
