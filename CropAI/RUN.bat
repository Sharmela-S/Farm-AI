@echo off
color 0B
title AI Crop Recommendation System - Running

echo.
echo ════════════════════════════════════════════════════════════
echo         🌾 AI CROP RECOMMENDATION SYSTEM 🌾
echo ════════════════════════════════════════════════════════════
echo.

cd backend
call venv\Scripts\activate.bat

echo [*] Starting server...
echo.
echo ✅ Server starting on: http://localhost:5000
echo 🌐 Open browser and visit: http://localhost:5000
echo 💡 Press Ctrl+C to stop the server
echo.

REM Auto-open browser
start http://localhost:5000

python app.py

if errorlevel 1 (
    color 0C
    echo.
    echo [ERROR] Server failed to start!
    echo.
    echo SOLUTIONS:
    echo 1. Make sure you ran INSTALL.bat first
    echo 2. Check if port 5000 is already in use
    echo 3. Run as Administrator
    echo.
    pause
)

pause