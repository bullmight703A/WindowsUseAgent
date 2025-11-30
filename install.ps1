# WindowsUseAgent Setup Script for Windows (PowerShell)
# This script will set up the WindowsUseAgent on your Windows machine

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "WindowsUseAgent Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[1/5] Python found: $pythonVersion" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if pip is installed
try {
    $pipVersion = pip --version 2>&1
    Write-Host "[2/5] pip found: $pipVersion" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "[ERROR] pip is not installed." -ForegroundColor Red
    Write-Host "Please install pip or reinstall Python with pip included." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Create virtual environment
Write-Host "[3/5] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Skipping creation." -ForegroundColor Yellow
} else {
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to create virtual environment." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "Virtual environment created successfully." -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "[4/5] Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to activate virtual environment." -ForegroundColor Red
    Write-Host "You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Install dependencies
Write-Host "[5/5] Installing dependencies..." -ForegroundColor Yellow
pip install -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install dependencies." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To use WindowsUseAgent:" -ForegroundColor Yellow
Write-Host "  1. Activate the virtual environment: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  2. Generate a config file: windowsuseagent --generate-config" -ForegroundColor White
Write-Host "  3. Edit config.json with your API keys" -ForegroundColor White
Write-Host "  4. Run the agent: windowsuseagent --config config.json" -ForegroundColor White
Write-Host ""
Write-Host "For more information, see README.md" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit"
