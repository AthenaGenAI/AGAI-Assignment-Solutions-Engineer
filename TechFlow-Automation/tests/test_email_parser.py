import sys
import pandas as pd
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.records import Contact, Invoice
from src.validation.validator import validate_email, validate_phone, validate_amount, validate_date
from src.parsers.email_parser import parse_eml_file, extract_contact_info_from_body, extract_invoice_info_from_body, detect_email_type
from src.logging.logger import setup_logger

logger = setup_logger("data_pipeline")
contacts = []
invoices = []

test_files = [
        'data/emails/email_01.eml',
        'data/emails/email_02.eml',
        'data/emails/email_03.eml',
        'data/emails/email_04.eml',
        'data/emails/email_05.eml',
        'data/emails/email_06.eml',
        'data/emails/email_07.eml',
        'data/emails/email_08.eml',
        'data/emails/email_09.eml',
        'data/emails/email_10.eml',
]

for filename in test_files:
    if not os.path.exists(filename):
        logger.warning(f"File not found: {filename}")
        continue

    data = parse_eml_file(filename)
    email_type = detect_email_type(data['body'])
    logger.info(f"Processing file: {filename} (type: {email_type})")

    if email_type == "client":
        info = extract_contact_info_from_body(data['body'])
        if validate_email(info['email']) and validate_phone(info['phone']):
            contact = Contact(**info)
            contacts.append(contact)
            logger.info(f"Valid contact: {contact.email}")
        else:
            logger.warning(f"Invalid contact data in {filename}: {info}")

    elif email_type == "invoice":
        inv = extract_invoice_info_from_body(data['body'])
        if (validate_amount(inv['net_amount']) and
            validate_amount(inv['vat']) and
            validate_amount(inv['total_amount']) and
            validate_date(inv['date'])):
            invoice = Invoice(**inv)
            invoices.append(invoice)
            logger.info(f"Valid invoice: {invoice.invoice_number}")
        else:
            logger.warning(f"Invalid invoice data in {filename}: {inv}")

    else:
        logger.warning(f"Unknown email type in {filename}")

# (Optional) Εκτύπωσε ή κάνε export τα results στο τέλος:
print("Contacts extracted:", [c.__dict__ for c in contacts])
print("Invoices extracted:", [i.__dict__ for i in invoices])

try:
    if contacts:
        contacts_df = pd.DataFrame([c.__dict__ for c in contacts])
        contacts_df.to_excel("contacts_export.xlsx", index=False)
        logger.info("Exported %d contacts to contacts_export.xlsx", len(contacts))
    else:
        logger.info("No contacts found for export.")

    if invoices:
        invoices_df = pd.DataFrame([i.__dict__ for i in invoices])
        invoices_df.to_excel("invoices_export.xlsx", index=False)
        logger.info("Exported %d invoices to invoices_export.xlsx", len(invoices))
    else:
        logger.info("No invoices found for export.")
except Exception as e:
    logger.error("Failed to export to Excel: %s", e)


if contacts:
    contacts_df = pd.DataFrame([c.__dict__ for c in contacts])
    print("\n--- Contacts ---\n", contacts_df.to_string(index=False))

if invoices:
    invoices_df = pd.DataFrame([i.__dict__ for i in invoices])
    print("\n--- Invoices ---\n", invoices_df.to_string(index=False))
