import os
import shutil
import time
from datetime import datetime

def create_test_email(email_number):
    """Create a test email file"""
    email_content = f"""From: Test User {email_number} <test{email_number}@example.com>
To: info@techflow-solutions.gr
Subject: Test Email {email_number} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')}
Content-Type: text/plain; charset=UTF-8

This is a test email number {email_number}.
Created automatically at {datetime.now()}.

Best regards,
Test User {email_number}
"""
    
    # Get the data directory path
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_emails_path = os.path.join(base_dir, '..', 'data', 'emails')
    data_emails_path = os.path.abspath(data_emails_path)
    
    if not os.path.exists(data_emails_path):
        print(f"Creating directory: {data_emails_path}")
        os.makedirs(data_emails_path, exist_ok=True)
    
    filename = f"test_email_{email_number}_{int(time.time())}.eml"
    filepath = os.path.join(data_emails_path, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(email_content)
    
    print(f"Created test email: {filepath}")
    return filepath

def create_test_form(form_number):
    """Create a test form file"""
    form_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Test Contact Form {form_number}</title>
</head>
<body>
    <form>
        <input type="text" name="name" value="Test Contact {form_number}" />
        <input type="email" name="email" value="contact{form_number}@example.com" />
        <textarea name="message">This is a test message from contact form {form_number}.
Created at {datetime.now()}.</textarea>
        <input type="submit" value="Submit" />
    </form>
</body>
</html>"""
    
    # Get the data directory path
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_forms_path = os.path.join(base_dir, '..', 'data', 'forms')
    data_forms_path = os.path.abspath(data_forms_path)
    
    if not os.path.exists(data_forms_path):
        print(f"Creating directory: {data_forms_path}")
        os.makedirs(data_forms_path, exist_ok=True)
    
    filename = f"test_form_{form_number}_{int(time.time())}.html"
    filepath = os.path.join(data_forms_path, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(form_content)
    
    print(f"Created test form: {filepath}")
    return filepath

if __name__ == "__main__":
    print("Creating test files...")
    
    # Create a test email
    create_test_email(1)
    
    # Wait a moment
    time.sleep(2)
    
    # Create a test form
    create_test_form(1)
    
    print("Test files created! If the file watcher is running, these should be automatically processed.")
