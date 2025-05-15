from django.contrib import admin
from .models import Invoice, InvoiceFile, InvoiceStatusHistory
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _

admin.site.register(Invoice)
admin.site.register(InvoiceStatusHistory)
admin.site.register(InvoiceFile)



class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'profile_pic')}),
        (_('Role'), {'fields': ('user_role', 'force_password_change')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_role', 'profile_pic', 'force_password_change'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'user_role', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')

admin.site.register(User, CustomUserAdmin)