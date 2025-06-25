# urls.py
from django.urls import path
from .views import InvoiceListAPIView

urlpatterns = [
    path('invoices/', InvoiceListAPIView.as_view(), name='invoice_list_api'),
]
