# TechFlow Automation Project

## Overview
This project automates the processing of emails, forms, and invoices for business workflows. It features a dashboard for monitoring, manual controls, and integration with Excel.

## Getting Started

### Quick Start (Windows)
1. Double-click `START_TECHFLOW.bat` in the `TechFlow-Automation` folder. This will start the TechFlow automation service and open the dashboard in your browser.
2. To stop the service, double-click `STOP_TECHFLOW.bat`.
3. To check the status, double-click `CHECK_STATUS.bat`.

### Manual Start (Advanced)
If you prefer using the command line:
1. Open a terminal and navigate to the project folder:
   ```sh
   cd AGAI-Assignment-Solutions-Engineer/TechFlow-Automation
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```sh
   python data_dashboard/manage.py migrate
   ```
4. Create a superuser (optional, for admin access):
   ```sh
   python data_dashboard/manage.py createsuperuser
   ```
5. Start the development server:
   ```sh
   python data_dashboard/manage.py runserver
   ```
6. Open your browser and go to `http://127.0.0.1:8000/`

## Using the App

- When you start TechFlow (with the batch file or manually), the dashboard opens in your browser.
- **Dashboard:** View the status of all forms, contacts, and invoices in real time. Approve, reject, or manually edit records. See errors and warnings for problematic data. Monitor recent activities and statistics.
- **Email Processing:** Emails in the `data/emails/` folder are automatically processed. Relevant data is extracted and shown in the dashboard.
- **Form Processing:** Forms in the `data/forms/` folder are parsed and validated. You can review and edit them from the dashboard.
- **Invoice Processing:** Invoices in the `data/invoices/` folder are parsed for financial data, VAT, and totals. You can approve or reject invoices from the dashboard.
- **Excel Export:** All processed data is exported to Excel files in the `data_dashboard/data_dashboard/` folder. Open these files with Excel to view or analyze the data.

## Creating Test Data
- Dummy data is provided in the `dummy_data/` folder (emails, forms, invoices).
- To populate the database with test emails:
  ```sh
  python data_dashboard/populate_emails.py
  ```
- For forms and invoices, use the provided scripts or add via the admin panel.

## Error Handling & Logging
- Errors and warnings are shown in the dashboard and logged for review.

## Stopping or Restarting
- Use `STOP_TECHFLOW.bat` to stop the automation service.
- Use `START_TECHFLOW.bat` to restart it.

## Admin Panel
- For advanced management, log in to the Django admin panel at `http://127.0.0.1:8000/admin` using your superuser credentials.

## Testing
- Run unit tests with:
  ```sh
  python data_dashboard/manage.py test
  ```
- Test scripts are in the `tests/` folder.

## Documentation
- Additional documentation is in the `docs/` folder.
- For technical details, see `AUTO_FILE_PROCESSING.md` and `BUSINESS_GUIDE.md`.

## Support
For issues or questions, contact the project maintainer or open an issue on GitHub.

---

**Enjoy automating your business workflows with TechFlow!**
