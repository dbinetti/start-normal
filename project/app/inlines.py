
# Django
from django.apps import apps
from django.contrib import admin

# Local
from .models import Affiliation
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
    extra = 0
    classes = [
        # 'collapse',
    ]


class AffiliationInline(admin.TabularInline):
    model = Affiliation
    fields = [
        'is_approved',
        'message',
        'user',
        'organization',
    ]
    readonly_fields = [
    ]
    ordering = (
        'user',
    )
    show_change_link = True
    extra = 0
    classes = [
        # 'collapse',
    ]
    autocomplete_fields = [
        'organization',
    ]
