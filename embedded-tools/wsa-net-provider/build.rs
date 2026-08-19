fn main() {
    println!("cargo:rustc-link-lib=advapi32");
    println!("cargo:rustc-link-lib=mpr");
    println!("cargo:rustc-link-lib=kernel32");
    println!("cargo:rustc-link-lib=ws2_32");
}
