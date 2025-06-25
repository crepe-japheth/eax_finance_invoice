# views.py
from rest_framework import generics
from invoice.models import Invoice
from .serializers import InvoiceSerializer

class InvoiceListAPIView(generics.ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

