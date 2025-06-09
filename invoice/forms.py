from django import forms
from .models import Invoice, InvoiceFile, Contract
from django.forms import inlineformset_factory
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.forms import UserChangeForm
from django.utils import timezone


User = get_user_model()
# from .models import User


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'date_received', 'payment_due_date', 'customer_name', 'amount', 'contract','EBM_invoice','CIT_declaration','good_received_note','delivery_note','profoma', 'contract_copy', 'final_notification_letter', 'tender_evaluation_report', 'perfomance_guaranty', 'advance_security', 'tender_advertisement', 'requisition_form', 'official_appointment_of_receiving_committee', 'evaluation_report_of_previous_period', 'attendance_list', 'mission_clearance_signed_at_destination','purchase_order']
        widgets = {
            'date_received': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'payment_due_date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'invoice_number': forms.TextInput(attrs={'type': 'text', 'class':'form-control'}),
            'customer_name': forms.TextInput(attrs={'type': 'text', 'class':'form-control'}),
            'contract': forms.Select(attrs={'class':'form-control select2'}),
            'amount': forms.NumberInput(attrs={'type': 'number', 'class':'form-control'}),
            'EBM_invoice':forms.CheckboxInput(attrs={'class': 'filled-in chk-col-success'}),
            'CIT_declaration':forms.CheckboxInput(attrs={'class': 'filled-in chk-col-success'}),
            'good_received_note':forms.CheckboxInput(attrs={'class': 'filled-in chk-col-success'}),
            'delivery_note':forms.CheckboxInput(attrs={'class': 'filled-in chk-col-success'}),
            'purchase_order':forms.CheckboxInput(attrs={'class': 'filled-in chk-col-success'}),
            'profoma':forms.CheckboxInput(attrs={'class': 'filled-in chk-col-success'}),
            'contract_copy':forms.CheckboxInput(attrs={'class': 'filled-in chk-col-success'}),
            'final_notification_letter':forms.CheckboxInput(attrs={'class': 'filled-in chk-col-success'}),
            'tender_evaluation_report':forms.CheckboxInput(attrs={'class': 'filled-in chk-col-success'}),
            'perfomance_guaranty':forms.CheckboxInput(attrs={'class': 'filled-in chk-col-success'}),
            'advance_security':forms.CheckboxInput(attrs={'class': 'filled-in chk-col-success'}),
            'tender_advertisement':forms.CheckboxInput(attrs={'class': 'filled-in chk-col-success'}),
            'requisition_form':forms.CheckboxInput(attrs={'class': 'filled-in chk-col-success'}),
            'official_appointment_of_receiving_committee':forms.CheckboxInput(attrs={'class': 'filled-in chk-col-success'}),
            'evaluation_report_of_previous_period':forms.CheckboxInput(attrs={'class': 'filled-in chk-col-success'}),
            'attendance_list':forms.CheckboxInput(attrs={'class': 'filled-in chk-col-success'}),
            'mission_clearance_signed_at_destination':forms.CheckboxInput(attrs={'class': 'filled-in chk-col-success'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.now().date()
        self.fields['contract'].queryset = Contract.objects.filter(end_at__gte=today)




InvoiceFileFormSet = inlineformset_factory(
    Invoice,
    InvoiceFile,
    fields=('file', 'description'),
    extra=1,
    can_delete=True,  # Allow deletion of existing files
    widgets={
        'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        'description': forms.TextInput(attrs={'placeholder': 'e.g. Quatation, LPO, Receipt', 'class': 'form-control'}),
    }
)






class UserCreationForm(UserCreationForm):
    """
    A form for creating new users with all required fields.
    """
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control ps-15 bg-transparent',
            'placeholder': 'Enter Password'
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control ps-15 bg-transparent',
            'placeholder': 'Confirm Password'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'user_role', 'profile_pic','password1', 'password2', 'force_password_change')
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control ps-15 bg-transparent', 'placeholder':'User Name'}),

            'email': forms.EmailInput(attrs={'class':'form-control ps-15 bg-transparent', 'placeholder':'User Email'}),

            'profile_pic': forms.FileInput(attrs={'class':'form-control ps-15 bg-transparent', 'placeholder':'Profile Picture'}),

            'user_role': forms.Select(attrs={'class':'form-control ps-15 bg-transparent'}),

        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Split full name into first name and last name
        full_name = self.cleaned_data.get('full_name', '')
        name_parts = full_name.split(' ', 1)
        
        user.first_name = name_parts[0]
        if len(name_parts) > 1:
            user.last_name = name_parts[1]
        
        user.email = self.cleaned_data['email']
        user.user_role = self.cleaned_data['user_role']
        user.force_password_change = self.cleaned_data.get('force_password_change', True)
        
        if commit:
            user.save()
        return user

class FirstLoginPasswordChangeForm(PasswordChangeForm):
    """
    A form for changing password on first login.
    """
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].help_text = "Enter the temporary password you were provided."
        self.fields['new_password1'].help_text = "Enter a new password you'll remember."






class InvoiceStatusUpdateForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control' ,"rows":"2" ,"cols":"50"}), required=False, help_text="Required if status is set to 'Incomplete'")

    class Meta:
        model = Invoice
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Pass user from view
        self.invoice_instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        comment = self.data.get('comment')  # Get from POST data
        if status == 'Incomplete' and not comment.strip():
            raise forms.ValidationError("Comment is required when marking invoice as Incomplete.")
        return cleaned_data
    




class UserUpdateForm(UserChangeForm):
    """
    Form for updating user profiles with additional fields from custom User model.
    """
    password = None  # Remove password field from the form
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_pic', 'user_role', 'is_active']
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'user_role': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom styling to form fields
        for field in self.fields:
            if field != 'profile_pic' and field != 'user_role':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Only superusers can change user_role
        user = kwargs.get('instance', None)
        if 'request' in kwargs and kwargs['request'].user.user_role != 'superuser':
            self.fields['user_role'].disabled = True
            # If regular user is updating their profile, remove admin fields
            if user and user == kwargs['request'].user:
                del self.fields['is_active']



class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['contract_with', 'started_at', 'end_at', 'contract_file']
        widgets = {
            'started_at': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'end_at': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'contract_file': forms.FileInput(attrs={'class':'form-control'}),
            'contract_with': forms.TextInput(attrs={'type': 'text', 'class':'form-control'}),
        }
