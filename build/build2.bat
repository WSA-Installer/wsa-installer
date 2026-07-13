@echo off
chcp 65001 >nul 2>nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

:: -------- Step 0: Activate Virtual Environment --------
if exist "venv\Scripts\activate.bat" (
    echo [+] Activating virtual environment...
    call venv\Scripts\activate.bat
)

title WSA Installer Build Script (Nuitka Standalone)

set DIST_FINAL=dist\WSA Installer

echo ============================================
echo  WSA Installer Build Script
echo  1. Clean + Check dependencies
echo  2. Nuitka --standalone app
echo  3. Restructure into _internal\ layout
echo  4. Compile launcher (C# via PowerShell)
echo  5. Copy assets + bundle.wsa
echo  6. NSIS installer
echo ============================================
echo.

:: -------- Step 1: Clean + Dependencies --------
echo [1/6] Cleaning previous build...
if exist "dist"                        rmdir /s /q "dist"
if exist "*.build"                     for /d %%d in (*.build) do rmdir /s /q "%%d" 2>nul
if exist "app.build_src_backup"        del /f /q "app.build_src_backup"
echo   [+] Clean complete.
echo.

echo [1/6] Checking dependencies...
venv\Scripts\python.exe -c "import py7zr, requests, flet, pyautogui, pyperclip, pywinauto, PyQt6" >nul 2>nul
if %errorlevel% neq 0 (
    echo   [!] Missing dependencies — installing...
    venv\Scripts\pip.exe install -r requirements.txt
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

:: -------- Step 2: Nuitka --standalone --------
echo [2/6] Compiling run.py to standalone EXE with Nuitka...
echo   This may take 30-60 minutes.
echo.
python -m nuitka --standalone ^
    --remove-output ^
    --windows-uac-admin ^
    --windows-icon-from-ico=assets\icon.ico ^
    --output-dir=tmp_nuitka ^
    run.py
if %errorlevel% neq 0 (
    echo [!] NUITKA COMPILATION FAILED (errorlevel=%errorlevel%^)
    pause
    exit /b 1
)
echo   [+] Nuitka build complete.
echo.

:: -------- Step 3: Restructure into _internal\ layout --------
echo [3/6] Restructuring output (PyInstaller-style _internal\)...

:: Create final directory structure
if not exist "%DIST_FINAL%\_internal" mkdir "%DIST_FINAL%\_internal"

:: Rename run.exe -> WSA Installer.exe
ren "tmp_nuitka\run.dist\run.exe" "WSA Installer.exe"

:: Move everything into _internal\ (including the real EXE)
xcopy /e /i /y "tmp_nuitka\run.dist\*.*" "%DIST_FINAL%\_internal\" >nul

:: Clean up Nuitka temp
rmdir /s /q "tmp_nuitka"

:: Copy assets into _internal\
if exist "assets" (
    xcopy /e /i /y "assets" "%DIST_FINAL%\_internal\assets" >nul
)

echo   [+] Restructure done. _internal\ has the real EXE + all deps.
echo.

:: -------- Step 4: Compile launcher (C# -> WSA Installer.exe) --------
echo [4/6] Compiling launcher EXE (C# via PowerShell)...

if not exist "launcher.cs" (
    echo   [!] launcher.cs not found — creating batch launcher instead...
    echo @start "" /D "%%~dp0_internal" "%%~dp0_internal\WSA Installer.exe" %%* > "%DIST_FINAL%\WSA Installer.cmd"
    echo   [+] Created batch launcher: WSA Installer.cmd
    echo   [~] NSIS and shortcuts will still work.
) else (
    :: Compile launcher.cs to GUI EXE at root level
    powershell -Command "Add-Type -TypeDefinition (Get-Content 'launcher.cs' -Raw) -OutputAssembly '%DIST_FINAL%\WSA Installer.exe' -OutputType WindowsApplication" >nul 2>nul
    if %errorlevel% neq 0 (
        echo   [!] LAUNCHER COMPILATION FAILED.
        echo   Trying alternative: batch launcher...
        echo @start "" /D "%%~dp0_internal" "%%~dp0_internal\WSA Installer.exe" %%* > "%DIST_FINAL%\WSA Installer.cmd"
        echo   [+] Created batch launcher instead: WSA Installer.cmd
        echo   [~] NSIS and shortcuts will still work.
    )
)
echo.

:: -------- Step 5: Bundle prompt (bundle.wsa) --------
echo [5/6] Build done.
echo   Output folder: %DIST_FINAL%
echo   Executable   : %DIST_FINAL%\WSA Installer.exe
echo.
echo   Enter path to bundle.wsa file (or leave empty to skip):
set /p BUNDLE_PATH="bundle.wsa path: "
if not "!BUNDLE_PATH!"=="" (
    if exist "!BUNDLE_PATH!" (
        echo   Copying bundle.wsa to %DIST_FINAL%\out_asset\...
        if not exist "%DIST_FINAL%\out_asset" mkdir "%DIST_FINAL%\out_asset"
        copy /y "!BUNDLE_PATH!" "%DIST_FINAL%\out_asset\bundle.wsa" >nul
        echo   [+] bundle.wsa copied.
    ) else (
        echo   [~] File not found: !BUNDLE_PATH!
    )
) else (
    echo   Skipping bundle copy.
)
echo.

:: -------- Step 6: NSIS --------
echo [6/6] Building NSIS installer...
if not exist "WSA_Installer_Setup.nsi" (
    echo   [~] WSA_Installer_Setup.nsi not found - skipping NSIS.
    goto :finish
)

makensis "WSA_Installer_Setup.nsi"
if %errorlevel% equ 0 (
    echo   [+] NSIS installer created: dist\WSA_Installer_Setup.exe
) else (
    echo   [~] makensis not in PATH, trying default path...
    if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
        "C:\Program Files (x86)\NSIS\makensis.exe" "WSA_Installer_Setup.nsi"
        if !errorlevel! equ 0 (
            echo   [+] NSIS installer created: dist\WSA_Installer_Setup.exe
        ) else (
            echo   [!] NSIS failed. Install NSIS from https://nsis.sourceforge.io/
        )
    ) else (
        echo   [!] NSIS not found. Install NSIS from https://nsis.sourceforge.io/
    )
)

:finish
echo.
echo ========================================
echo  ALL DONE
echo ========================================
echo  Launcher     : %DIST_FINAL%\WSA Installer.exe
echo  App + deps   : %DIST_FINAL%\_internal\
echo  Installer    : dist\WSA_Installer_Setup.exe
echo ========================================
echo.
pause
