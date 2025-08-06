import os
import glob
from django.core.management.base import BaseCommand
from records.models import Contact, Email, Invoice
from bs4 import BeautifulSoup

class Command(BaseCommand):
    help = 'Import dummy data from forms, emails, and invoices.'

    def handle(self, *args, **options):
        self.import_forms()
        self.import_emails()
        self.import_invoices()
        self.stdout.write(self.style.SUCCESS('Dummy data import complete.'))

    def import_forms(self):
        forms_path = os.path.join('..', '..', '..', '..', 'dummy_data', 'forms', '*.html')
        for form_file in glob.glob(forms_path):
            with open(form_file, encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                # Example extraction logic, adjust to your HTML structure
                name = soup.find('span', {'class': 'name'}).text if soup.find('span', {'class': 'name'}) else ''
                email = soup.find('span', {'class': 'email'}).text if soup.find('span', {'class': 'email'}) else ''
                phone = soup.find('span', {'class': 'phone'}).text if soup.find('span', {'class': 'phone'}) else ''
                company = soup.find('span', {'class': 'company'}).text if soup.find('span', {'class': 'company'}) else ''
                message = soup.find('span', {'class': 'message'}).text if soup.find('span', {'class': 'message'}) else ''
                Contact.objects.create(name=name, email=email, phone=phone, company=company, message=message)

    def import_emails(self):
        emails_path = os.path.join('..', '..', '..', '..', 'dummy_data', 'emails', '*.eml')
        for email_file in glob.glob(emails_path):
            with open(email_file, encoding='utf-8') as f:
                lines = f.readlines()
                subject = lines[0].strip() if lines else ''
                sender = lines[1].strip() if len(lines) > 1 else ''
                body = ''.join(lines[2:]) if len(lines) > 2 else ''
                Email.objects.create(subject=subject, sender=sender, body=body)

    def import_invoices(self):
        invoices_path = os.path.join('..', '..', '..', '..', 'dummy_data', 'invoices', '*.html')
        for invoice_file in glob.glob(invoices_path):
            with open(invoice_file, encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                invoice_number = soup.find('span', {'class': 'invoice-number'}).text if soup.find('span', {'class': 'invoice-number'}) else ''
                date = soup.find('span', {'class': 'date'}).text if soup.find('span', {'class': 'date'}) else ''
                customer = soup.find('span', {'class': 'customer'}).text if soup.find('span', {'class': 'customer'}) else ''
                amount = soup.find('span', {'class': 'amount'}).text if soup.find('span', {'class': 'amount'}) else ''
                Invoice.objects.create(invoice_number=invoice_number, date=date, customer=customer, amount=amount)
