# Embedded Tools

Source code for all native modules and tools embedded in WSA Installer.

## Tools

### 1. ApkIconShlExt (C++)

Windows Shell Extension that displays per-file APK icons in Explorer.

| File | Description |
|------|-------------|
| `ApkIconShlExt.cpp` | Main COM server implementation (IExtractIconW, IThumbnailProvider) |
| `ApkIconShlExt.def` | Module definition for DLL exports |
| `ApkIconShlExt.rc` | Resource file |
| `build_shell_ext.bat` | Build script using MSVC |
| `default_apk.ico` | Default icon for APK files |
| `register.reg` | Registry entries for registration |
| `defaulticon.reg` | Default icon registry entries |

**Build Requirements:**
- MSVC (Visual Studio Build Tools)
- Windows SDK

**Build:**
```cmd
build_shell_ext.bat
```

---

### 2. WSA Net Provider (Rust)

Network provider for UNC-to-WebDAV translation and WSA boot initialization.

| File | Description |
|------|-------------|
| `src/lib.rs` | Main implementation (WSA boot, ADB connect, WebDAV start) |
| `Cargo.toml` | Rust package manifest |
| `build.rs` | Build script |
| `wsa_init.py` | Python wrapper for WSA initialization |
| `wsa_init.pyi` | Type stubs for Python |

**Build Requirements:**
- Rust toolchain
- Python 3.14

**Build:**
```cmd
cargo build --release
```

**Output:**
- `wsa_init.pyd` — Python extension module
- `wsa_net_provider.dll` — Network provider DLL

---

### 3. aapt++ (Rust)

Universal Android Package Tool — a production-ready AAPT replacement.

| Crate | Description |
|-------|-------------|
| `aaptpp-core` | Core parsing and extraction logic |
| `aaptpp-ffi` | C FFI bindings for cross-language use |
| `aaptpp-python` | Python bindings via PyO3 |
| `aaptpp-cli` | Command-line interface |
| `assets/` | Test assets and resources |

**Build Requirements:**
- Rust toolchain
- Python 3.14 (for Python bindings)

**Build:**
```cmd
cargo build --release
```

**Output:**
- `aaptpp.exe` — CLI tool
- `aaptpp.pyd` — Python extension module

---

## Integration

These tools are compiled and placed in the `assets/` folder of the WSA Installer distribution:

```
assets/
├── ApkIconShlExt.dll    ← from apk-icon-shl-ext/
├── wsa_init.pyd         ← from wsa-net-provider/
├── wsa_net_provider.dll ← from wsa-net-provider/
└── aaptpp.exe           ← from aaptpp/
```

## License

MIT License — see [LICENSE](../LICENSE) for details.
