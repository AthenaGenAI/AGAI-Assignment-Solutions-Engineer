from django.core.management.base import BaseCommand
import pandas as pd
from records.models import Contact, Invoice, Form, Email, Template

class Command(BaseCommand):
    help = 'Export all data to Excel files'

    def handle(self, *args, **kwargs):
        contacts = list(Contact.objects.all().values())
        pd.DataFrame(contacts).to_excel('contacts_export.xlsx', index=False)
        invoices = list(Invoice.objects.all().values())
        pd.DataFrame(invoices).to_excel('invoices_export.xlsx', index=False)
        forms = list(Form.objects.all().values())
        pd.DataFrame(forms).to_excel('forms_export.xlsx', index=False)
        emails = list(Email.objects.all().values())
        pd.DataFrame(emails).to_excel('emails_export.xlsx', index=False)
        templates = list(Template.objects.all().values())
        pd.DataFrame(templates).to_excel('templates_export.xlsx', index=False)
        self.stdout.write(self.style.SUCCESS('Exported all records!'))
