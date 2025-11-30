@echo off
REM WindowsUseAgent Setup Script for Windows
REM This script will set up the WindowsUseAgent on your Windows machine

echo ========================================
echo WindowsUseAgent Installation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [1/5] Python found:
python --version
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed.
    echo Please install pip or reinstall Python with pip included.
    pause
    exit /b 1
)

echo [2/5] pip found:
pip --version
echo.

REM Create virtual environment
echo [3/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
)
echo.

REM Activate virtual environment
echo [4/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)
echo.

REM Install dependencies
echo [5/5] Installing dependencies...
pip install -e .
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo.

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To use WindowsUseAgent:
echo   1. Activate the virtual environment: venv\Scripts\activate.bat
echo   2. Generate a config file: windowsuseagent --generate-config
echo   3. Edit config.json with your API keys
echo   4. Run the agent: windowsuseagent --config config.json
echo.
echo For more information, see README.md
echo ========================================
echo.
pause
