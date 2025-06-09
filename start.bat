@echo off
echo 🇬🇷 Greek Social Story Video Generator
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    echo 📥 Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo ⚠️ Environment file not found!
    echo 🔧 Running setup first...
    echo.
    python setup.py
    echo.
)

REM Start the main application
echo 🚀 Starting Greek Video Generator...
echo.
python main.py --interactive

pause 