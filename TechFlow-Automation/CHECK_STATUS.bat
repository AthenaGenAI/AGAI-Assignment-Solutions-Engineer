@echo off
title TechFlow System Status Check
color 0A
echo.
echo ===============================================
echo     TechFlow System Status Check
echo ===============================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate
cd data_dashboard

echo Checking system status...
echo.

echo [1] Checking database records...
python manage.py shell -c "from records.models import Email, Form, Invoice; print(f'📧 Emails: {Email.objects.count()}'); print(f'📝 Forms: {Form.objects.count()}'); print(f'💰 Invoices: {Invoice.objects.count()}')"

echo.
echo [2] Checking latest email...
python manage.py shell -c "from records.models import Email; latest = Email.objects.last(); print(f'Latest: {latest.subject} from {latest.sender}' if latest else 'No emails found')"

echo.
echo [3] Testing web server connection...
curl -s -o nul -w "Web server status: %%{http_code}\n" http://127.0.0.1:8000 2>nul || echo "Web server: Not responding"

echo.
echo ===============================================
echo     Status Check Complete
echo ===============================================
echo.
pause
