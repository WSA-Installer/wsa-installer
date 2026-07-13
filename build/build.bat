@echo off
chcp 65001 >nul 2>nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

:: ═══════════════════════════════════════════════════════════════
::  VERSION — Change this to update app.py, file_version_info,
::  and NSIS installer version in one shot.
:: ═══════════════════════════════════════════════════════════════
SET VERSION=1.2
:: -------- Step 0: Activate Virtual Environment --------
if exist "venv\Scripts\activate.bat" (
    echo [+] Activating virtual environment...
    call venv\Scripts\activate.bat
)

title WSA Installer Build Script

echo ============================================
echo  WSA Installer Build Script
echo  1. Clean
echo  2. Check dependencies
echo  3. Nuitka module (app.py -^> app.pyd)
echo  4. PyInstaller onedir
echo  5. Patch Flet client (icon + metadata)
echo  6. (optional) bundle.wsa
echo  7. NSIS installer
echo ============================================
echo.

:: -------- Step 1: Clean --------
echo [1/7] Cleaning previous build...
if exist "dist"                        rmdir /s /q "dist"
if exist "build"                       rmdir /s /q "build"
if exist "app.pyd"                     del /f /q "app.pyd"
if exist "app.pyi"                     del /f /q "app.pyi"
for /d %%d in (*.build) do rmdir /s /q "%%d" 2>nul
echo   [+] Clean complete.
echo.

:: -------- Step 2: Dependencies --------
echo [2/7] Checking dependencies...
venv\Scripts\python.exe -c "import requests, flet, pyautogui, pyperclip, pywinauto, PyQt6" >nul 2>nul
if %errorlevel% neq 0 (
    echo   [!] Missing dependencies — installing...
    venv\Scripts\python.exe -m pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo   [!] PIP INSTALL FAILED.
        pause
        exit /b 1
    )
    echo   [+] Dependencies installed.
) else (
    echo   [+] All dependencies OK.
)
echo.

:: -------- Step 2.5: Update version across all files --------
echo [2.5/7] Setting version to %VERSION%...

:: app.py: APP_ID suffix
powershell -Command "$c = Get-Content 'app.py' -Raw; $c = $c -replace 'mrcyber\.wsainstaller\.download\.\d+\.\d+', 'mrcyber.wsainstaller.download.%VERSION%'; Set-Content 'app.py' -Value $c -Encoding UTF8 -NoNewline"

:: file_version_info.txt: string versions (1.0.0.0 -> X.Y.0.0) and tuple versions (1, 0, 0, 0)
for /f "tokens=1,2 delims=." %%a in ("%VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)
powershell -Command "$c = Get-Content 'file_version_info.txt' -Raw; $c = $c -replace '\d+\.\d+\.\d+\.\d+', '%VERSION%.0.0'; $c = $c -replace '\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)', '(!MAJOR!, !MINOR!, 0, 0)'; Set-Content 'file_version_info.txt' -Value $c -Encoding UTF8 -NoNewline"

echo   [+] Version updated to %VERSION%
echo     - app.py            APP_ID = mrcyber.wsainstaller.download.%VERSION%
echo     - file_version_info  FileVersion = %VERSION%.0.0
echo     - NSIS will use /DAPP_VERSION=%VERSION%
echo.

:: -------- Step 3: Nuitka module (Protect source code) --------
echo [3/7] Compiling app.pyd with Nuitka...

:: Backup app.py before compilation
copy /y app.py app.py.backup >nul
echo   [+] Backup created: app.py.backup

:: Compile app.py directly (keeps PyInit_app export correct)
python -m nuitka --module --remove-output app.py
if %errorlevel% neq 0 (
    echo [!] NUITKA MODULE COMPILATION FAILED.
    copy /y app.py.backup app.py >nul
    del app.py.backup
    pause
    exit /b 1
)

:: Find the compiled .pyd (ABI-tagged: app.cp314-win_amd64.pyd)
if exist app.*.pyd (
    for %%f in (app.*.pyd) do (
        ren "%%f" "app.pyd"
        goto :pyd_renamed
    )
)
echo [!] No .pyd file found after Nuitka compilation.
copy /y app.py.backup app.py >nul
del app.py.backup
pause
exit /b 1
:pyd_renamed

:: Verify app.pyd exists
if not exist "app.pyd" (
    echo [!] app.pyd not found after rename.
    copy /y app.py.backup app.py >nul
    del app.py.backup
    pause
    exit /b 1
)
echo   [+] app.pyd created successfully (PyInit_app export intact).

:: Delete interface file (exposes function signatures)
if exist "app.pyi" (
    del /f /q "app.pyi"
    echo   [+] app.pyi deleted.
)

:: Rename app.py to wsa.py — hides source from PyInstaller, forces it to bundle app.pyd
ren app.py wsa.py
echo   [+] app.py renamed to wsa.py — source hidden from PyInstaller.

:: Backup no longer needed
echo.

:: -------- Step 3.5: Compile WSARepair.py to WSARepair.exe --------
echo [3.5/7] Compiling WSARepair.exe...

venv\Scripts\pyinstaller.exe --onefile --name WSARepair --distpath assets --workpath build_tmp --specpath build_tmp --noconfirm WSARepair.py
if %errorlevel% neq 0 (
    echo [!] WSARepair.py compilation failed — skipping.
) else (
    echo   [+] WSARepair.exe compiled to assets\
)

:: Clean up build artifacts
if exist "build_tmp" rmdir /s /q "build_tmp"
echo.

:: -------- Step 4: PyInstaller onedir --------
echo [4/7] Running PyInstaller (onedir)...
echo   Spec: WSA_Installer_Download_onedir.spec
echo.

venv\Scripts\pyinstaller.exe --noconfirm "WSA_Installer_Download_onedir.spec"
if %errorlevel% neq 0 (
    echo [!] PyInstaller failed, trying python -m PyInstaller...
    venv\Scripts\python.exe -m PyInstaller "WSA_Installer_Download_onedir.spec"
    if %errorlevel% neq 0 (
        echo [!] PYINSTALLER FAILED.
        if exist "wsa.py" (
            ren wsa.py app.py
        )
        pause
        exit /b 1
    )
)

echo   [+] PyInstaller onedir build complete.
echo.

:: -------- Restore app.py from wsa.py --------
echo [4.5/7] Restoring app.py...
if exist "wsa.py" (
    ren wsa.py app.py
    echo   [+] app.py restored from wsa.py.
)
echo.

:: -------- Step 4.6 removed: clean_venv replaced by embedded Python in .pyd --------

:: -------- Step 5: Patch Flet client EXE --------
echo [5/7] Patching Flet client EXE (icon + metadata)...

set FLET_EXE=dist\WSA Installer\_internal\flet_desktop\app\flet\flet.exe

if not exist "patch_flet" mkdir "patch_flet"

if exist "!FLET_EXE!" (
    :: Backup original
    copy /y "!FLET_EXE!" "patch_flet\flet.exe.bak" >nul
    echo   [+] Backed up original flet.exe

    venv\Scripts\python.exe patch_flet.py "!FLET_EXE!" "assets\icon.ico" "file_version_info.txt"
    if !errorlevel! equ 0 (
        echo   [+] Flet client patched successfully
        copy /y "!FLET_EXE!" "patch_flet\flet.exe" >nul
        echo   [+] Patched copy saved to patch_flet\flet.exe
    ) else (
        echo   [!] Patch FAILED — restoring backup...
        copy /y "patch_flet\flet.exe.bak" "!FLET_EXE!" >nul
    )

    :: Also patch the cached Flet client for immediate effect
    for /d %%d in ("%USERPROFILE%\.flet\client\flet-desktop-full-*") do (
        if exist "%%d\flet.exe" (
            echo   [~] Patching cached Flet client at %%d...
            copy /y "%%d\flet.exe" "%%d\flet.exe.bak" >nul 2>nul
            venv\Scripts\python.exe patch_flet.py "%%d\flet.exe" "assets\icon.ico" "file_version_info.txt"
        )
    )

    :: Create patched flet-windows.zip so client machines extract patched version
    :: instead of downloading original from GitHub
    set FLET_APP_DIR=dist\WSA Installer\_internal\flet_desktop\app
    if exist "!FLET_APP_DIR!\flet" (
        echo   [~] Creating patched flet-windows.zip...
        del /f /q "!FLET_APP_DIR!\flet-windows.zip" >nul 2>nul
        powershell -Command "Compress-Archive -Path '!FLET_APP_DIR!\flet' -DestinationPath '!FLET_APP_DIR!\flet-windows.zip' -Force"
        if !errorlevel! equ 0 (
            echo   [+] Patched flet-windows.zip created for client cache extraction
        ) else (
            echo   [!] Failed to create flet-windows.zip
        )
    )
) else (
    echo   [~] flet.exe not found at !FLET_EXE! — skipping patch
)
echo.

:: -------- Step 6: Bundle prompt (bundle.wsa) --------
echo [6/7] PyInstaller build done.
echo   Output folder: dist\WSA Installer\
echo ========================================
echo.
echo   Enter path to bundle.wsa file (or leave empty to skip):
set /p BUNDLE_PATH="bundle.wsa path: "
if not "!BUNDLE_PATH!"=="" (
    if exist "!BUNDLE_PATH!" (
        echo   Copying bundle.wsa to dist\WSA Installer\out_asset\...
        if not exist "dist\WSA Installer\out_asset" mkdir "dist\WSA Installer\out_asset"
        copy /y "!BUNDLE_PATH!" "dist\WSA Installer\out_asset\bundle.wsa" >nul
        echo   [+] bundle.wsa copied.
    ) else (
        echo   [~] File not found: !BUNDLE_PATH!
    )
) else (
    echo   Skipping bundle copy.
)
echo.

:: -------- Step 7: NSIS --------
echo [7/7] Building NSIS installer...
if not exist "WSA_Installer_Setup.nsi" (
    echo [!] WSA_Installer_Setup.nsi not found - skipping NSIS.
    goto :finish
)

makensis /DAPP_VERSION=%VERSION% "WSA_Installer_Setup.nsi"
if %errorlevel% equ 0 (
    echo [+] NSIS installer created: dist\WSA_Installer_Setup.exe
) else (
    echo [~] makensis not in PATH, trying default path...
    if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
        "C:\Program Files (x86)\NSIS\makensis.exe" /DAPP_VERSION=%VERSION% "WSA_Installer_Setup.nsi"
        if !errorlevel! equ 0 (
            echo [+] NSIS installer created: dist\WSA_Installer_Setup.exe
        ) else (
            echo [!] NSIS failed. Install NSIS from https://nsis.sourceforge.io/
        )
    ) else (
        echo [!] NSIS not found. Install NSIS from https://nsis.sourceforge.io/
    )
)

:finish
:: Safety: restore app.py if wsa.py still exists
if exist "wsa.py" (
    echo [~] Restoring app.py from wsa.py...
    ren wsa.py app.py
)
echo.
echo ========================================
echo  ALL DONE
echo ========================================
echo  EXE + deps : dist\WSA Installer\
echo  Installer  : dist\WSA_Installer_Setup.exe
echo ========================================
echo.
pause
