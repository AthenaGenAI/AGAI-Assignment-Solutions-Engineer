import os
import sys
import django
from email import message_from_file
from datetime import datetime
from django.db import transaction

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_dir)

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_dashboard.settings')
django.setup()

from records.models import Email

@transaction.atomic
def run():
    # Go up to the TechFlow-Automation directory and then into data/emails
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    data_folder = os.path.join(base_dir, 'data', 'emails')
    print(f"Looking for emails in: {data_folder}")
    
    if not os.path.exists(data_folder):
        print(f"Error: Directory {data_folder} does not exist")
        return
    
    email_files = [f for f in os.listdir(data_folder) if f.endswith('.eml')]
    print(f"Found {len(email_files)} email files: {email_files}")

    for email_file in email_files:
        file_path = os.path.join(data_folder, email_file)
        print(f"Processing file: {email_file}")
        try:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    msg = message_from_file(f)
            except UnicodeDecodeError:
                # Try with different encoding if utf-8 fails
                with open(file_path, 'r', encoding='latin-1') as f:
                    msg = message_from_file(f)

            sender = msg['From']
            recipient = msg['To']
            subject = msg['Subject']
            sent_at = msg['Date']
            
            print(f"  Sender: {sender}")
            print(f"  Subject: {subject}")

            try:
                sent_at = datetime.strptime(sent_at, '%a, %d %b %Y %H:%M:%S %z')
            except (ValueError, TypeError):
                sent_at = datetime.now()

            # Get body content
            if msg.is_multipart():
                body = ""
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            body += payload.decode('utf-8', errors='ignore')
                        else:
                            body += part.get_payload()
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode('utf-8', errors='ignore')
                else:
                    body = msg.get_payload()
            
            # Ensure the body is properly decoded
            if isinstance(body, bytes):
                body = body.decode('utf-8', errors='ignore')
            
            # Handle Unicode escape sequences
            try:
                body = body.encode('utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')
            except (UnicodeDecodeError, UnicodeEncodeError):
                pass  # Keep the original body if conversion fails

            email = Email.objects.create(
                sender=sender or "",
                recipient=recipient or "",
                subject=subject or "",
                body=body,
                sent_at=sent_at
            )
            print(f"  Successfully created email with ID: {email.id}")
            
        except Exception as e:
            print(f"  Error processing {email_file}: {e}")

    print(f"Successfully populated {len(email_files)} emails into the database.")

if __name__ == "__main__":
    run()
