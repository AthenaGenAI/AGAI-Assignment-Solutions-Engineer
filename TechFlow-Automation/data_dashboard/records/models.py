from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return f"{self.name} ({self.email})"
    
class Email(models.Model):
    subject = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField()

    def __str__(self):
        return self.subject

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=100)
    date = models.CharField(max_length=50)
    supplier = models.CharField(max_length=200)
    net_amount = models.CharField(max_length=50)
    vat = models.CharField(max_length=50)
    total_amount = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return self.invoice_number

class Form(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    company = models.CharField(max_length=200)
    service = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    priority = models.CharField(max_length=50, blank=True)
    submitted_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return f"{self.name} ({self.email})"

class Template(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
