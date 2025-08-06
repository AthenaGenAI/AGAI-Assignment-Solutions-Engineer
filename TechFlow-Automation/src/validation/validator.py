import re
from datetime import datetime

def validate_email(email_str):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email_str))

def validate_phone(phone_str):
    pattern = r'^[\d\-\+ ]+$'
    return bool(re.match(pattern, phone_str))

def validate_amount(amount_str):
    try:
        amount = float(amount_str.replace('€', '').replace(',', '').strip())
        return amount >= 0
    except Exception:
        return False

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except Exception:
        return False
