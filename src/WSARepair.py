"""WSARepair.exe --- proxy for Windows Settings Repair/Uninstall buttons."""
import sys, os, subprocess, time, winreg

def log(msg):
    print(f"""[WSARepair {time.strftime("%H:%M:%S")}] {msg}""", flush=True)

def _find_installer():
    log("Looking for WSA Installer...")

    # Method 1: NSIS uninstaller registry InstallLocation + DisplayIcon
    nsus_key = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\WSAInstaller"
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, nsus_key, 0,
                             winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        install_dir, _ = winreg.QueryValueEx(key, "InstallLocation")
        winreg.CloseKey(key)
        if install_dir:
            exe = os.path.join(install_dir, "WSA Installer.exe")
            log(f"NSIS InstallLocation: {exe}")
            if os.path.exists(exe):
                log(f"Found: {exe}"); return exe
            log("Not on disk, trying DisplayIcon...")
    except FileNotFoundError:
        log("NSIS uninstall key not found")
    except Exception as e:
        log(f"NSIS registry error: {e}")

    # Method 2: NSIS DisplayIcon
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, nsus_key, 0,
                             winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        icon_path, _ = winreg.QueryValueEx(key, "DisplayIcon")
        winreg.CloseKey(key)
        log(f"NSIS DisplayIcon: {icon_path}")
        if icon_path and os.path.exists(icon_path):
            log(f"Found: {icon_path}"); return icon_path
    except Exception as e:
        log(f"DisplayIcon error: {e}")

    # Method 3: HKLM\SOFTWARE\WSAInstaller\InstallerPath (custom, backup)
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WSAInstaller", 0,
                             winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        exe_path, _ = winreg.QueryValueEx(key, "InstallerPath")
        winreg.CloseKey(key)
        log(f"Custom registry: {exe_path}")
        if exe_path and os.path.exists(exe_path):
            log(f"Found: {exe_path}"); return exe_path
    except Exception:
        log("Custom registry key not found")

    # Method 4: Hardcoded Program Files path
    fixed = r"C:\Program Files\WSA Installer\WSA Installer.exe"
    log(f"Hardcoded: {fixed}")
    if os.path.exists(fixed):
        log(f"Found: {fixed}"); return fixed

    log("ERROR: No installer found"); return ""

def main():
    log("Started")
    log(f"Args: {sys.argv}")
    a = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    log(f"Action: {a}")
    if a not in ("repair", "uninstall"):
        log(f"Bad action: {a}"); return 1
    exe = _find_installer()
    if not exe or not os.path.exists(exe):
        log("Cannot proceed - not found"); return 1
    f = "--repair-wsa" if a == "repair" else "--uninstall"
    log(f"Launch: {exe} {f}")
    try:
        subprocess.Popen([exe, f], creationflags=subprocess.DETACHED_PROCESS,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log("Launched OK"); return 0
    except Exception as e:
        log(f"Launch failed: {e}"); return 1

if __name__ == "__main__":
    sys.exit(main())
