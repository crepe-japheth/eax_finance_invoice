from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .forms import InvoiceForm, InvoiceFileFormSet, InvoiceStatusUpdateForm, UserUpdateForm
from .models import InvoiceFile, User, Invoice, InvoiceStatusHistory
from django.shortcuts import get_object_or_404
from invoice.utils.dashboard_chart import invoice_line_dashboard, get_yearly_status_totals, weekly_invoice_status_chart

from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import UserCreationForm, FirstLoginPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# views.py

User = get_user_model()



class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'invoice/index.html'
    # login_url = 'login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_pending"] = Invoice.objects.filter(status="Pending").count()
        context["total_paid"] = Invoice.objects.filter(status="Paid").count()
        context["total_incomplete"] = Invoice.objects.filter(status="Incomplete").count()

        today = timezone.now().date()
        today_invoices = Invoice.objects.filter(created_at__date=today)

        context["increase_today"] = Invoice.objects.filter(created_at__date=today).count()
        context["today_paid"] = Invoice.objects.filter(updated_at__date=today,status="Paind").count()
        context["today_incomplete"] = Invoice.objects.filter(updated_at__date=today,status="Incomplete").count()


        context["invoice_line_dashboard"] = invoice_line_dashboard()
        context["get_yearly_status_totals"] = get_yearly_status_totals()
        context["weekly_invoice_status_chart"] = weekly_invoice_status_chart()
        context["latest_transactions"] = Invoice.objects.order_by("-updated_at")[:5]
        return context




class CreateInvoiceView(View):
    def get(self, request):
        invoice_form = InvoiceForm()
        file_formset = InvoiceFileFormSet(queryset=InvoiceFile.objects.none())
        return render(request, 'invoice/create_invoice.html', {
            'invoice_form': invoice_form,
            'file_formset': file_formset,
        })

    def post(self, request):
        invoice_form = InvoiceForm(request.POST)
        file_formset = InvoiceFileFormSet(request.POST, request.FILES, queryset=InvoiceFile.objects.none())

        if invoice_form.is_valid() and file_formset.is_valid():
            invoice = invoice_form.save(commit=False)
            user = User.objects.get(id=1)
            invoice.created_by = user #request.user
            invoice.save()

            for file_form in file_formset:
                if file_form.cleaned_data.get('file'):
                    file_instance = file_form.save(commit=False)
                    file_instance.invoice = invoice
                    file_instance.save()

            return redirect('invoice')  # Or wherever you want

        return render(request, 'invoice/create_invoice.html', {
            'invoice_form': invoice_form,
            'file_formset': file_formset,
        })
    
class EditInvoiceView(View):
    def get(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
        invoice_form = InvoiceForm(instance=invoice)
        file_formset = InvoiceFileFormSet(instance=invoice)
        return render(request, 'invoice/edit_invoice.html', {
            'invoice_form': invoice_form,
            'file_formset': file_formset,
            'invoice': invoice
        })

    def post(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
        invoice_form = InvoiceForm(request.POST, instance=invoice)
        file_formset = InvoiceFileFormSet(request.POST, request.FILES, instance=invoice, prefix='files')
        if invoice_form.is_valid() and file_formset.is_valid():
            print(invoice_form.errors)
            invoice = invoice_form.save()
            file_formset.save()
            return redirect('invoice_detail', pk=invoice.pk)

        return render(request, 'invoice/edit_invoice.html', {
            'invoice_form': invoice_form,
            'file_formset': file_formset,
            'invoice': invoice
        })


class InvoiceView(ListView):
    model = Invoice
    template_name = 'invoice/invoice.html'
    context_object_name = "invoices"



# class RegisterView(TemplateView):
#     template_name = 'invoice/register.html'


class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = "invoice/invoice_detail.html"
    context_object_name = "invoice"


def is_superuser(user):
    """Check if user is a superuser"""
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def create_user_view(request):
    """View to create a new user - only accessible by superusers"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('user')  # Redirect to user list page
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()
    
    return render(request, 'invoice/register.html', {'form': form})

@login_required
def first_login_password_change(request):
    """View for users to change password on first login"""
    # If user doesn't need to change password, redirect to home
    if not request.user.force_password_change:
        return redirect('index')
        
    if request.method == 'POST':
        form = FirstLoginPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to keep the user logged in
            update_session_auth_hash(request, user)
            
            # Mark that the user has changed their password
            user.force_password_change = False
            user.save()
            
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
    else:
        form = FirstLoginPasswordChangeForm(request.user)
    
    return render(request, 'invoice/first_login.html', {'form': form})

@login_required
def user_login_router(request):
    """Route users after login based on whether they need to change password"""
    if request.user.force_password_change:
        return redirect('first_login_password_change')
    else:
        # Direct to appropriate dashboard based on user role
        if request.user.is_superuser:
            return redirect('index')
        elif request.user.user_role == 'finance_manager':
            return redirect('index')
        else:  # invoice_manager
            return redirect('index')

class UserView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = "users"
    template_name = "invoice/users.html"





# class IsFinanceManagerMixin(UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.user_role == 'finance_manager'

class InvoiceStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    form_class = InvoiceStatusUpdateForm
    template_name = 'invoice/invoice_status_update.html'
    context_object_name = 'invoice'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # pass user to the form
        return kwargs

    def form_valid(self, form):
        invoice = form.instance
        old_status = invoice.status
        new_status = form.cleaned_data['status']
        comment = self.request.POST.get('comment', '')

        # Save new invoice status
        response = super().form_valid(form)

        # Save status change history
        if old_status != new_status:
            InvoiceStatusHistory.objects.create(
                invoice=invoice,
                previous_status=old_status,
                new_status=new_status,
                comment=comment if new_status == 'Incomplete' else '',
                changed_by=self.request.user
            )
        return response

    def get_success_url(self):
        return reverse_lazy('invoice_detail', kwargs={'pk': self.object.pk})  # Or wherever you want to redirect


class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoice')  # Redirect to invoice list after deletion
    template_name = 'invoice/invoice_confirm_delete.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'invoice/user_update.html'
    success_url = reverse_lazy('user')  # Redirect to user list after update
    
class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('user')  # Redirect to user list after deletion
    template_name = 'invoice/user_confirm_delete.html'
