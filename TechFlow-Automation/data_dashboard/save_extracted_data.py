import os
import django
import json
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_dashboard.settings')
django.setup()

from records.models import Form
from src.parsers.form_parser import parse_html_form

def save_extracted_data(file_path):
    """
    Extracts data from an HTML form and saves it to the database.

    Args:
        file_path (str): Path to the HTML form file.
    """
    extracted_data = parse_html_form(file_path)

    # Convert submitted_at to datetime
    submitted_at = extracted_data.get('submitted_at')
    if submitted_at:
        try:
            extracted_data['submitted_at'] = datetime.strptime(submitted_at, '%Y-%m-%dT%H:%M')
        except ValueError:
            extracted_data['submitted_at'] = None

    # Save to database
    form = Form(
        name=extracted_data.get('name', ''),
        email=extracted_data.get('email', ''),
        phone=extracted_data.get('phone', ''),
        company=extracted_data.get('company', ''),
        service=extracted_data.get('service', ''),
        message=extracted_data.get('message', ''),
        priority=extracted_data.get('priority', ''),
        submitted_at=extracted_data.get('submitted_at')
    )
    form.save()
    print(f"Saved form: {form}")

# Example usage
if __name__ == "__main__":
    save_extracted_data('TechFlow-Automation/data/forms/contact_form_2.html')
