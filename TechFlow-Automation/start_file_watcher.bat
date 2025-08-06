@echo off
echo Starting TechFlow File Watcher...
echo This will monitor the data directory for new files and automatically process them.
echo Press Ctrl+C to stop the watcher.
echo.

cd /d "C:\Users\konla\Desktop\Job apps\AGAI-Assignment-Solutions-Engineer\AGAI-Assignment-Solutions-Engineer\TechFlow-Automation"
call venv\Scripts\activate
cd data_dashboard
python manage.py watch_files
