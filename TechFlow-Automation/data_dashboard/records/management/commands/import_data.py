from django.core.management.base import BaseCommand
import pandas as pd
from records.models import Contact, Invoice, Form, Email, Template
from pathlib import Path
# Update the data_dir to point to the correct location
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Go up 3 levels to reach the data_dashboard directory
data_dir = BASE_DIR
class Command(BaseCommand):
    help = 'Import contacts, invoices, forms, emails, and templates from Excel files'

    def handle(self, *args, **kwargs):
        contacts = pd.read_excel(data_dir / 'contacts_export.xlsx')
        for _, row in contacts.iterrows():
            Contact.objects.get_or_create(
                name=row['name'],
                email=row['email'],
                phone=row['phone'],
                company=row['company'],
                position=row.get('position', ''),
                status='Pending'
            )
        invoices = pd.read_excel(data_dir /'invoices_export.xlsx')
        for _, row in invoices.iterrows():
            Invoice.objects.get_or_create(
                invoice_number=row['invoice_number'],
                date=row['date'],
                supplier=row['supplier'],
                net_amount=row['net_amount'],
                vat=row['vat'],
                total_amount=row['total_amount'],
                status='Pending'
            )
        # Import Forms
        try:
            forms = pd.read_excel(data_dir / 'forms_export.xlsx')
            for _, row in forms.iterrows():
                Form.objects.get_or_create(
                    name=row['name'],
                    email=row['email'],
                    phone=row['phone'],
                    company=row['company'],
                    service=row.get('service', ''),
                    message=row.get('message', ''),
                    priority=row.get('priority', ''),
                    submitted_at=row.get('submitted_at', None)
                )
        except Exception:
            pass
        # Import Emails
        try:
            emails = pd.read_excel(data_dir / 'emails_export.xlsx')
            for _, row in emails.iterrows():
                Email.objects.get_or_create(
                    subject=row['subject'],
                    sender=row['sender'],
                    recipient=row['recipient'],
                    body=row.get('body', ''),
                    sent_at=row.get('sent_at', None)
                )
        except Exception:
            pass
        # Import Templates
        try:
            templates = pd.read_excel(data_dir / 'templates_export.xlsx')
            for _, row in templates.iterrows():
                Template.objects.get_or_create(
                    name=row['name'],
                    description=row.get('description', ''),
                    created_at=row.get('created_at', None)
                )
        except Exception:
            pass
        self.stdout.write(self.style.SUCCESS('Imported all records!'))