
# Django
from django.apps import apps
from django.contrib import admin

# Local
from .models import Contact
from .models import Signature


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
    extra = 0
    classes = [
        # 'collapse',
    ]


class SignatureInline(admin.TabularInline):
    model = Signature
    fields = [
        'is_approved',
        'message',
        'account',
        'petition',
    ]
    readonly_fields = [
    ]
    ordering = (
        'account',
    )
    show_change_link = True
    extra = 0
    classes = [
        # 'collapse',
    ]
    autocomplete_fields = [
        'petition',
    ]
