import os
import django
from email import message_from_file
from datetime import datetime
from records.models import Email

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_dashboard.settings')
django.setup()

def populate_emails():
    data_folder = os.path.join(os.getcwd(), 'data', 'emails')
    email_files = [f for f in os.listdir(data_folder) if f.endswith('.eml')]

    for email_file in email_files:
        file_path = os.path.join(data_folder, email_file)
        with open(file_path, 'r') as f:
            msg = message_from_file(f)

            sender = msg['From']
            recipient = msg['To']
            subject = msg['Subject']
            sent_at = msg['Date']

            try:
                sent_at = datetime.strptime(sent_at, '%a, %d %b %Y %H:%M:%S %z')
            except ValueError:
                sent_at = datetime.now()

            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

            Email.objects.create(
                sender=sender,
                recipient=recipient,
                subject=subject,
                body=body,
                sent_at=sent_at
            )

    print(f"Successfully populated {len(email_files)} emails into the database.")

if __name__ == "__main__":
    populate_emails()
