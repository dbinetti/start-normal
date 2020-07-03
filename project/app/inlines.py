
# Django
from django.apps import apps
from django.contrib import admin

# Local
from .models import Contact
from .models import Registration
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
class RegistrationInline(admin.TabularInline):
    model = Registration
    fields = [
        'name',
        'notes',
        'account',
    ]
    readonly_fields = [
    ]
    ordering = (
        'name',
    )
    show_change_link = True
    extra = 0
    classes = [
        # 'collapse',
    ]
class SignatureInline(admin.TabularInline):
    model = Signature
    fields = [
        'petition',
        'is_approved',
        'is_public',
        'message',
        'account',
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
