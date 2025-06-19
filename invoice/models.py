from datetime import date, timedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

# User = get_user_model()

class User(AbstractUser):
    """
    Custom User model with additional fields for profile and role management.
    """
    USER_ROLE_CHOICES = (
        ('finance_manager', 'Finance Manager'),
        ('invoice_manager', 'Invoice Manager'),
        ('superuser', 'Super User'),
    )
    # Add related_name to avoid clashes with auth.User model
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='invoice_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='invoice_user_set',
        related_query_name='user',
    )
    
    email = models.EmailField(_('email address'), unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    user_role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='superuser')
    force_password_change = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        # Handle user permissions based on role when saving
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            self._set_role_permissions()
    
    def _set_role_permissions(self):
        """Set permissions based on user role"""
        # Clear existing groups
        self.groups.clear()
        
        if self.user_role == 'superuser':
            self.is_staff = True
            self.is_superuser = True
        elif self.user_role == 'finance_manager':
            finance_group, _ = Group.objects.get_or_create(name='Finance Managers')
            self.groups.add(finance_group)
            self.is_staff = True
        elif self.user_role == 'invoice_manager':
            invoice_group, _ = Group.objects.get_or_create(name='Invoice Managers')
            self.groups.add(invoice_group)
            self.is_staff = True
        
        # Save the changes
        self.save(update_fields=['is_staff', 'is_superuser'])


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Incomplete', 'Incomplete'),
    ]

    invoice_number = models.CharField(max_length=50, unique=True)
    date_received = models.DateField()
    payment_due_date = models.DateField()
    customer_name = models.CharField(max_length=255)
    contract = models.ForeignKey('Contract', on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    EBM_invoice = models.BooleanField(blank=True, null=True)
    CIT_declaration = models.BooleanField(blank=True, null=True)
    good_received_note = models.BooleanField(blank=True, null=True)
    delivery_note = models.BooleanField(blank=True, null=True)
    purchase_order = models.BooleanField(blank=True, null=True)
    profoma = models.BooleanField(blank=True, null=True)
    contract_copy = models.BooleanField(blank=True, null=True)
    final_notification_letter = models.BooleanField(blank=True, null=True)
    tender_evaluation_report = models.BooleanField(blank=True, null=True)
    perfomance_guaranty = models.BooleanField(blank=True, null=True)
    advance_security = models.BooleanField(blank=True, null=True)
    tender_advertisement = models.BooleanField(blank=True, null=True)
    requisition_form = models.BooleanField(blank=True, null=True)
    official_appointment_of_receiving_committee = models.BooleanField(blank=True, null=True)
    evaluation_report_of_previous_period = models.BooleanField(blank=True, null=True)
    attendance_list = models.BooleanField(blank=True, null=True)
    mission_clearance_signed_at_destination = models.BooleanField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_invoices')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_invoices')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    received_by_finance = models.BooleanField(default=False)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_invoices')
    received_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.invoice_number} - {self.customer_name}"
    
    def is_overdue(self):
        """Check if the invoice is past due and not paid"""
        return self.status != 'Paid' and date.today() > self.payment_due_date

    def is_approaching_due_date(self, days=3):
        """
        Check if the invoice is approaching its due date within `days`
        and not paid.
        """
        if self.status == 'Paid':
            return False
        today = date.today()
        return today <= self.payment_due_date <= today + timedelta(days=days)



def invoice_file_upload_to(instance, filename):
    return f'invoices/{instance.invoice.invoice_number}/{filename}'

class InvoiceFile(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=invoice_file_upload_to)
    description = models.CharField(max_length=255, blank=True)  # e.g., Contract, Receipt

    def __str__(self):
        return f"File for {self.invoice.invoice_number} - {self.description}"
    

class InvoiceStatusHistory(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='status_history')
    previous_status = models.CharField(max_length=20, choices=Invoice.STATUS_CHOICES)
    new_status = models.CharField(max_length=20, choices=Invoice.STATUS_CHOICES)
    comment = models.TextField(blank=True)  # Required if marked as Incomplete
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.invoice.invoice_number}: {self.previous_status} → {self.new_status} by {self.changed_by}"


class Contract(models.Model):
    contract_with = models.CharField(max_length=200)
    started_at = models.DateField()
    end_at = models.DateField()
    contract_file = models.FileField(upload_to='contract_attachment/', blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def clean(self):
        super().clean()
        if self.started_at and self.end_at and self.started_at >= self.end_at:
            raise ValidationError("Start date must be earlier than end date.")
        
    @property
    def is_active(self):
        today = date.today()
        return self.started_at <= today <= self.end_at

    def __str__(self):
        return self.contract_with


