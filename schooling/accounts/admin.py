from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.core.mail import send_mail
import random
import string

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'manage_role_link')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ()

    def manage_role_link(self, obj):
        link = reverse("admin:accounts_user_change", args=[obj.pk])
        return format_html(f'<a href="{link}">Manage Role</a>')
    manage_role_link.short_description = 'Manage Role'

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if change:  
            old_role = User.objects.get(pk=obj.pk).role
            if old_role == 'student' and obj.role == 'teacher':
                new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                obj.set_password(new_password) 
                obj.save()
                
                send_mail(
                    'Role Updated and New Password',
                    f'Your role has been changed to Teacher. Your new password is: {new_password}. Please change it upon your first login.',
                    'from@example.com',
                    [obj.email],
                    fail_silently=False,
                )
                
                obj.password_expired = True
                obj.save()
            else:
                obj.save()
        else:
            obj.save()

admin.site.register(User, UserAdmin)
