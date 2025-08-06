import os
import codecs
from email import message_from_file
from datetime import datetime
from django.db import transaction
from bs4 import BeautifulSoup
from records.models import Email, Form, Invoice


def process_email_file(file_path):
    """Process a single email file and add it to the database"""
    try:
        with transaction.atomic():
            print(f"Processing email file: {file_path}")
            
            # Read and parse email
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    msg = message_from_file(f)
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin-1') as f:
                    msg = message_from_file(f)

            sender = msg['From'] or ""
            recipient = msg['To'] or ""
            subject = msg['Subject'] or ""
            sent_at = msg['Date']

            # Parse date
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

            # Check if email already exists (avoid duplicates)
            if not Email.objects.filter(sender=sender, subject=subject, sent_at=sent_at).exists():
                email = Email.objects.create(
                    sender=sender,
                    recipient=recipient,
                    subject=subject,
                    body=body,
                    sent_at=sent_at
                )
                print(f"✓ Email created with ID: {email.id} from {sender}")

                # --- NEW: Automatically create contact from sender ---
                from records.models import Contact
                import re
                # Try to extract name and email from sender string
                match = re.match(r"(.+?)\s*<(.+?)>", sender)
                if match:
                    name = match.group(1).strip()
                    email_addr = match.group(2).strip()
                else:
                    name = sender
                    email_addr = sender
                # Only create contact if not already present
                if not Contact.objects.filter(email=email_addr).exists():
                    Contact.objects.create(
                        name=name,
                        email=email_addr,
                        phone="",
                        company="",
                        position="",
                        status="Pending"
                    )
                    print(f"✓ Contact created for {name} <{email_addr}>")
                else:
                    print(f"⚠ Contact already exists for {email_addr}, skipping.")
                # --- END NEW ---
            else:
                print(f"⚠ Email already exists, skipping: {subject}")
                
    except Exception as e:
        print(f"✗ Error processing email {file_path}: {e}")


def process_form_file(file_path):
    """Process a single form file and add it to the database"""
    try:
        with transaction.atomic():
            print(f"Processing form file: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract form data (customize based on your form structure)
            name = ""
            email = ""
            message = ""
            
            # Try to find common form field patterns
            name_field = soup.find('input', {'name': 'name'}) or soup.find('input', {'id': 'name'})
            if name_field and name_field.get('value'):
                name = name_field.get('value')
            
            email_field = soup.find('input', {'name': 'email'}) or soup.find('input', {'id': 'email'})
            if email_field and email_field.get('value'):
                email = email_field.get('value')
            
            message_field = soup.find('textarea', {'name': 'message'}) or soup.find('textarea', {'id': 'message'})
            if message_field:
                message = message_field.get_text(strip=True)
            
            # Get filename for reference
            filename = os.path.basename(file_path)
            
            # Check if form already exists (avoid duplicates)
            if not Form.objects.filter(name=name, email=email, message=message).exists():
                form = Form.objects.create(
                    name=name or f"Form from {filename}",
                    email=email or "unknown@example.com",
                    message=message or f"Form content from {filename}",
                    status='pending'
                )
                print(f"✓ Form created with ID: {form.id} from {filename}")
            else:
                print(f"⚠ Form already exists, skipping: {filename}")
                
    except Exception as e:
        print(f"✗ Error processing form {file_path}: {e}")


def process_invoice_file(file_path):
    """Process a single invoice file and add it to the database"""
    try:
        with transaction.atomic():
            print(f"Processing invoice file: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract invoice data (customize based on your invoice structure)
            invoice_number = ""
            customer_name = ""
            amount = 0.0
            
            # Try to find invoice number
            invoice_num_elem = soup.find(text=lambda text: text and 'invoice' in text.lower())
            if invoice_num_elem:
                # Extract invoice number pattern
                import re
                match = re.search(r'TF-\d+-\d+', str(invoice_num_elem))
                if match:
                    invoice_number = match.group()
            
            # Try to find customer name (customize based on your HTML structure)
            customer_elem = soup.find('h2') or soup.find('strong')
            if customer_elem:
                customer_name = customer_elem.get_text(strip=True)
            
            # Try to find amount (customize based on your HTML structure)
            amount_text = soup.find(text=lambda text: text and '€' in text)
            if amount_text:
                import re
                amount_match = re.search(r'(\d+\.?\d*)', amount_text)
                if amount_match:
                    amount = float(amount_match.group(1))
            
            # Get filename for reference
            filename = os.path.basename(file_path)
            if not invoice_number:
                invoice_number = filename.replace('.html', '')
            
            # Check if invoice already exists (avoid duplicates)
            if not Invoice.objects.filter(invoice_number=invoice_number).exists():
                invoice = Invoice.objects.create(
                    invoice_number=invoice_number,
                    customer_name=customer_name or f"Customer from {filename}",
                    amount=amount,
                    status='pending',
                    invoice_date=datetime.now()
                )
                print(f"✓ Invoice created with ID: {invoice.id} - {invoice_number}")
            else:
                print(f"⚠ Invoice already exists, skipping: {invoice_number}")
                
    except Exception as e:
        print(f"✗ Error processing invoice {file_path}: {e}")
