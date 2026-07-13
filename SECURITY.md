# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability within WSA Installer, please send an email to the project maintainers. All security vulnerabilities will be promptly addressed.

**Please do NOT report security vulnerabilities through public GitHub issues.**

### What to Include

When reporting a vulnerability, please include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 1 week
- **Fix and release**: Depends on severity, typically within 2 weeks

## Security Architecture

WSA Installer implements multiple security layers:

### Layer 1: Rust Security Gateway (`widget_ui.pyd`)

- Zero-trust configuration parsing
- Signature verification for remote config
- Encrypted configuration handling
- Hash-based deduplication to prevent redundant updates

### Layer 2: Instance Enforcement

- Socket-based single instance lock prevents multiple installer copies
- Port-based process detection for conflict resolution

### Layer 3: Windows Service

- `WSABackgroundService` runs as SYSTEM-level Windows Service
- Auto-restart on failure with configurable retry logic
- User session process spawning via `CreateProcessAsUserW`

### Layer 4: Source Protection

- Nuitka compilation (`app.py` → `app.pyd`) for source code protection
- PyInstaller bundling with binary obfuscation
- Embedded Python 3.14 runtime isolation

### Layer 5: Privilege Management

- UAC elevation for system modifications
- Administrator privilege validation before operations
- Input blocking during sensitive automation sequences

## Best Practices for Users

1. **Download only from official sources** — Use the official GitHub releases
2. **Run as administrator** — Required for WSA installation and system modifications
3. **Keep updated** — Use the built-in self-update feature
4. **Verify checksums** — Compare downloaded file hashes when possible
5. **Review logs** — Check `wsa_activity.log` for suspicious activity

## Security Updates

Security updates will be released as patches to the current version. Users are encouraged to enable automatic updates or check the [Releases](https://github.com/WSA-Installer/wsa-installer/releases) page regularly.

## Scope

This security policy applies to:

- The WSA Installer application (`WSA Installer.exe`)
- The NSIS installer (`WSA_Installer_Setup.exe`)
- The background service (`WSABackgroundService`)
- The native modules (`widget_ui.pyd`, `playstore_patcher_mem.pyd`)

It does NOT apply to:

- Third-party software (ADB, Python, etc.)
- Windows Subsystem for Android itself
- Applications installed within WSA

## Acknowledgments

We appreciate the security research community and responsible disclosure of vulnerabilities.
