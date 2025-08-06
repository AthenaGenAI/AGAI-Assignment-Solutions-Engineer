# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import django
from datetime import datetime

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_dashboard.settings')
django.setup()

from parsers.form_parser import parse_html_form
from records.models import Contact, Form

def create_contact_from_form(form_data):
    """Create or update a contact record from form data"""
    try:
        # Check if contact with this email already exists
        existing_contact = Contact.objects.filter(email=form_data.get('email')).first()
        if existing_contact:
            # Update existing contact
            existing_contact.name = form_data.get('name', existing_contact.name)
            existing_contact.phone = form_data.get('phone', existing_contact.phone)
            existing_contact.company = form_data.get('company', existing_contact.company)
            existing_contact.save()
            print(f"Updated contact: {existing_contact.name} ({existing_contact.email})")
            return existing_contact
        
        # Create new contact
        contact = Contact.objects.create(
            name=form_data.get('name', ''),
            email=form_data.get('email', ''),
            phone=form_data.get('phone', ''),
            company=form_data.get('company', ''),
            position='',  # Form doesn't have position field
            status='Pending'
        )
        print(f"Created new contact: {contact.name} ({contact.email})")
        return contact
    except Exception as e:
        print(f"Error creating or updating contact: {e}")
        return None

def create_form_record(form_data):
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
        
        # Create new form record
        form_record = Form.objects.create(
            name=form_data.get('name', ''),
            email=form_data.get('email', ''),
            phone=form_data.get('phone', ''),
            company=form_data.get('company', ''),
            service=form_data.get('service', ''),
            message=form_data.get('message', ''),
            priority=form_data.get('priority', ''),
            submitted_at=submitted_at
        )
        print(f"Created new form record: {form_record.name} - {form_record.service}")
        return form_record
    except Exception as e:
        print(f"Error creating form record: {e}")
        return None

def save_forms_to_excel(output_file):
    # Resolve the absolute path to the HTML forms directory
    forms_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dummy_data/forms/'))
    data = []
    processed_count = 0
    contact_count = 0
    form_count = 0

    print(f"Processing forms from: {forms_dir}")
    
    for form_file in os.listdir(forms_dir):
        if form_file.endswith('.html'):
            form_path = os.path.join(forms_dir, form_file)
            form_data = parse_html_form(form_path)
            
            if form_data:
                # Add to data for Excel export
                data.append(form_data)
                processed_count += 1
                
                # Create contact record from form data
                contact = create_contact_from_form(form_data)
                if contact:
                    contact_count += 1
                
                # Create form record in database
                form_record = create_form_record(form_data)
                if form_record:
                    form_count += 1
                
                print(f"Processed form: {form_file}")

    # Convert the data list of dicts to a DataFrame and save to Excel
    if data:
        fieldnames = ['name', 'email', 'phone', 'company', 'service', 'message', 'submitted_at', 'priority']
        df = pd.DataFrame(data, columns=fieldnames)
        df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"Exported {len(data)} forms to {output_file}")
    else:
        print("No form data found to export")
    
    print(f"\nSummary:")
    print(f"- Forms processed: {processed_count}")
    print(f"- Contacts created: {contact_count}")
    print(f"- Form records created: {form_count}")
    print(f"- Excel file: {output_file}")

if __name__ == '__main__':
    save_forms_to_excel('forms_export.xlsx')