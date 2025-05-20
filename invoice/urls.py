from django.urls import path
from .views import DashboardView, UserView, InvoiceView, CreateInvoiceView, InvoiceDetailView, EditInvoiceView, InvoiceStatusUpdateView

from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'), 
    path('invoice/', InvoiceView.as_view(), name='invoice'), 
    path('user', UserView.as_view(), name='user'), 
    path('invoice/create', CreateInvoiceView.as_view(), name='create_invoice'), 
    path('invoice/<int:pk>/detail', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoice/<int:pk>/edit/', EditInvoiceView.as_view(), name='edit_invoice'),
    path('invoice/<int:pk>/status-update/', InvoiceStatusUpdateView.as_view(), name='invoice_status_update'),
    path('invoices/<int:pk>/delete/', views.InvoiceDeleteView.as_view(), name='invoice-delete'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),
    path('users/create/', views.create_user_view, name='create_user'),
    
    # Login related URLs
    path('login/', auth_views.LoginView.as_view(template_name='invoice/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # First-time login password change
    path('password/change/first-login/', views.first_login_password_change, name='first_login_password_change'),
    
    # Login router for directing users based on role and password change status
    path('login/router/', views.user_login_router, name='login_router'),
    
    # Additional password management (optional)
    path('password/reset/', 
        auth_views.PasswordResetView.as_view(template_name='invoice/password_reset.html'), 
        name='password_reset'),
    path('password/reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='invoice/password_reset_done.html'), 
        name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='invoice/password_reset_confirm.html'), 
        name='password_reset_confirm'),
    path('password/reset/complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='invoice/password_reset_complete.html'), 
        name='password_reset_complete'),
]