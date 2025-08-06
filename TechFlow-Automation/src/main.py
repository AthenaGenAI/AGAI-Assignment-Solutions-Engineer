from src.utils.records import Contact, Invoice

if email_type == "client":
    info = extract_contact_info_from_body(data['body'])
    contact = Contact(**info)
    # μπορείς να τον προσθέσεις σε λίστα, να τον κάνεις export κτλ.
elif email_type == "invoice":
    inv = extract_invoice_info_from_body(data['body'])
    invoice = Invoice(**inv)
    # προσθήκη σε λίστα invoices κλπ.
