import subprocess, time, os, socket, ctypes, sys


def _read_cfg(path):
    cfg = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    cfg[k.strip()] = v.strip()
    except Exception:
        pass
    return cfg


def _tcp_alive(host, port, timeout=2):
    try:
        s = socket.create_connection((host, port), timeout=timeout)
        s.close()
        return True
    except Exception:
        return False


def _run(cmd, timeout=15):
    try:
        return subprocess.run(
            cmd, capture_output=True, timeout=timeout,
            creationflags=0x08000000,
        )
    except Exception:
        return None


def _acquire_lock(lock_path):
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC)
        import msvcrt
        msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        return fd
    except Exception:
        return None


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    cfg = _read_cfg(os.path.join(base, "wsa_init.cfg"))

    adb_port = int(cfg.get("adb_port", "58526"))
    webdav_port = int(cfg.get("webdav_port", "8088"))
    wsa_boot_timeout = int(cfg.get("wsa_boot_timeout", "30"))
    adb_connect_delay = int(cfg.get("adb_connect_delay", "2"))
    webdav_start_delay = int(cfg.get("webdav_start_delay", "3"))
    wsa_package = cfg.get("wsa_package", "com.wsa.webdav")

    adb = os.path.join(base, "adb.exe")
    apk = os.path.join(base, "wsa-webdav.apk")
    dev = f"127.0.0.1:{adb_port}"

    if _tcp_alive("127.0.0.1", webdav_port):
        return

    lock_path = os.path.join(os.environ.get("TEMP", "C:\\Windows\\Temp"), "wsa_init.lock")
    lock = _acquire_lock(lock_path)
    try:
        if _tcp_alive("127.0.0.1", webdav_port):
            return

        _run(["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command",
              "Start-Process 'wsa://'"])
        for _ in range(wsa_boot_timeout):
            time.sleep(1)
            if _tcp_alive("127.0.0.1", adb_port):
                break

        time.sleep(adb_connect_delay)
        _run([adb, "connect", dev])
        time.sleep(adb_connect_delay)

        r = _run([adb, "-s", dev, "shell", "pm", "list", "packages", wsa_package], timeout=10)
        output = (r.stdout + r.stderr) if r else b""
        if wsa_package.encode() not in output:
            _run([adb, "-s", dev, "install", "-r", apk], timeout=30)

        _run([adb, "-s", dev, "shell", "am", "start", "-n",
              f"{wsa_package}/.MainActivity"])
        time.sleep(webdav_start_delay)

        for _ in range(5):
            r = _run([adb, "-s", dev, "shell", "pidof", wsa_package], timeout=5)
            if r and r.stdout.strip().isdigit():
                break
            time.sleep(2)

        _run([adb, "-s", dev, "forward", f"tcp:{webdav_port}", f"tcp:{webdav_port}"])
        time.sleep(2)

        for _ in range(10):
            if _tcp_alive("127.0.0.1", webdav_port):
                break
            time.sleep(1)
    finally:
        if lock is not None:
            try:
                import msvcrt
                msvcrt.locking(lock, msvcrt.LK_UNLCK, 1)
            except Exception:
                pass
            try:
                os.close(lock)
            except Exception:
                pass


if __name__ == "__main__":
    main()
