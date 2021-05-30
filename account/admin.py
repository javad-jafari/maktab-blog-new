from django.contrib import admin
from django.contrib.auth.forms import AdminPasswordChangeForm

from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _


class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'is_staff']
    change_password_form = AdminPasswordChangeForm
    ordering = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2')
        }),
    )
    fieldsets = (
        (_('authentication data'), {
            "fields": (
                'email',
                'password',
            ),
        }),
        (_('Personal info'), {
            "fields": ('full_name', 'avatar')
        }),
        (_('Permissions'), {
            "fields": ('is_author','is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Important dates'), {
            "fields": ('last_login',)
        }),
    )


# Register your models here.
admin.site.register(User, UserAdmin)