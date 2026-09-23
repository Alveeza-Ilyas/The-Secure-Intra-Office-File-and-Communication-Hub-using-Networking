@echo off
title The Secure Intra-Office File & Communication Hub
echo ===================================================================
echo     Launching The Secure Intra-Office File and Communication Hub
echo ===================================================================
echo.

:: Check Python installation
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to PATH!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

:: Optional check for Flask
python -c "import flask" >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Installing required dependencies...
    python -m pip install -r requirements.txt
)

echo [INFO] Starting Flask Server on http://127.0.0.1:5000 ...
echo [INFO] Press Ctrl+C in this window anytime to stop the server.
echo.

:: Automatically open browser after 2 seconds in background
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:5000"

:: Start the Flask app
python app.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Server stopped unexpectedly.
    pause
)
