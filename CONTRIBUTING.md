# Contributing to WSA Installer

Thank you for your interest in contributing to WSA Installer! This document provides guidelines and information for contributors.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone. Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check [existing issues](https://github.com/WSA-Installer/wsa-installer/issues) to avoid duplicates.

When creating a bug report, include:

- **Clear title** — Describe the issue concisely
- **WSA Installer version** — Found in the About section
- **Windows version** — e.g., Windows 11 23H2
- **Steps to reproduce** — Detailed steps to trigger the bug
- **Expected behavior** — What you expected to happen
- **Actual behavior** — What actually happened
- **Logs** — Relevant log output from `wsa_activity.log` or the UI log

### Suggesting Features

Feature suggestions are welcome! Please provide:

- **Problem statement** — What problem does this solve?
- **Proposed solution** — How should it work?
- **Alternatives considered** — Other approaches you thought about
- **Component** — Which part of the installer does this affect?

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Test thoroughly on Windows 10 and/or Windows 11
5. Commit with a descriptive message
6. Push to your fork
7. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.14
- Windows 10/11
- Administrator privileges (for testing)
- Git

### Getting Started

```bash
# Clone the repository
git clone https://github.com/WSA-Installer/wsa-installer.git
cd wsa-installer

# Run the development launcher
run.bat
```

The `run.bat` script will:
1. Create a Python virtual environment if it doesn't exist
2. Install all dependencies from `requirements.txt`
3. Launch the application

### Project Structure

```
wsa-installer/
├── src/
│   ├── app.py                    # Main application (~11K lines)
│   ├── run.py                    # Entry point
│   ├── WSARepair.py              # Windows Settings proxy
│   └── patch_flet.py             # Flet client patcher
├── assets/                       # Runtime resources
├── native/                       # Rust native modules
├── emb_py/                       # Embedded Python 3.14
├── build/                        # Build scripts
├── docs/                         # Documentation
└── tests/                        # Tests
```

### Key Files

- **`app.py`** — The main application file containing the Flet GUI, installer logic, background service, repair, update, and file sharing functionality
- **`WSARepair.py`** — Proxy for Windows Settings Repair/Uninstall buttons
- **`build.bat`** — Primary build pipeline (Nuitka → PyInstaller → NSIS)

## Code Style

### Python

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Use meaningful variable and function names
- Add docstrings for public functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>

Types:
  feat     - New feature
  fix      - Bug fix
  docs     - Documentation changes
  style    - Code style changes (formatting, etc.)
  refactor - Code refactoring
  perf     - Performance improvements
  test     - Adding or updating tests
  build    - Build system changes
  ci       - CI/CD changes
  chore    - Maintenance tasks

Scopes:
  installer  - Main installer
  service    - Background service
  webdav     - File sharing
  ui         - User interface
  build      - Build pipeline
  docs       - Documentation
```

Examples:
```
feat(installer): add parallel chunked download with resume
fix(service): resolve WSA port detection timeout
docs(readme): update installation guide
build(nsis): add silent install support
```

### Branch Naming

- `feature/description` — New features
- `fix/description` — Bug fixes
- `docs/description` — Documentation changes
- `release/version` — Release preparation

## Testing

### Manual Testing

Before submitting a PR, test the following flows:

1. **Fresh Install** — Install WSA on a clean system
2. **Play Store** — Verify Play Store integration works
3. **Repair** — Test the repair flow from Windows Settings
4. **Uninstall** — Verify complete uninstallation
5. **Update** — Test the self-update mechanism
6. **File Sharing** — Test WebDAV drive mounting

### Test Checklist

- [ ] Tested on Windows 10 (build 19041+)
- [ ] Tested on Windows 11
- [ ] Tested with Play Store installation
- [ ] Tested repair flow
- [ ] Tested uninstall flow
- [ ] No new warnings or errors
- [ ] UI renders correctly at different DPI settings

## Building

### Development Build

```cmd
run.bat
```

### Release Build

```cmd
build.bat
```

This will produce `dist/WSA_Installer_Setup.exe`.

### Build Requirements

- Python 3.14 with pip
- Nuitka (`pip install nuitka`)
- PyInstaller (`pip install pyinstaller`)
- NSIS ([nsis.sourceforge.io](https://nsis.sourceforge.io))

## Documentation

- Update `docs/` if adding new features
- Update `README.md` if changing public API or behavior
- Add entries to `CHANGELOG.md` for notable changes
- Update `ROADMAP.md` if adding planned features

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

## Questions?

If you have questions about contributing, feel free to:

- Open a [Discussion](https://github.com/WSA-Installer/wsa-installer/discussions)
- Contact via [YouTube](https://www.youtube.com/@AT_Tech_Zone)

Thank you for contributing to WSA Installer!
