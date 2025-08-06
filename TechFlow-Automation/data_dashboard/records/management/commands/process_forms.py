import os
import sys
from django.core.management.base import BaseCommand
from datetime import datetime

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../src')))

from parsers.form_parser import parse_html_form
from records.models import Contact, Form

class Command(BaseCommand):
    help = 'Process HTML forms and create Contact and Form records in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--forms-dir',
            type=str,
            default='../../dummy_data/forms/',
            help='Directory containing HTML form files'
        )

    def handle(self, *args, **options):
        forms_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 
            options['forms_dir']
        ))
        
        if not os.path.exists(forms_dir):
            self.stdout.write(
                self.style.ERROR(f'Forms directory not found: {forms_dir}')
            )
            return
        
        processed_count = 0
        contact_count = 0
        form_count = 0
        
        self.stdout.write(f"Processing forms from: {forms_dir}")
        self.stdout.write("=" * 50)
        
        for form_file in os.listdir(forms_dir):
            if form_file.endswith('.html'):
                form_path = os.path.join(forms_dir, form_file)
                form_data = parse_html_form(form_path)
                
                if form_data:
                    processed_count += 1
                    self.stdout.write(f"\nProcessing: {form_file}")
                    
                    # Create or get contact
                    contact = self.create_contact_from_form(form_data)
                    if contact and hasattr(contact, '_created'):
                        contact_count += 1
                    
                    # Create form record
                    form_record = self.create_form_record(form_data)
                    if form_record and hasattr(form_record, '_created'):
                        form_count += 1
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(
            self.style.SUCCESS("PROCESSING COMPLETE")
        )
        self.stdout.write("=" * 50)
        self.stdout.write(f"Forms processed: {processed_count}")
        self.stdout.write(f"New contacts created: {contact_count}")
        self.stdout.write(f"Form records created: {form_count}")
        self.stdout.write(f"Total contacts in database: {Contact.objects.count()}")
        self.stdout.write(f"Total forms in database: {Form.objects.count()}")

    def create_contact_from_form(self, form_data):
        """Create a new contact record from form data"""
        try:
            # Use get_or_create to avoid duplicates
            contact, created = Contact.objects.get_or_create(
                email=form_data.get('email'),
                defaults={
                    'name': form_data.get('name', ''),
                    'phone': form_data.get('phone', ''),
                    'company': form_data.get('company', ''),
                    'position': '',
                    'status': 'Pending'
                }
            )
            
            if created:
                self.stdout.write(f"  ✓ New contact: {contact.name} ({contact.email})")
                contact._created = True
            else:
                self.stdout.write(f"  → Contact exists: {contact.email}")
                contact._created = False
            
            return contact
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"  ✗ Error creating contact: {e}")
            )
            return None

    def create_form_record(self, form_data):
        """Create a new form record in the database"""
        try:
            # Parse submitted_at if it exists
            submitted_at = None
            if form_data.get('submitted_at'):
                try:
                    submitted_at = datetime.strptime(form_data.get('submitted_at'), '%Y-%m-%d %H:%M:%S')
                except:
                    submitted_at = datetime.now()
            else:
                submitted_at = datetime.now()
            
            # Use get_or_create to avoid duplicates
            form_record, created = Form.objects.get_or_create(
                email=form_data.get('email'),
                service=form_data.get('service'),
                defaults={
                    'name': form_data.get('name', ''),
                    'phone': form_data.get('phone', ''),
                    'company': form_data.get('company', ''),
                    'message': form_data.get('message', ''),
                    'priority': form_data.get('priority', ''),
                    'submitted_at': submitted_at
                }
            )
            
            if created:
                self.stdout.write(f"  ✓ New form record: {form_record.service}")
                form_record._created = True
            else:
                self.stdout.write(f"  → Form record exists: {form_record.service}")
                form_record._created = False
            
            return form_record
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"  ✗ Error creating form record: {e}")
            )
            return None