from django.contrib import admin

# Register your models here.
from .models import Contact, Email, Invoice, Form

admin.site.register(Contact)
admin.site.register(Email)
admin.site.register(Invoice)
admin.site.register(Form)