from django.urls import path
from . import views
from .views import update_status, invoice_update_status

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),  # This should be first
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/<int:pk>/edit/', views.contact_edit, name='contact_edit'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/<int:pk>/edit/', views.invoice_edit, name='invoice_edit'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    path('invoices/<int:pk>/delete/', views.invoice_delete, name='invoice_delete'),
    path('contacts/<int:pk>/', views.contact_detail, name='contact_detail'),
    path('emails/', views.email_list, name='email_list'),
    path('emails/<int:pk>/', views.email_detail, name='email_detail'),
    path('emails/<int:pk>/delete/', views.email_delete, name='email_delete'),
    path('forms/', views.form_list, name='form_list'),
    path('templates/', views.template_list, name='template_list'),
    path('invoices/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoice-html/<str:invoice_id>/', views.serve_invoice_html, name='serve_invoice_html'),
    path('forms/<int:pk>/delete/', views.form_delete, name='form_delete'),
    path('update-status/<int:form_id>/', update_status, name='form_update_status'),
    path('update-invoice-status/<int:invoice_id>/', invoice_update_status, name='invoice_update_status'),
]