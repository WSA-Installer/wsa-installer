#![windows_subsystem = "console"]

use rustyline::DefaultEditor;
use rustyline::error::ReadlineError;
use rustyline::history::History;

use aaptpp_core::{
    detect_file, icon::{png_to_ico, svg_to_ico, xml_to_ico, xml_to_svg},
    icon_bytes_file, manifest_text_file,
    info::{PackageInfo, ComponentDetail},
};
use clap::{Parser, Subcommand, CommandFactory};
use std::io::Write;
use std::path::Path;

fn shell_split(input: &str) -> Vec<String> {
    let mut result = Vec::new();
    let mut current = String::new();
    let mut in_quote = false;
    let mut quote_char = '"';
    for ch in input.chars() {
        if in_quote {
            if ch == quote_char {
                in_quote = false;
            } else {
                current.push(ch);
            }
        } else if ch == '"' || ch == '\'' {
            in_quote = true;
            quote_char = ch;
        } else if ch.is_whitespace() {
            if !current.is_empty() {
                result.push(std::mem::take(&mut current));
            }
        } else {
            current.push(ch);
        }
    }
    if !current.is_empty() {
        result.push(current);
    }
    result
}

fn history_path() -> std::path::PathBuf {
    let exe = std::env::current_exe().unwrap_or_else(|_| std::path::PathBuf::from("."));
    let dir = exe.parent().unwrap_or(std::path::Path::new(".")).join("aap++");
    let _ = std::fs::create_dir_all(&dir);
    dir.join("history.txt")
}

const REG_KEY: &str = r"Software\AAPT++";

fn reg_read_debug() -> bool {
    let out = std::process::Command::new("reg")
        .args(["query", &format!("HKCU\\{}", REG_KEY), "/v", "Debug", "/t", "REG_DWORD"])
        .output()
        .ok();
    if let Some(o) = out {
        let s = String::from_utf8_lossy(&o.stdout);
        // Look for "0x1" or "1" in the output
        s.contains("0x1") || s.contains("    1")
    } else {
        false
    }
}

fn reg_write_debug(enabled: bool) {
    let val = if enabled { "1" } else { "0" };
    let _ = std::process::Command::new("reg")
        .args(["add", &format!("HKCU\\{}", REG_KEY), "/v", "Debug", "/t", "REG_DWORD", "/d", val, "/f"])
        .output();
}

#[derive(Parser)]
#[command(
    name = "aaptpp",
    version,
    about = "Universal Android Package Tool — inspect APK / XAPK / APKS / AAB / OBB",
    long_about = "AAPT++ reads Android packages (APK, XAPK, APKS, APKM, AAB, OBB) and \
extracts every piece of metadata: manifest, resources, icon, signing, native libs. \
It replaces the legacy aapt.exe + manual-unzip approach."
)]
struct Cli {
    /// Output as JSON instead of human-readable text
    #[arg(long, global = true, default_value_t = false)]
    json: bool,

    /// Show extra debug information
    #[arg(long, global = true, default_value_t = false)]
    debug: bool,

    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand)]
enum Commands {
    // ─── Full report ───
    /// Full report (all metadata)
    Info { file: String },
    /// Decoded AndroidManifest as text
    Manifest { file: String },
    /// List archive entry names
    List { file: String },
    /// Detect package type
    Detect { file: String },

    // ─── Manifest identity ───
    /// Package name
    Package { file: String },
    /// Application label (resolved)
    AppName { file: String },
    /// Version code + name
    Version { file: String },
    /// Version code only
    VersionCode { file: String },
    /// Version name only
    VersionName { file: String },
    /// Split name (for split APKs)
    SplitName { file: String },

    // ─── SDK ───
    /// All SDK levels (min/target/compile/max)
    Sdk { file: String },
    /// Min SDK only
    MinSdk { file: String },
    /// Target SDK only
    TargetSdk { file: String },
    /// Max SDK only
    MaxSdk { file: String },
    /// Compile SDK only
    CompileSdk { file: String },

    // ─── Permissions ───
    /// One permission per line
    Permissions { file: String, verbose: bool },

    // ─── Components ───
    /// All components summary
    Components { file: String },
    /// Launcher activity name
    Launcher { file: String },
    /// Activities with details
    Activities { file: String, verbose: bool },
    /// Services
    Services { file: String, verbose: bool },
    /// Receivers
    Receivers { file: String, verbose: bool },
    /// Providers
    Providers { file: String, verbose: bool },

    // ─── Features & Libraries ───
    /// Uses-feature list
    Features { file: String },
    /// Uses-library list
    Libraries { file: String },

    // ─── Resources ───
    /// Resource table summary
    Resources { file: String },
    /// Supported locales
    Locales { file: String },
    /// Supported densities
    Densities { file: String },
    /// Resource configurations
    Resolutions { file: String },

    // ─── Signing ───
    /// Signing scheme summary
    Signing { file: String },
    /// Certificate details
    Certificates { file: String, verbose: bool },

    // ─── Native ───
    /// Supported ABIs
    Abis { file: String, verbose: bool },
    /// Native library details
    Native { file: String },

    // ─── Application flags ───
    /// Debuggable flag
    Debuggable { file: String },
    /// Install location
    InstallLocation { file: String },
    /// Allow backup flag
    AllowBackup { file: String },
    /// Is game flag
    IsGame { file: String },
    /// Multi arch flag
    MultiArch { file: String },
    /// Supports RTL flag
    SupportsRtl { file: String },
    /// Has code flag
    HasCode { file: String },

    // ─── Meta ───
    /// Meta-data entries
    Metadata { file: String, count: bool },
    /// OBB expansion files
    Obb { file: String },
    /// Split modules
    Splits { file: String },
    /// APK members (containers)
    Apks { file: String },
    /// Supported screens
    SupportsScreens { file: String },
    /// Original package name
    OriginalPackage { file: String },

    // ─── Icon ───
    /// Extract best icon
    Icon {
        file: String,
        #[arg(short, long)] output: Option<String>,
        #[arg(long)] ico: bool,
        #[arg(long)] round: bool,
    },
    /// Batch extract icons for multiple files (one-shot, outputs JSON)
    BatchIcons {
        files: Vec<String>,
        /// Output directory for .ico files (default: LOCALAPPDATA\\WSA_Installer\\ApkIconCache)
        #[arg(short, long)] out_dir: Option<String>,
        #[arg(long)] round: bool,
    },

    // ─── Conversion ───
    /// Convert container to standard APK
    Convert {
        file: String,
        #[arg(short, long)] output: Option<String>,
    },

    // ─── SVG / ICO conversion ───
    /// Convert Android XML vector drawable to SVG
    Svg {
        /// Input file: .xml (vector drawable) or .apk/.xapk (extracts icon)
        file: String,
        #[arg(short, long)] output: Option<String>,
        #[arg(long)] round: bool,
    },
    /// Convert SVG to multi-size ICO
    SvgIco {
        file: String,
        #[arg(short, long)] output: Option<String>,
    },
    /// Convert Android XML vector drawable to ICO (XML → PNG → ICO)
    XmlIco {
        file: String,
        #[arg(short, long)] output: Option<String>,
    },

    // ─── Debug ───
    /// Enable persistent debug logging (writes registry value)
    EnableDebug,
    /// Disable persistent debug logging
    DisableDebug,
}

fn main() {
    let cli = Cli::parse();
    let json = cli.json;
    let debug = cli.debug;

    // Eagerly extract runtime on startup
    match aaptpp_core::aapt_wrapper::extract_embedded_aapt() {
        Ok(path) => {
            if debug {
                eprintln!("Runtime extracted: {}", path.display());
            }
        }
        Err(e) => {
            eprintln!("Warning: failed to extract runtime: {}", e);
        }
    }
    // Propagate debug flag to deep code via env var
    // Debug is ON if: --debug flag OR registry value is 1
    let debug_on = debug || reg_read_debug();
    if debug_on {
        std::env::set_var("AAPT_DEBUG", "1");
    } else {
        std::env::remove_var("AAPT_DEBUG");
    }

    let command = match cli.command {
        Some(Commands::EnableDebug) => {
            reg_write_debug(true);
            println!("Debug mode ENABLED (persistent). All commands now show debug logs.");
            println!("Run 'disable-debug' to turn off.");
            return;
        }
        Some(Commands::DisableDebug) => {
            reg_write_debug(false);
            std::env::remove_var("AAPT_DEBUG");
            println!("Debug mode DISABLED.");
            return;
        }
        Some(cmd) => cmd,
        None => {
            let debug_status = if reg_read_debug() { "ON (persistent)" } else { "OFF" };
            println!("AAPT++ — Universal Android Package Tool");
            println!("Debug: {} | Type 'enable-debug'/'disable-debug' to toggle", debug_status);
            println!("Type 'help' for commands, 'exit' to quit.\n");

            let mut rl = DefaultEditor::new().expect("Failed to create readline editor");
            let hist_path = history_path();
            let _ = rl.load_history(&hist_path);
            loop {
                let line = match rl.readline("aaptpp> ") {
                    Ok(l) => l,
                    Err(ReadlineError::Interrupted) | Err(ReadlineError::Eof) => break,
                    Err(_) => break,
                };
                let line = line.trim();
                if line.is_empty() {
                    continue;
                }
                if line == "exit" || line == "quit" {
                    break;
                }
                if line == "help" {
                    Cli::command().print_help().ok();
                    println!();
                    continue;
                }
                if line == "history" {
                    let h = rl.history();
                    if h.is_empty() {
                        println!("(no history)");
                    } else {
                        for (i, entry) in h.iter().enumerate() {
                            println!("  {}: {}", i + 1, entry);
                        }
                    }
                    continue;
                }
                if line == "clear" {
                    rl.clear_history().ok();
                    let _ = std::fs::remove_file(&hist_path);
                    println!("History cleared.");
                    continue;
                }
                // !n re-runs command from history
                if let Some(n) = line.strip_prefix('!') {
                    if let Ok(idx) = n.parse::<usize>() {
                        if idx >= 1 && idx <= rl.history().len() {
                            let cmd = rl.history()[idx - 1].to_string();
                            println!("{}", cmd);
                            let _ = rl.add_history_entry(&cmd);
                            let parsed = shell_split(&cmd);
                            let args: Vec<&str> = std::iter::once("aaptpp").chain(parsed.iter().map(|s| s.as_str())).collect();
                            match Cli::try_parse_from(&args) {
                                Ok(cli2) => {
                                    let debug_on = cli2.debug || reg_read_debug();
                                    if debug_on { std::env::set_var("AAPT_DEBUG", "1"); } else { std::env::remove_var("AAPT_DEBUG"); }
                                    if let Some(cmd) = cli2.command {
                                        let r = run_command(cmd, cli2.json, debug_on);
                                        if let Err(e) = r { eprintln!("error: {}", e); }
                                    }
                                }
                                Err(e) => { eprintln!("{}", e); }
                            }
                            continue;
                        } else {
                            eprintln!("!{}: event not found", idx);
                            continue;
                        }
                    }
                }
                let _ = rl.add_history_entry(line);
                let _ = rl.save_history(&hist_path);
                let parsed = shell_split(line);
                let args: Vec<&str> = std::iter::once("aaptpp").chain(parsed.iter().map(|s| s.as_str())).collect();
                match Cli::try_parse_from(&args) {
                    Ok(cli2) => {
                        let json = cli2.json;
                        let debug = cli2.debug;
                        // Handle debug toggle commands
                        if let Some(ref cmd) = cli2.command {
                            match cmd {
                                Commands::EnableDebug => {
                                    reg_write_debug(true);
                                    std::env::set_var("AAPT_DEBUG", "1");
                                    println!("Debug mode ENABLED (persistent).");
                                    continue;
                                }
                                Commands::DisableDebug => {
                                    reg_write_debug(false);
                                    std::env::remove_var("AAPT_DEBUG");
                                    println!("Debug mode DISABLED.");
                                    continue;
                                }
                                _ => {}
                            }
                        }
                        // Merge registry + flag
                        let debug_on = debug || reg_read_debug();
                        if debug_on {
                            std::env::set_var("AAPT_DEBUG", "1");
                        } else {
                            std::env::remove_var("AAPT_DEBUG");
                        }
                        if let Some(cmd) = cli2.command {
                            let r = run_command(cmd, json, debug_on);
                            if let Err(e) = r {
                                eprintln!("error: {}", e);
                            }
                        }
                    }
                    Err(e) => {
                        eprintln!("{}", e);
                    }
                }
            }
            return;
        }
    };

    let res = run_command(command, json, debug);

    if let Err(e) = res {
        eprintln!("error: {}", e);
        std::process::exit(1);
    }
}

fn load(file: &str) -> Result<PackageInfo, String> {
    let source = aaptpp_core::select_source_apk(Path::new(file)).map_err(|e| e.to_string())?;
    aaptpp_core::pipeline::extract_metadata(&source).map_err(|e| e.to_string())
}

fn run_command(command: Commands, json: bool, debug: bool) -> Result<(), String> {
    match command {
        Commands::Info { ref file } => cmd_info(file, json, debug),
        Commands::Manifest { ref file } => cmd_manifest(file),
        Commands::List { ref file } => cmd_list(file),
        Commands::Detect { ref file } => cmd_detect(file),

        Commands::Package { ref file } => field_str(file, |i| Some(i.manifest.package.clone()), "package"),
        Commands::AppName { ref file } => field_str(file, |i| Some(i.app_name.clone()), "app_name"),
        Commands::Version { ref file } => cmd_version(file),
        Commands::VersionCode { ref file } => field_str(file, |i| i.manifest.version_code.clone(), "version_code"),
        Commands::VersionName { ref file } => field_str(file, |i| i.manifest.version_name.clone(), "version_name"),
        Commands::SplitName { ref file } => field_str(file, |i| i.manifest.split_name.clone(), "split_name"),

        Commands::Sdk { ref file } => cmd_sdk(file),
        Commands::MinSdk { ref file } => field_str(file, |i| i.sdk.min.map(|v| v.to_string()), "min_sdk"),
        Commands::TargetSdk { ref file } => field_str(file, |i| i.sdk.target.map(|v| v.to_string()), "target_sdk"),
        Commands::MaxSdk { ref file } => field_str(file, |i| i.sdk.max.map(|v| v.to_string()), "max_sdk"),
        Commands::CompileSdk { ref file } => field_str(file, |i| i.sdk.compile.map(|v| v.to_string()), "compile_sdk"),

        Commands::Permissions { ref file, verbose } => cmd_permissions(file, verbose),
        Commands::Components { ref file } => cmd_components(file),
        Commands::Launcher { ref file } => field_str(file, |i| i.launcher_activity.clone(), "launcher"),
        Commands::Activities { ref file, verbose } => cmd_list_components(file, "activity", verbose),
        Commands::Services { ref file, verbose } => cmd_list_components(file, "service", verbose),
        Commands::Receivers { ref file, verbose } => cmd_list_components(file, "receiver", verbose),
        Commands::Providers { ref file, verbose } => cmd_list_components(file, "provider", verbose),

        Commands::Features { ref file } => cmd_features(file),
        Commands::Libraries { ref file } => cmd_libraries(file),

        Commands::Resources { ref file } => cmd_resources(file),
        Commands::Locales { ref file } => cmd_locales(file),
        Commands::Densities { ref file } => cmd_densities(file),
        Commands::Resolutions { ref file } => cmd_resolutions(file),

        Commands::Signing { ref file } => cmd_signing(file),
        Commands::Certificates { ref file, verbose } => cmd_certificates(file, verbose),

        Commands::Abis { ref file, verbose } => cmd_abis(file, verbose),
        Commands::Native { ref file } => cmd_native(file),

        Commands::Debuggable { ref file } => field_str(file, |i| Some(i.application.debuggable.to_string()), "debuggable"),
        Commands::InstallLocation { ref file } => field_str(file, |i| i.manifest.install_location.clone(), "install_location"),
        Commands::AllowBackup { ref file } => field_str(file, |i| i.application.allow_backup.map(|v| v.to_string()), "allow_backup"),
        Commands::IsGame { ref file } => field_str(file, |i| i.application.is_game.map(|v| v.to_string()), "is_game"),
        Commands::MultiArch { ref file } => field_str(file, |i| i.application.multi_arch.map(|v| v.to_string()), "multi_arch"),
        Commands::SupportsRtl { ref file } => field_str(file, |i| i.application.supports_rtl.map(|v| v.to_string()), "supports_rtl"),
        Commands::HasCode { ref file } => field_str(file, |i| i.application.has_code.map(|v| v.to_string()), "has_code"),

        Commands::Metadata { ref file, count } => cmd_metadata(file, count),
        Commands::Obb { ref file } => cmd_list_str(file, |i| i.obb.clone(), "obb"),
        Commands::Splits { ref file } => cmd_list_str(file, |i| i.split_modules.clone(), "splits"),
        Commands::Apks { ref file } => cmd_list_str(file, |i| i.apk_members.clone(), "apk_members"),
        Commands::SupportsScreens { ref file } => cmd_supports_screens(file),
        Commands::OriginalPackage { ref file } => cmd_original_package(file),

        Commands::Icon { ref file, output, ico, round } => cmd_icon(file, output, ico, round, debug, json),
        Commands::BatchIcons { ref files, out_dir, round } => cmd_batch_icons(files, out_dir.as_deref(), round),
        Commands::Convert { ref file, output } => cmd_convert(file, output),
        Commands::Svg { ref file, output, round } => cmd_svg(file, output, round),
        Commands::SvgIco { ref file, output } => cmd_svg_ico(file, output),
        Commands::XmlIco { ref file, output } => cmd_xml_ico(file, output),
        Commands::EnableDebug | Commands::DisableDebug => Ok(()),
    }
}

fn field_str(
    file: &str,
    extract: impl Fn(&PackageInfo) -> Option<String>,
    field: &str,
) -> Result<(), String> {
    let info = load(file)?;
    match extract(&info) {
        Some(v) if !v.is_empty() => println!("{}", v),
        _ => { eprintln!("error: {} not found", field); std::process::exit(1); }
    }
    Ok(())
}

fn cmd_list_str(
    file: &str,
    extract: impl Fn(&PackageInfo) -> Vec<String>,
    _name: &str,
) -> Result<(), String> {
    let info = load(file)?;
    for s in extract(&info) {
        println!("{}", s);
    }
    Ok(())
}

fn comp_type(c: &ComponentDetail) -> &str {
    if c.component_type == "activity-alias" { "activity-alias" }
    else { &c.component_type }
}

// ─── info command: human-readable by default, --json for JSON ───

fn cmd_info(file: &str, json: bool, debug: bool) -> Result<(), String> {
    let info = load(file)?;

    if json {
        let j = serde_json::to_string_pretty(&info).map_err(|e| e.to_string())?;
        println!("{}", j);
        return Ok(());
    }

    // Human-readable output
    println!("=== APK Info ===");
    println!();
    println!("  File:            {}", file);
    println!("  Package:         {}", info.manifest.package);
    println!("  App:             {}", info.app_name);
    println!("  Package type:    {}", info.package_type);

    if let Some(ref v) = info.manifest.version_name {
        let code = info.manifest.version_code.as_deref().unwrap_or("");
        if code.is_empty() {
            println!("  Version:         {}", v);
        } else {
            println!("  Version:         {} ({})", v, code);
        }
    }

    println!();
    println!("  --- SDK ---");
    let min = info.sdk.min.map(|v| v.to_string()).unwrap_or_else(|| "-".into());
    let target = info.sdk.target.map(|v| v.to_string()).unwrap_or_else(|| "-".into());
    let compile = info.sdk.compile.map(|v| v.to_string()).unwrap_or_else(|| "-".into());
    let max = info.sdk.max.map(|v| v.to_string()).unwrap_or_else(|| "-".into());
    println!("  Min:             {}", min);
    println!("  Target:          {}", target);
    println!("  Compile:         {}", compile);
    println!("  Max:             {}", max);

    println!();
    println!("  --- Application ---");
    println!("  Debuggable:      {}", info.application.debuggable);
    if let Some(v) = info.application.allow_backup { println!("  Allow backup:    {}", v); }
    if let Some(v) = info.application.supports_rtl { println!("  Supports RTL:    {}", v); }
    if let Some(v) = info.application.is_game { println!("  Is game:         {}", v); }
    if let Some(ref theme) = info.application.theme { println!("  Theme:           {}", theme); }

    if let Some(ref launcher) = info.launcher_activity {
        println!();
        println!("  --- Launcher ---");
        println!("  Activity:        {}", launcher);
    }

    if !info.permissions.is_empty() {
        println!();
        println!("  --- Permissions ({}) ---", info.permissions.len());
        for p in info.permissions.iter().take(20) {
            println!("    {}", p.name);
        }
        if info.permissions.len() > 20 {
            println!("    ... and {} more", info.permissions.len() - 20);
        }
    }

    if !info.components.is_empty() {
        let mut acts = 0u32; let mut sers = 0u32; let mut recs = 0u32; let mut provs = 0u32;
        for c in &info.components {
            match c.component_type.as_str() {
                "activity" => acts += 1,
                "service" => sers += 1,
                "receiver" => recs += 1,
                "provider" => provs += 1,
                _ => {}
            }
        }
        println!();
        println!("  --- Components ---");
        println!("  Activities:      {}", acts);
        println!("  Services:        {}", sers);
        println!("  Receivers:       {}", recs);
        println!("  Providers:       {}", provs);
    }

    if !info.features.is_empty() {
        println!();
        println!("  --- Features ({}) ---", info.features.len());
        for f in info.features.iter().take(10) {
            let name = f.name.as_deref().unwrap_or("(unnamed)");
            let req = if f.required { "" } else { " (optional)" };
            println!("    {}{}", name, req);
        }
        if info.features.len() > 10 {
            println!("    ... and {} more", info.features.len() - 10);
        }
    }

    if !info.native_libs.supported_abis.is_empty() {
        println!();
        println!("  --- Native Libraries ---");
        println!("  ABIs:            {}", info.native_libs.supported_abis.join(", "));
        println!("  64-bit:          {}", info.native_libs.has_64bit);
        println!("  32-bit:          {}", info.native_libs.has_32bit);
        println!("  Total libs:      {}", info.native_libs.total_libs);
    }

    println!();
    println!("  --- Resources ---");
    println!("  Has resources:   {}", info.resources.has_resources);
    println!("  Total entries:   {}", info.resources.total_entries);
    if !info.resources.densities.is_empty() {
        println!("  Densities:       {}", info.resources.densities.join(", "));
    }

    println!();
    println!("  --- Signing ---");
    if info.signing.schemes.is_empty() {
        println!("  Schemes:         none");
    } else {
        println!("  Schemes:         {}", info.signing.schemes.join(", "));
    }
    println!("  Certificates:    {}", info.signing.certificates.len());
    for c in &info.signing.certificates {
        println!("    Subject:       {}", c.subject);
        println!("    SHA256:        {}", c.sha256);
        println!("    Expires:       {} (expired={})", c.not_after, c.expired);
    }

    if info.icon.present {
        println!();
        println!("  --- Icon ---");
        println!("  Present:         yes");
        if let Some(ref p) = info.icon.resource_path {
            println!("  Path:            {}", p);
        }
        if let Some(r) = info.icon.resource {
            println!("  Resource:        0x{:08x}", r);
        }
    }

    println!();
    println!("  --- Archive ---");
    println!("  File size:       {} bytes", info.file_size);
    if info.compressed_size > 0 {
        println!("  Compressed:      {} bytes", info.compressed_size);
    }

    if debug {
        println!();
        println!("  --- Debug ---");
        println!("  Split name:      {:?}", info.manifest.split_name);
        println!("  Config split:    {:?}", info.manifest.config_for_split);
        println!("  Install loc:     {:?}", info.manifest.install_location);
        println!("  Platform build:  {:?}", info.manifest.platform_build_version_code);
        println!("  Permissions:     {}", info.permissions.len());
        println!("  Components:      {}", info.components.len());
        println!("  Meta-data:       {}", info.meta_data.len());
        println!("  Configurations:  {}", info.resources.configurations.len());
        if !info.resources.configurations.is_empty() {
            for c in info.resources.configurations.iter().take(20) {
                println!("    {}", c);
            }
        }
        println!("  Original pkgs:   {}", info.original_packages.len());
        println!("  OBB:             {}", info.obb.len());
        println!("  Split modules:   {}", info.split_modules.len());
    }

    println!();
    Ok(())
}

fn cmd_manifest(file: &str) -> Result<(), String> {
    let text = manifest_text_file(Path::new(file)).map_err(|e| e.to_string())?;
    println!("{}", text);
    Ok(())
}

fn cmd_list(file: &str) -> Result<(), String> {
    let za = aaptpp_core::archive::ZipArchive::open_path(Path::new(file))
        .map_err(|e| e.to_string())?;
    for n in za.entry_names() {
        println!("{}", n);
    }
    Ok(())
}

fn cmd_detect(file: &str) -> Result<(), String> {
    let pt = detect_file(Path::new(file)).map_err(|e| e.to_string())?;
    println!("{}", pt.as_str());
    Ok(())
}

fn cmd_version(file: &str) -> Result<(), String> {
    let info = load(file)?;
    let name = info.manifest.version_name.clone().unwrap_or_default();
    let code = info.manifest.version_code.clone().unwrap_or_default();
    if name.is_empty() && code.is_empty() {
        eprintln!("error: version not found");
        std::process::exit(1);
    }
    let open = if !name.is_empty() && !code.is_empty() { " (" } else { "" };
    let close = if !name.is_empty() && !code.is_empty() { ")" } else { "" };
    println!("{}{}{}{}", name, open, code, close);
    Ok(())
}

fn cmd_sdk(file: &str) -> Result<(), String> {
    let info = load(file)?;
    let min = info.sdk.min.map(|v| v.to_string()).unwrap_or_else(|| "-".into());
    let target = info.sdk.target.map(|v| v.to_string()).unwrap_or_else(|| "-".into());
    let compile = info.sdk.compile.map(|v| v.to_string()).unwrap_or_else(|| "-".into());
    let max = info.sdk.max.map(|v| v.to_string()).unwrap_or_else(|| "-".into());
    println!("min {} · target {} · compile {} · max {}", min, target, compile, max);
    Ok(())
}

fn cmd_permissions(file: &str, verbose: bool) -> Result<(), String> {
    let info = load(file)?;
    if info.permissions.is_empty() {
        eprintln!("error: no permissions found");
        std::process::exit(1);
    }
    for p in &info.permissions {
        if verbose {
            let extra = if p.max_sdk_version.is_some() || p.sdk_23 {
                format!("  [maxSdk={}{}]",
                    p.max_sdk_version.map(|v| v.to_string()).unwrap_or_default(),
                    if p.sdk_23 { ",sdk23" } else { "" })
            } else { String::new() };
            println!("{}{}", p.name, extra);
        } else {
            println!("{}", p.name);
        }
    }
    Ok(())
}

fn cmd_components(file: &str) -> Result<(), String> {
    let info = load(file)?;
    let mut acts = 0u32; let mut sers = 0u32; let mut recs = 0u32; let mut provs = 0u32; let mut aliases = 0u32;
    for c in &info.components {
        match c.component_type.as_str() {
            "activity" => acts += 1,
            "service" => sers += 1,
            "receiver" => recs += 1,
            "provider" => provs += 1,
            "activity-alias" => aliases += 1,
            _ => {}
        }
    }
    println!("activities={} services={} receivers={} providers={} aliases={}",
        acts, sers, recs, provs, aliases);
    if let Some(l) = &info.launcher_activity {
        println!("launcher: {}", l);
    }
    Ok(())
}

fn cmd_list_components(file: &str, ctype: &str, verbose: bool) -> Result<(), String> {
    let info = load(file)?;
    let mut found = false;
    for c in &info.components {
        if comp_type(c) != ctype { continue; }
        found = true;
        if verbose {
            println!("{}", serde_json::to_string_pretty(c).map_err(|e| e.to_string())?);
        } else {
            let extra = if c.exported == Some(true) { " (exported)" } else if c.exported == Some(false) { " (not exported)" } else { "" };
            let if_count = c.intent_filters.len();
            let ifs = if if_count > 0 { format!(" [{} filters]", if_count) } else { String::new() };
            println!("{}{}{}", c.name, extra, ifs);
        }
    }
    if !found {
        eprintln!("error: no {} found", ctype);
        std::process::exit(1);
    }
    Ok(())
}

fn cmd_features(file: &str) -> Result<(), String> {
    let info = load(file)?;
    if info.features.is_empty() { eprintln!("error: no features"); std::process::exit(1); }
    for f in &info.features {
        let req = if f.required { "" } else { " (optional)" };
        let gl = f.gl_es_version.map(|v| format!(" glEs={}", v)).unwrap_or_default();
        let name = f.name.as_deref().unwrap_or("(unnamed)");
        println!("{}{}{}", name, req, gl);
    }
    Ok(())
}

fn cmd_libraries(file: &str) -> Result<(), String> {
    let info = load(file)?;
    if info.libraries.is_empty() { eprintln!("error: no libraries"); std::process::exit(1); }
    for l in &info.libraries {
        println!("{}", l.name);
    }
    Ok(())
}

fn cmd_resources(file: &str) -> Result<(), String> {
    let info = load(file)?;
    let r = &info.resources;
    println!("has_resources={} total_entries={}", r.has_resources, r.total_entries);
    for pkg in &r.packages {
        println!("  package id={} name='{}' types={} entries={}",
            pkg.id, pkg.name, pkg.type_names.len(), pkg.entry_count);
    }
    if !r.locales.is_empty() { println!("locales: {}", r.locales.join(", ")); }
    if !r.densities.is_empty() { println!("densities: {}", r.densities.join(", ")); }
    Ok(())
}

fn cmd_locales(file: &str) -> Result<(), String> {
    let info = load(file)?;
    if info.resources.locales.is_empty() { eprintln!("error: no locales"); std::process::exit(1); }
    for l in &info.resources.locales { println!("{}", l); }
    Ok(())
}

fn cmd_densities(file: &str) -> Result<(), String> {
    let info = load(file)?;
    if info.resources.densities.is_empty() { eprintln!("error: no densities"); std::process::exit(1); }
    for d in &info.resources.densities { println!("{}", d); }
    Ok(())
}

fn cmd_resolutions(file: &str) -> Result<(), String> {
    let info = load(file)?;
    if info.resources.configurations.is_empty() { eprintln!("error: no configurations"); std::process::exit(1); }
    for c in &info.resources.configurations { println!("{}", c); }
    Ok(())
}

fn cmd_signing(file: &str) -> Result<(), String> {
    let info = load(file)?;
    let s = &info.signing;
    let schemes = if s.schemes.is_empty() { "none".into() } else { s.schemes.join(", ") };
    println!("schemes: {}", schemes);
    println!("certificates: {}", s.certificates.len());
    for c in &s.certificates {
        println!("  subject={}", c.subject);
        println!("  issuer={}", c.issuer);
        println!("  sha256={}", c.sha256);
        println!("  expires={} expired={}", c.not_after, c.expired);
    }
    Ok(())
}

fn cmd_certificates(file: &str, verbose: bool) -> Result<(), String> {
    let info = load(file)?;
    if info.signing.certificates.is_empty() { eprintln!("error: no certificates"); std::process::exit(1); }
    for c in &info.signing.certificates {
        if verbose {
            println!("{}", serde_json::to_string_pretty(c).map_err(|e| e.to_string())?);
        } else {
            println!("subject={}", c.subject);
            println!("  issuer={}", c.issuer);
            println!("  serial={}", c.serial_number);
            println!("  sha256={}", c.sha256);
            println!("  algorithm={}", c.algorithm);
            println!("  expires={} expired={}", c.not_after, c.expired);
        }
    }
    Ok(())
}

fn cmd_abis(file: &str, verbose: bool) -> Result<(), String> {
    let info = load(file)?;
    if info.native_libs.supported_abis.is_empty() { eprintln!("error: no native libs"); std::process::exit(1); }
    if verbose {
        println!("{}", serde_json::to_string_pretty(&info.native_libs).map_err(|e| e.to_string())?);
    } else {
        for abi in &info.native_libs.supported_abis {
            println!("{}", abi);
        }
    }
    Ok(())
}

fn cmd_native(file: &str) -> Result<(), String> {
    let info = load(file)?;
    if info.native_libs.supported_abis.is_empty() { eprintln!("error: no native libs"); std::process::exit(1); }
    println!("primary ABI: {}", info.native_libs.primary_abi.as_deref().unwrap_or("none"));
    println!("64-bit: {}  32-bit: {}", info.native_libs.has_64bit, info.native_libs.has_32bit);
    println!("total libraries: {}", info.native_libs.total_libs);
    for a in &info.native_libs.per_abi {
        println!("  {} ({} libs)", a.abi, a.count);
        for lib in &a.libs {
            println!("    {}", lib);
        }
    }
    Ok(())
}

fn cmd_metadata(file: &str, count_only: bool) -> Result<(), String> {
    let info = load(file)?;
    if count_only {
        println!("{}", info.meta_data.len());
        return Ok(());
    }
    if info.meta_data.is_empty() { eprintln!("error: no meta-data"); std::process::exit(1); }
    for m in &info.meta_data {
        let val = m.value.as_deref().unwrap_or("");
        let res = m.resource.map(|r| format!(" @0x{:08x}", r)).unwrap_or_default();
        println!("{}={}{}", m.name, val, res);
    }
    Ok(())
}

fn cmd_supports_screens(file: &str) -> Result<(), String> {
    let info = load(file)?;
    match &info.supports_screens {
        Some(ss) => {
            println!("smallScreens={:?} normalScreens={:?} largeScreens={:?} xlargeScreens={:?}",
                ss.small_screens, ss.normal_screens, ss.large_screens, ss.xlarge_screens);
            println!("resizeable={:?} anyDensity={:?}", ss.resizeable, ss.any_density);
        }
        None => { eprintln!("error: supports-screens not found"); std::process::exit(1); }
    }
    Ok(())
}

fn cmd_original_package(file: &str) -> Result<(), String> {
    let info = load(file)?;
    if info.original_packages.is_empty() { eprintln!("error: no original-package"); std::process::exit(1); }
    for p in &info.original_packages { println!("{}", p.name); }
    Ok(())
}

fn cache_key_for(path: &str) -> String {
    let s = path.strip_prefix(r"\\?\").unwrap_or(path);
    let mut k: String = s.chars().map(|c| match c {
        '\\' | ':' | ' ' | '/' | '?' | '*' | '"' | '<' | '>' | '|' => '_',
        _ => c,
    }).collect();
    if k.len() > 120 {
        k = k[k.len()-120..].to_string();
    }
    k
}

fn cmd_batch_icons(files: &[String], out_dir: Option<&str>, prefer_round: bool) -> Result<(), String> {
    use std::path::PathBuf;

    let cache_dir = match out_dir {
        Some(d) => PathBuf::from(d),
        None => {
            let local = std::env::var("LOCALAPPDATA")
                .unwrap_or_else(|_| std::env::var("TEMP").unwrap_or_else(|_| ".".into()));
            PathBuf::from(local).join("WSA_Installer").join("ApkIconCache")
        }
    };
    std::fs::create_dir_all(&cache_dir).map_err(|e| format!("create cache dir: {}", e))?;

    let mut results: Vec<serde_json::Value> = Vec::new();
    for file_path in files {
        let path = std::path::Path::new(file_path);
        let mut res = serde_json::json!({
            "path": file_path,
            "package": "",
            "app_name": "",
            "ico_file": "",
            "error": ""
        });

        let result = (|| -> std::result::Result<Vec<u8>, String> {
            let bytes = icon_bytes_file(path, prefer_round).map_err(|e| format!("icon: {}", e))?;
            if bytes.is_empty() {
                return Err("empty icon data".into());
            }
            png_to_ico(&bytes).map_err(|e| format!("ico: {}", e))
        })();

        match result {
            Ok(ico_data) => {
                // Use CacheKeyFor naming (same as C++ GetCacheDir): replace special chars, truncate
                let abs_path = std::fs::canonicalize(path).unwrap_or_else(|_| path.to_path_buf());
                let abs_str = abs_path.to_string_lossy().to_string();
                let ico_name = format!("{}.ico", cache_key_for(&abs_str));
                let ico_path = cache_dir.join(&ico_name);

                if let Err(e) = std::fs::write(&ico_path, &ico_data) {
                    res["error"] = serde_json::Value::String(format!("write ico: {}", e));
                } else {
                    res["ico_file"] = serde_json::Value::String(ico_path.to_string_lossy().to_string());
                    // Try to extract package info for the JSON
                    if let Ok(source) = aaptpp_core::pipeline::select_source_apk(path) {
                        if let Ok(info) = aaptpp_core::pipeline::extract_metadata(&source) {
                            res["package"] = serde_json::Value::String(info.manifest.package);
                            res["app_name"] = serde_json::Value::String(info.app_name);
                        }
                    }
                }
            }
            Err(e) => {
                res["error"] = serde_json::Value::String(e);
            }
        }
        results.push(res);
    }

    println!("{}", serde_json::to_string(&serde_json::json!(results)).map_err(|e| e.to_string())?);
    Ok(())
}

fn cmd_icon(file: &str, out: Option<String>, as_ico: bool, prefer_round: bool, debug: bool, json: bool) -> Result<(), String> {
    let path = Path::new(file);
    let source = aaptpp_core::select_source_apk(path).map_err(|e| e.to_string())?;
    let info = aaptpp_core::pipeline::extract_metadata(&source).map_err(|e| e.to_string())?;

    let bytes = icon_bytes_file(path, prefer_round).map_err(|e| e.to_string())?;
    let data: Vec<u8> = if as_ico {
        png_to_ico(&bytes).map_err(|e| e.to_string())?
    } else {
        bytes
    };

    let data_size = data.len();
    let is_png = data.len() >= 4 && &data[0..4] == b"\x89PNG";
    let is_ico = data.len() >= 6 && data[0] == 0 && data[1] == 0 && data[2] == 1 && data[3] == 0;
    let is_jpeg = data.len() >= 2 && data[0] == 0xFF && data[1] == 0xD8;
    let fmt = if is_ico { "ICO" } else if is_png { "PNG" } else if is_jpeg { "JPEG" } else { "binary" };

    // Write binary icon data to output (file or stdout)
    match out {
        Some(ref path) => {
            std::fs::write(path, &data).map_err(|e| e.to_string())?;
        }
        None => {
            use std::io::Write;
            std::io::stdout().write_all(&data).map_err(|e| e.to_string())?;
        }
    }

    // Output info to stderr
    if json {
        let mut obj = serde_json::Map::new();
        obj.insert("file".into(), serde_json::Value::String(file.to_string()));
        obj.insert("package".into(), serde_json::Value::String(info.manifest.package.clone()));
        obj.insert("app_name".into(), serde_json::Value::String(info.app_name.clone()));
        obj.insert("format".into(), serde_json::Value::String(fmt.into()));
        obj.insert("size_bytes".into(), serde_json::Value::Number(data_size.into()));
        obj.insert("as_ico".into(), serde_json::Value::Bool(as_ico));
        if let Some(ref v) = info.manifest.version_name {
            obj.insert("version".into(), serde_json::Value::String(v.clone()));
        }
        if let Some(sdk) = info.sdk.min {
            obj.insert("min_sdk".into(), serde_json::Value::Number(sdk.into()));
        }
        if let Some(sdk) = info.sdk.target {
            obj.insert("target_sdk".into(), serde_json::Value::Number(sdk.into()));
        }
        eprintln!("{}", serde_json::to_string_pretty(&serde_json::Value::Object(obj)).unwrap_or_default());
    } else {
        println!("Icon:   {} [{} {} bytes]", fmt, if prefer_round { "round" } else { "standard" }, data_size);
        println!("Source: {}", info.manifest.package);
        println!("App:    {}", info.app_name);
        if let Some(ref v) = info.manifest.version_name {
            println!("Ver:    {}", v);
        }
        if debug {
            println!("Container: {:?}", source.original_type);
            println!("Path:      {}", source.path.display());
            if let Some(ref cp) = source.container_path {
                println!("Extracted: {}", cp.display());
            }
        }
    }

    Ok(())
}

fn cmd_convert(file: &str, output: Option<String>) -> Result<(), String> {
    use aaptpp_core::detect::{detect_file, PackageType, base_apk_member};
    use aaptpp_core::archive::ZipArchive;
    use std::io::Write;

    let path = Path::new(file);
    let ptype = detect_file(path).map_err(|e| e.to_string())?;

    match ptype {
        PackageType::Apk | PackageType::Aab => {
            match output {
                Some(out) => { std::fs::copy(path, Path::new(&out)).map_err(|e| e.to_string())?; println!("{}", out); }
                None => { println!("{}", file); }
            }
        }
        PackageType::Xapk | PackageType::Apks | PackageType::Apkm => {
            let mut za = ZipArchive::open_path(path).map_err(|e| e.to_string())?;
            let names: Vec<String> = za.entry_names().iter().map(|s| s.to_string()).collect();
            let base = base_apk_member(&names).ok_or_else(|| "no base APK found in container".to_string())?;
            let bytes = za.read_entry(&base).map_err(|e| e.to_string())?;

            let out_path = match output {
                Some(ref o) => o.clone(),
                None => {
                    let stem = path.file_stem().map(|s| s.to_string_lossy()).unwrap_or_default();
                    let parent = path.parent().unwrap_or(Path::new("."));
                    let mut p = parent.join(format!("{}.apk", stem));
                    let mut i = 1;
                    while p.exists() {
                        p = parent.join(format!("{}_{}.apk", stem, i));
                        i += 1;
                    }
                    p.to_string_lossy().to_string()
                }
            };

            let mut f = std::fs::File::create(&out_path).map_err(|e| e.to_string())?;
            f.write_all(&bytes).map_err(|e| e.to_string())?;
            println!("{}", out_path);
        }
        _ => { return Err("unsupported package type for conversion".to_string()); }
    }
    Ok(())
}

fn cmd_svg(file: &str, out: Option<String>, prefer_round: bool) -> Result<(), String> {
    let path = Path::new(file);
    let ext = path.extension().and_then(|e| e.to_str()).unwrap_or("").to_lowercase();

    let svg_str = if ext == "xml" {
        // Direct XML vector drawable → SVG
        let bytes = std::fs::read(path).map_err(|e| format!("read: {}", e))?;
        xml_to_svg(&bytes).map_err(|e| format!("xml_to_svg: {}", e))?
    } else {
        // APK/XAPK/etc → extract icon bytes, render to SVG
        let icon_bytes = icon_bytes_file(path, prefer_round).map_err(|e| format!("icon: {}", e))?;
        if icon_bytes.len() >= 4 && &icon_bytes[0..4] == b"\x89PNG" {
            // PNG icon — can't convert raster to vector SVG, output as is or return error
            return Err("icon is raster (PNG/JPEG), cannot convert to SVG. Use --ico for ICO output.".into());
        }
        if icon_bytes.len() >= 8 && icon_bytes[0] == 0x03 && icon_bytes[1] == 0x00 {
            // Binary XML vector drawable
            xml_to_svg(&icon_bytes).map_err(|e| format!("xml_to_svg: {}", e))?
        } else {
            return Err("icon format not supported for SVG conversion".into());
        }
    };

    match out {
        Some(ref path) => {
            std::fs::write(path, svg_str.as_bytes()).map_err(|e| e.to_string())?;
            println!("{}", path);
        }
        None => {
            println!("{}", svg_str);
        }
    }
    Ok(())
}

fn cmd_svg_ico(file: &str, out: Option<String>) -> Result<(), String> {
    let path = Path::new(file);
    let svg_bytes = std::fs::read(path).map_err(|e| format!("read: {}", e))?;
    let ico_data = svg_to_ico(&svg_bytes).map_err(|e| format!("svg_to_ico: {}", e))?;

    match out {
        Some(ref path) => {
            std::fs::write(path, &ico_data).map_err(|e| e.to_string())?;
            println!("{}", path);
        }
        None => {
            use std::io::Write;
            std::io::stdout().write_all(&ico_data).map_err(|e| e.to_string())?;
        }
    }
    Ok(())
}

fn cmd_xml_ico(file: &str, out: Option<String>) -> Result<(), String> {
    let path = Path::new(file);
    let bytes = std::fs::read(path).map_err(|e| format!("read: {}", e))?;
    let ico_data = xml_to_ico(&bytes).map_err(|e| format!("xml_to_ico: {}", e))?;

    match out {
        Some(ref path) => {
            std::fs::write(path, &ico_data).map_err(|e| e.to_string())?;
            println!("{}", path);
        }
        None => {
            use std::io::Write;
            std::io::stdout().write_all(&ico_data).map_err(|e| e.to_string())?;
        }
    }
    Ok(())
}
