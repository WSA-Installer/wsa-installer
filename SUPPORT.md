# Support

## Getting Help

If you need help with WSA Installer, here are the available support channels:

### Documentation

- [Installation Guide](docs/installation.md) — Step-by-step installation instructions
- [Troubleshooting Guide](docs/troubleshooting.md) — Solutions to common issues
- [CLI Reference](docs/cli-reference.md) — Command-line options
- [Architecture Guide](docs/architecture.md) — Technical overview

### Community Support

| Channel | Link | Best For |
|:--------|:-----|:---------|
| GitHub Issues | [Report a Bug](https://github.com/WSA-Installer/wsa-installer/issues/new?template=bug_report.yml) | Bug reports and issues |
| GitHub Discussions | [Ask a Question](https://github.com/WSA-Installer/wsa-installer/discussions) | Questions and general help |
| YouTube | [@AT_Tech_Zone](https://www.youtube.com/@AT_Tech_Zone) | Video tutorials and guides |

### Contact

- **YouTube**: [@AT_Tech_Zone](https://www.youtube.com/@AT_Tech_Zone)
- **Buy Me a Coffee**: [mrcyberdev](https://buymeacoffee.com/mrcyberdev)

## Frequently Asked Questions

### General

**Q: What is WSA Installer?**
A: WSA Installer is a tool that automates the installation of Windows Subsystem for Android (WSA) with Google Play Store on Windows 10 and Windows 11.

**Q: Is WSA Installer free?**
A: Yes, WSA Installer is free and open-source under the MIT License.

**Q: Does WSA Installer work on Windows 10?**
A: Yes, WSA Installer supports Windows 10 build 19041 and later.

### Installation

**Q: Do I need to be an administrator?**
A: Yes, WSA Installer requires administrator privileges to install WSA and configure Windows features.

**Q: Can I install WSA without Play Store?**
A: Yes, the installer offers both options: WSA only or WSA with Play Store.

**Q: How long does installation take?**
A: Installation typically takes 5-15 minutes depending on your internet speed and system performance.

**Q: What is bundle.wsa?**
A: `bundle.wsa` is a pre-packaged archive containing WSA packages. It's optional — the installer can download packages directly from GitHub.

### Troubleshooting

**Q: Virtualization is not detected**
A: Enable Intel VT-x or AMD-V in your BIOS/UEFI settings. Check your motherboard documentation for instructions.

**Q: WSA won't start after installation**
A: Try restarting your computer. If the issue persists, use the Repair feature from Windows Settings → Apps → WSA Installer → Modify → Repair.

**Q: Play Store is not working**
A: Ensure Developer Mode is enabled in WSA Settings. Try disconnecting and reconnecting ADB. Check the installer logs for errors.

**Q: How do I uninstall WSA?**
A: Use the WSA Installer's built-in uninstaller, or go to Windows Settings → Apps → WSA Installer → Uninstall.

### Advanced

**Q: Can I install multiple WSA versions?**
A: Not currently. This is a planned feature for a future release.

**Q: How do I use the background service?**
A: The background service is installed automatically. It monitors WSA status and manages the Play Store SDK. You can manage it via Windows Services (`WSABackgroundService`).

**Q: Can I use WSA Installer in enterprise environments?**
A: Yes, WSA Installer supports silent installation via `/S` flag, making it suitable for enterprise deployment.

## Feature Requests

Have an idea for a new feature? [Open a feature request](https://github.com/WSA-Installer/wsa-installer/issues/new?template=feature_request.yml) on GitHub.

## Contributing

Want to help improve WSA Installer? See our [Contributing Guide](CONTRIBUTING.md) for details.
