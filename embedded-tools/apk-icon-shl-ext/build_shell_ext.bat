@echo off
REM Build ApkIconShlExt.dll (x64) using MSVC from Visual Studio.
REM Embeds default_apk.ico as RCDATA resource.
REM Shows default icon for all .apk/.xapk/.apks/.apkm/.aab files.
setlocal
cd /d "%~dp0"

set VSROOT=C:\Program Files\Microsoft Visual Studio\18\Insiders
set VCVARS=%VSROOT%\VC\Auxiliary\Build\vcvars64.bat
set SDKINC=C:\Program Files (x86)\Windows Kits\10\Include\10.0.26100.0\um
set SDKSHARED=C:\Program Files (x86)\Windows Kits\10\Include\10.0.26100.0\shared

if not exist "%VCVARS%" (
    echo [!] vcvars64.bat not found at %VCVARS%
    echo     Adjust VSROOT in this script to your Visual Studio install.
    exit /b 1
)

call "%VCVARS%"
if errorlevel 1 (
    echo [!] Failed to initialize MSVC environment.
    exit /b 1
)

echo [*] Compiling resources ...
rc /nologo /fo ApkIconShlExt.res ApkIconShlExt.rc
if errorlevel 1 (
    echo [!] Resource compilation FAILED.
    exit /b 1
)

echo [*] Compiling ApkIconShlExt.cpp ...
cl /nologo /c /EHsc /O2 /I"%SDKINC%" /I"%SDKSHARED%" ApkIconShlExt.cpp
if errorlevel 1 (
    echo [!] Compilation FAILED.
    exit /b 1
)

echo [*] Linking ApkIconShlExt.dll ...
link /nologo /DLL /DEF:ApkIconShlExt.def /OUT:ApkIconShlExt.dll ^
    ApkIconShlExt.obj ApkIconShlExt.res ^
    ole32.lib user32.lib gdi32.lib shell32.lib shlwapi.lib advapi32.lib
if errorlevel 1 (
    echo [!] Linking FAILED.
    exit /b 1
)

copy /Y "ApkIconShlExt.dll" "..\assets\ApkIconShlExt.dll"
if errorlevel 1 (
    echo [!] Failed to copy to assets.
    exit /b 1
)

echo [+] ApkIconShlExt.dll built (shell_ext\ + assets\)
echo [+] No external aaptpp/lib dependency.
endlocal
