@echo off
title Add Test Data - TechFlow Automation
color 0B
echo.
echo ===============================================
echo     Adding Test Data to TechFlow System
echo ===============================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo Activating Python environment...
call venv\Scripts\activate
cd data_dashboard

echo.
echo Creating test files...
python records\utils\create_test_files.py

echo.
echo Test data has been added!
echo Check the web application to see the new records.
echo.
pause
