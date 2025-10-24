@echo off
color 0A
title AI Crop Recommendation System - Installer

echo.
echo ════════════════════════════════════════════════════════════
echo      AI CROP RECOMMENDATION SYSTEM - INSTALLER
echo ════════════════════════════════════════════════════════════
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python is NOT installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation:
    echo   ✓ Check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [Step 1/6] Python found!
python --version
echo.

echo [Step 2/6] Creating project directories...
mkdir backend 2>nul
mkdir frontend 2>nul
mkdir frontend\css 2>nul
mkdir frontend\js 2>nul
mkdir frontend\assets 2>nul
mkdir frontend\assets\images 2>nul
mkdir frontend\assets\icons 2>nul
mkdir data 2>nul
mkdir data\sample_soils 2>nul
mkdir models 2>nul
mkdir uploads 2>nul
echo ✓ Directories created!
echo.

echo [Step 3/6] Creating virtual environment...
cd backend
python -m venv venv
if errorlevel 1 (
    color 0C
    echo [ERROR] Failed to create virtual environment!
    pause
    exit /b 1
)
echo ✓ Virtual environment created!
echo.

echo [Step 4/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Activated!
echo.

echo [Step 5/6] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo ✓ Pip upgraded!
echo.

echo [Step 6/6] Installing required packages...
echo    This may take 5-10 minutes...
echo.
pip install flask==2.3.2 --quiet
echo    [1/5] Flask installed
pip install flask-cors==4.0.0 --quiet
echo    [2/5] Flask-CORS installed
pip install pillow==10.0.0 --quiet
echo    [3/5] Pillow installed
pip install numpy==1.24.3 --quiet
echo    [4/5] NumPy installed
pip install requests==2.31.0 --quiet
echo    [5/5] Requests installed

if errorlevel 1 (
    color 0C
    echo [ERROR] Package installation failed!
    echo.
    echo Try running as Administrator:
    echo Right-click INSTALL.bat and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

cd ..

color 0A
echo.
echo ════════════════════════════════════════════════════════════
echo                  ✅ INSTALLATION COMPLETE!
echo ════════════════════════════════════════════════════════════
echo.
echo 🚀 TO RUN: Double-click RUN.bat
echo 🌐 ACCESS: http://localhost:5000
echo.
pause