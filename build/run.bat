@echo off
chcp 65001 >nul 2>nul
setlocal
cd /d "%~dp0"

:: -------- Create venv if missing --------
if not exist "venv\Scripts\python.exe" (
    echo [+] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [!] Failed to create venv. Make sure Python is installed and in PATH.
        pause
        exit /b 1
    )
    echo [+] venv created.
)

:: -------- Install requirements if flet is missing --------
venv\Scripts\python.exe -c "import flet" >nul 2>nul
if %errorlevel% neq 0 (
    echo [+] Installing dependencies...
    venv\Scripts\python.exe -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [!] pip install failed.
        pause
        exit /b 1
    )
    echo [+] Dependencies installed.
)

:: -------- Run --------
echo [+] Starting WSA Installer...
venv\Scripts\python.exe run.py %*
