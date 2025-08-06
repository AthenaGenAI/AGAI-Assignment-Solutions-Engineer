@echo off
title TechFlow Automation - Quick Setup
color 0E
echo.
echo ===============================================
echo     TechFlow Automation - Quick Setup
echo ===============================================
echo.

set SCRIPT_DIR=%~dp0
set DESKTOP=%USERPROFILE%\Desktop

echo Creating desktop shortcuts...

REM Create shortcut for starting the system
echo Creating "Start TechFlow.lnk" on desktop...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Start TechFlow.lnk'); $Shortcut.TargetPath = '%SCRIPT_DIR%START_TECHFLOW.bat'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.IconLocation = 'shell32.dll,137'; $Shortcut.Description = 'Start TechFlow Automation System'; $Shortcut.Save()}"

REM Create shortcut for adding test data
echo Creating "Add Test Data.lnk" on desktop...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Add Test Data.lnk'); $Shortcut.TargetPath = '%SCRIPT_DIR%ADD_TEST_DATA.bat'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.IconLocation = 'shell32.dll,70'; $Shortcut.Description = 'Add test data to TechFlow'; $Shortcut.Save()}"

REM Create shortcut for stopping the system
echo Creating "Stop TechFlow.lnk" on desktop...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Stop TechFlow.lnk'); $Shortcut.TargetPath = '%SCRIPT_DIR%STOP_TECHFLOW.bat'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.IconLocation = 'shell32.dll,131'; $Shortcut.Description = 'Stop TechFlow Automation System'; $Shortcut.Save()}"

echo.
echo ===============================================
echo     Setup Complete!
echo ===============================================
echo.
echo Desktop shortcuts created:
echo   ✓ Start TechFlow - Starts the complete system
echo   ✓ Add Test Data - Adds sample emails/forms
echo   ✓ Stop TechFlow - Stops all services
echo.
echo BUSINESS USAGE:
echo 1. Double-click "Start TechFlow" on desktop
echo 2. System starts automatically (web + file monitor)
echo 3. Browser opens to http://127.0.0.1:8000
echo 4. Drop files in data folders - they process automatically
echo.
pause
