@echo off
title TechFlow Automation System
color 0A
echo.
echo ===============================================
echo     TechFlow Automation System Starting...
echo ===============================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo [1/3] Activating Python environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [2/3] Starting Django application...
cd data_dashboard
start "TechFlow Web Server" cmd /k "python manage.py runserver 127.0.0.1:8000"
timeout /t 3 /nobreak > nul

echo [3/3] Starting file monitoring system...
start "TechFlow File Monitor" cmd /k "python manage.py watch_files --path ../data"

echo.
echo ===============================================
echo     TechFlow Automation System is RUNNING!
echo ===============================================
echo.
echo ✓ Web Application: http://127.0.0.1:8000
echo ✓ File Monitor: Running in background
echo.
echo The system will automatically:
echo   - Process new emails in data/emails/
echo   - Process new forms in data/forms/
echo   - Process new invoices in data/invoices/
echo.
echo To add test data, run: add_test_data.bat
echo To stop the system, close both command windows.
echo.

REM Open the web application in browser after 5 seconds
timeout /t 5 /nobreak > nul
start http://127.0.0.1:8000

echo System is ready! You can close this window.
pause
