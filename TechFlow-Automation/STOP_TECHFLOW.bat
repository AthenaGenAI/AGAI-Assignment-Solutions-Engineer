@echo off
title Stop TechFlow Automation
color 0C
echo.
echo ===============================================
echo     Stopping TechFlow Automation System
echo ===============================================
echo.

echo Stopping Django development server...
taskkill /F /FI "WINDOWTITLE eq TechFlow Web Server*" >nul 2>&1

echo Stopping file monitor...
taskkill /F /FI "WINDOWTITLE eq TechFlow File Monitor*" >nul 2>&1

echo.
echo TechFlow Automation System has been stopped.
echo.
pause
