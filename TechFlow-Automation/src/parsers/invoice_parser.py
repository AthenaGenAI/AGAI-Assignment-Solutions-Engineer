from bs4 import BeautifulSoup
import re

def parse_html_invoice(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Extract header details
    invoice_number = soup.find('strong', string=re.compile('Αριθμός:')).next_sibling.strip()
    date = soup.find('strong', string=re.compile('Ημερομηνία:')).next_sibling.strip()
    customer = soup.find('strong', string=re.compile('Πελάτης:')).parent.find_all(text=True)[1].strip()
    
    # Extract summary amounts
    summary_table = soup.find('div', class_='summary').find('table')
    rows = summary_table.find_all('tr')
    net_amount = rows[0].find_all('td')[1].text.strip()
    vat = rows[1].find_all('td')[1].text.strip()
    total_amount = rows[2].find_all('td')[1].text.strip()

    result = {
        'invoice_number': invoice_number,
        'date': date,
        'customer': customer,
        'net_amount': net_amount,
        'vat': vat,
        'total_amount': total_amount
    }
    return result
