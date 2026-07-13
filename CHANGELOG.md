# Changelog

All notable changes to WSA Installer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-07-12

### Added
- File sharing via WebDAV (user and root modes)
- Drive mounting as Windows network drives
- Advanced settings page with file sharing controls
- Auto-repair toggle in advanced settings
- Background service GUI monitor dialog
- 30-chunk parallel download for self-updates
- Download resume support across sessions
- Drive letter selection for WebDAV mounts
- Custom drive labels and icons via registry

### Changed
- Upgraded to Python 3.14
- Improved download speed with parallel chunks
- Enhanced error handling with retry logic
- Updated NSIS installer with maintenance mode
- Improved glass transparency system

### Fixed
- WsaClient.exe crash on Windows 10 (WSAPatch)
- ADB authorization popup automation reliability
- Service auto-restart on failure
- Single-instance lock release on uninstall

## [1.1.0] - 2026-06-01

### Added
- Background service (`WSABackgroundService`)
- Windows Service integration with auto-restart
- Remote configuration via Rust security gateway
- Self-update mechanism
- Repair flow from Windows Settings
- YouTube channel subscription on completion

### Changed
- Improved system detection (5 methods)
- Enhanced Play Store patching with 7-phase flow
- Better progress tracking with phase headers

### Fixed
- Virtualization detection on certain hardware
- Hyper-V enabling on Windows 10

## [1.0.0] - 2026-05-01

### Added
- Initial release
- 5-step installation wizard
- System detection (virtualization, Hyper-V, VMP, WSL)
- WSA download with parallel chunks
- 7z extraction with nested folder detection
- 6-phase WSA installation
- 7-phase Play Store integration
- ADB authorization automation
- Glass transparency UI
- NSIS professional installer
- Silent installation support
- Single-instance enforcement
