import email
from email import policy
import re

def extract_contact_info_from_body(body):
    # Κάνε strip για να φύγουν extra spaces left/right
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    results = {"name": "", "email": "", "phone": "", "company": "", "position": ""}

    for line in lines:
        if "Όνομα:" in line:
            results["name"] = line.split("Όνομα:")[1].strip()
        if "Email:" in line:
            results["email"] = line.split("Email:")[1].strip()
        if "Τηλέφωνο:" in line or "Κινητό:" in line:
            results["phone"] = line.split(":", 1)[1].strip()
        if "Εταιρεία:" in line:
            results["company"] = line.split("Εταιρεία:")[1].strip()
        if "Θέση:" in line:
            results["position"] = line.split("Θέση:")[1].strip()
    return results


def parse_eml_file(file_path):
    # Άνοιξε σε BINARY mode για να διαβάσει σωστά encoding
    with open(file_path, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=policy.default)

    from_ = msg['From']
    to = msg['To']
    subject = msg['Subject']
    date = msg['Date']

    if msg.is_multipart():
        body = ''
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                payload = part.get_payload(decode=True)
                if payload:
                    body += payload.decode(part.get_content_charset() or 'utf-8')
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode(msg.get_content_charset() or 'utf-8')
        else:
            body = ''

    return {
        'from': from_,
        'to': to,
        'subject': subject,
        'date': date,
        'body': body
    }

import email
from email import policy
import re

def extract_invoice_info_from_body(body):
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    results = {
        "invoice_number": "",
        "date": "",
        "supplier": "",
        "net_amount": "",
        "vat": "",
        "total_amount": ""
    }
    for line in lines:
        if "Αριθμός:" in line:
            results["invoice_number"] = line.split("Αριθμός:")[1].strip()
        if "Ημερομηνία:" in line:
            results["date"] = line.split("Ημερομηνία:")[1].strip()
        if "Προμηθευτής:" in line:
            results["supplier"] = line.split("Προμηθευτής:")[1].strip()
        if "Καθαρή Αξία:" in line:
            results["net_amount"] = line.split("Καθαρή Αξία:")[1].strip()
        if "ΦΠΑ" in line:
            results["vat"] = line.split(":")[1].strip()
        if "Συνολικό Ποσό:" in line:
            results["total_amount"] = line.split("Συνολικό Ποσό:")[1].strip()
    return results



def detect_email_type(body):
    if "Όνομα:" in body or "Κινητό:" in body or "Τηλέφωνο:" in body:
        return "client"
    elif "Αριθμός:" in body and "Προμηθευτής:" in body:
        return "invoice"
    else:
        return "unknown"