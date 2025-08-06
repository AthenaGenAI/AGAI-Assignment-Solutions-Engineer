class Contact:
    def __init__(self, name, email, phone, company, position):
        self.name = name
        self.email = email
        self.phone = phone
        self.company = company
        self.position = position

class Invoice:
    def __init__(self, invoice_number, date, supplier, net_amount, vat, total_amount):
        self.invoice_number = invoice_number
        self.date = date
        self.supplier = supplier
        self.net_amount = net_amount
        self.vat = vat
        self.total_amount = total_amount
