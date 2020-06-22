
from django.apps import apps
# Django
from django.contrib import admin

# Local
from .models import Contact


class ContactInline(admin.TabularInline):
    model = Contact
    fields = [
        'is_active',
        'name',
        'role',
        'email',
        'phone',
    ]
    readonly_fields = [
    ]
    ordering = (
        'role',
    )
    show_change_link = True
    extra = 1
    classes = [
        # 'collapse',
    ]
