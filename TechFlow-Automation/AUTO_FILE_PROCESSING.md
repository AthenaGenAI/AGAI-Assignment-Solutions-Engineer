# TechFlow Automation - Automatic File Processing

## Overview

The TechFlow Automation system now includes automatic file monitoring and processing capabilities. When new files are added to the data directories, they are automatically processed and added to the database in real-time.

## Features

- **Real-time File Monitoring**: Watches data directories for new files
- **Automatic Email Processing**: New `.eml` files in `data/emails/` are automatically parsed and added to the database
- **Automatic Form Processing**: New `.html` files in `data/forms/` are automatically processed
- **Automatic Invoice Processing**: New `.html` files in `data/invoices/` are automatically processed
- **Duplicate Prevention**: Files that have already been processed are not added again

## How to Use

### 1. Start the File Watcher

**Option A: Using the batch script (Windows)**
```bash
# Double-click or run from command line
start_file_watcher.bat
```

**Option B: Using Django management command**
```bash
# Navigate to the project directory
cd TechFlow-Automation
.\venv\Scripts\activate
cd data_dashboard

# Start the file watcher
python manage.py watch_files

# Or specify a custom path
python manage.py watch_files --path "C:\path\to\your\data"
```

### 2. Add Files to Monitor

Once the file watcher is running, simply add new files to the appropriate directories:

- **Emails**: Drop `.eml` files into `TechFlow-Automation/data/emails/`
- **Forms**: Drop `.html` files into `TechFlow-Automation/data/forms/`
- **Invoices**: Drop `.html` files into `TechFlow-Automation/data/invoices/`

### 3. View Results

- The file watcher will display processing messages in the console
- New records will automatically appear in the web interface
- Visit the respective pages (Emails, Forms, Invoices) to see the new data

## Testing

You can test the system by creating test files:

```bash
cd data_dashboard
python records/utils/create_test_files.py
```

This will create sample email and form files in the data directories.

## Technical Details

### File Processing Logic

- **Email Files (.eml)**: 
  - Extracts sender, recipient, subject, date, and body
  - Handles Unicode characters properly (Greek, Latin, etc.)
  - Prevents duplicate emails based on sender, subject, and date

- **Form Files (.html)**:
  - Extracts name, email, and message from form fields
  - Creates contact records with pending status
  - Prevents duplicate forms based on content

- **Invoice Files (.html)**:
  - Extracts invoice number, customer name, and amount
  - Creates invoice records with pending status
  - Prevents duplicate invoices based on invoice number

### Directory Structure

```
TechFlow-Automation/
├── data/
│   ├── emails/          # Drop .eml files here
│   ├── forms/           # Drop .html form files here
│   └── invoices/        # Drop .html invoice files here
├── data_dashboard/
│   └── records/
│       ├── management/
│       │   └── commands/
│       │       └── watch_files.py    # File watcher command
│       └── utils/
│           ├── file_processors.py    # File processing logic
│           └── create_test_files.py  # Test file generator
└── start_file_watcher.bat           # Windows startup script
```

## Benefits

1. **Real-time Processing**: No need to manually run scripts
2. **Simulates Real Scenarios**: Mimics receiving emails, forms, and invoices
3. **Easy Testing**: Drop files and see immediate results
4. **Robust Error Handling**: Continues processing even if individual files fail
5. **Unicode Support**: Properly handles Greek, Latin, and other character sets

## Stopping the Watcher

To stop the file watcher:
- Press `Ctrl+C` in the terminal where it's running
- Close the command window

## Troubleshooting

- **Files not being processed**: Check that the file watcher is running and monitoring the correct directory
- **Permission errors**: Ensure the application has read/write access to the data directories
- **Encoding issues**: The system automatically handles UTF-8 and Latin-1 encodings
- **Database errors**: Check the Django logs for specific error messages
