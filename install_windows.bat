@echo off
REM ZapProbe Windows Installation Script
REM Windows Setup Script

setlocal enabledelayedexpansion

echo.
echo ======================================================
echo ZapProbe - Windows Installation
echo ======================================================
echo.

REM Python check
echo [*] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python not found!
    echo.
    echo Please install Python 3.8+ from: https://www.python.org/
    echo Make sure to check "Add Python to PATH"
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo [+] Python %PYTHON_VER% found

REM pip check
echo [*] Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [!] pip not found!
    echo [*] Installing pip...
    python -m ensurepip --upgrade
)
for /f "tokens=2" %%i in ('pip --version 2^>^&1') do set PIP_VER=%%i
echo [+] %PIP_VER% found

REM Install dependencies
echo.
echo [*] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [!] Failed to install dependencies
    pause
    exit /b 1
)
echo [+] Dependencies installed

REM Install package
echo.
echo [*] Installing ZapProbe package...
pip install -e .
if errorlevel 1 (
    echo [!] Failed to install ZapProbe
    pause
    exit /b 1
)
echo [+] ZapProbe installed

REM Test installation
echo.
echo [*] Testing installation...
zapprobe --version >nul 2>&1
if errorlevel 1 (
    echo [!] zapprobe command not found
    echo [*] Trying with Python module...
    python -m cli_runner --version
) else (
    echo [+] zapprobe command works!
)

echo.
echo ======================================================
echo Installation Complete!
echo ======================================================
echo.
echo Usage:
echo   zapprobe --gui                    # GUI mode
echo   zapprobe URL                      # Quick scan
echo   zapprobe URL -t sqli -o report.json # Advanced
echo.
pause
