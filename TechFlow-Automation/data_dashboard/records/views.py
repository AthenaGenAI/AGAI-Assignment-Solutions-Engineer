from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

# Create your views here.
from django.shortcuts import render
from .models import Contact, Invoice

from django.shortcuts import render, get_object_or_404, redirect
from .models import Invoice
from django.shortcuts import get_object_or_404, redirect
from .models import Email  # Import your Email model
from records.models import Form, Contact

def dashboard_view(request):
    forms = Form.objects.all()
    contacts = Contact.objects.all()
    return render(request, 'records/dashboard.html', {'forms': forms, 'contacts': contacts})
def email_list(request):
    emails = Email.objects.all()  # Replace with your actual model/query
    return render(request, 'records/email_list.html', {'emails': emails})

def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        contact.delete()
        return redirect('contact_list')
    return render(request, 'records/contact_confirm_delete.html', {'contact': contact})

def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        invoice.delete()
        return redirect('invoice_list')
    return render(request, 'records/invoice_confirm_delete.html', {'invoice': invoice})

def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        status = request.POST.get("status")
        if status in ["Pending", "Approved", "Rejected"]:
            contact.status = status
            contact.save()
        # Optionally update other fields here
        return redirect('contact_list')
    return render(request, 'records/contact_edit.html', {'contact': contact})

def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        status = request.POST.get("status")
        if status in ["Pending", "Approved", "Rejected"]:
            invoice.status = status
            invoice.save()
        # Optionally update other fields here
        return redirect('invoice_list')
    return render(request, 'records/invoice_edit.html', {'invoice': invoice})

def contact_list(request):
    status = request.GET.get('status')
    if status:
        contacts = Contact.objects.filter(status=status)
    else:
        contacts = Contact.objects.all()
    return render(request, 'records/contact_list.html', {'contacts': contacts})

def invoice_list(request):
    status = request.GET.get('status')
    if status:
        invoices = Invoice.objects.filter(status=status)
    else:
        invoices = Invoice.objects.all()
    return render(request, 'records/invoice_list.html', {'invoices': invoices})

def dashboard_home(request):
    # Add logic to get real data from your models
    pending_invoices = Invoice.objects.filter(status='Pending').count()
    pending_contacts = Contact.objects.filter(status='Pending').count()
    context = {
        'pending_invoices': pending_invoices,
        'pending_contacts': pending_contacts,
        'processed_today': 47,
        'errors_warnings': 3,
        'monthly_savings': 2340,
        'recent_activities': [
            {
                'type': 'Email',
                'source': 'sofia@greenfood.gr',
                'status': 'Pending',
                'time': '2 min ago'
            },
            # Add more activities...
        ]
    }
    return render(request, 'records/dashboard_home.html', context)

def form_list(request):
    # Fetch all forms from the database
    forms = Form.objects.all()
    return render(request, 'records/form_list.html', {
        'forms': forms,
        'fields': ['name', 'email', 'phone', 'company', 'service', 'message', 'submitted_at', 'priority']
    })

def template_list(request):
    # Logic to fetch and display templates
    templates = []  # Replace with actual template fetching logic
    return render(request, 'records/template_list.html', {'templates': templates})

def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, 'records/contact_detail.html', {'contact': contact})

def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'records/invoice_detail.html', {'invoice': invoice})

def serve_invoice_html(request, invoice_id):
    import os
    from django.http import HttpResponse, Http404
    from django.conf import settings
    
    # Construct the path to the invoice HTML file
    invoice_file_path = os.path.join(settings.BASE_DIR, '..', 'data', 'invoices', f'invoice_{invoice_id}.html')
    
    try:
        with open(invoice_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return HttpResponse(content, content_type='text/html')
    except FileNotFoundError:
        raise Http404("Invoice not found")

@csrf_exempt
def form_delete(request, pk):
    form = get_object_or_404(Form, pk=pk)
    if request.method == "POST":
        form.delete()
        return redirect('form_list')
    return render(request, 'records/form_confirm_delete.html', {'form': form})

def update_status(request, form_id):
    form = get_object_or_404(Form, id=form_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Approved', 'Rejected']:
            form.status = new_status
            form.save()
            return redirect('form_list')

    return render(request, 'records/update_status.html', {'form': form})

def invoice_update_status(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Approved', 'Rejected']:
            invoice.status = new_status
            invoice.save()
            return redirect('invoice_list')

    return render(request, 'records/invoice_update_status.html', {'invoice': invoice})

def add_contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        company = request.POST.get("company")
        service = request.POST.get("service")

        # Check for duplicates
        if Contact.objects.filter(Q(name=name) & Q(email=email) & Q(phone=phone) & Q(company=company) & Q(service=service)).exists():
            return JsonResponse({"error": "Duplicate contact detected."})

        # Add new contact
        Contact.objects.create(name=name, email=email, phone=phone, company=company, service=service)
        return JsonResponse({"success": "Contact added successfully."})


def add_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        company = request.POST.get("company")
        service = request.POST.get("service")

        # Check for duplicates
        if Form.objects.filter(Q(name=name) & Q(email=email) & Q(phone=phone) & Q(company=company) & Q(service=service)).exists():
            return JsonResponse({"error": "Duplicate form detected."})

        # Add new form
        Form.objects.create(name=name, email=email, phone=phone, company=company, service=service)
        return JsonResponse({"success": "Form added successfully."})


def add_invoice(request):
    if request.method == "POST":
        invoice_number = request.POST.get("invoice_number")
        date = request.POST.get("date")
        customer = request.POST.get("customer")
        amount = request.POST.get("amount")

        # Check for duplicates
        if Invoice.objects.filter(Q(invoice_number=invoice_number) & Q(date=date) & Q(customer=customer) & Q(amount=amount)).exists():
            return JsonResponse({"error": "Duplicate invoice detected."})

        # Add new invoice
        Invoice.objects.create(invoice_number=invoice_number, date=date, customer=customer, amount=amount)
        return JsonResponse({"success": "Invoice added successfully."})

def email_detail(request, pk):
    email = get_object_or_404(Email, pk=pk)
    return render(request, 'records/email_detail.html', {'email': email})

def email_delete(request, pk):
    email = get_object_or_404(Email, pk=pk)
    if request.method == "POST":
        email.delete()
        return redirect('email_list')
    return render(request, 'records/email_confirm_delete.html', {'email': email})