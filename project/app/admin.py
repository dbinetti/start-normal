# Django
from django.contrib import admin

# Local
from .models import Signature


@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    fields = [
        'is_approved',
        'name',
        'handle',
        'email',
        'phone',
        'is_volunteer',
        'is_public',
        'is_subscribed',
        'location',
        'notes',
    ]
    list_display = [
        'email',
        'name',
        'handle',
        'location',
        'is_public',
        'is_subscribed',
    ]
    list_editable = [
        'name',
        'handle',
        'location',
        'is_public',
        'is_subscribed',
    ]
    list_filter = [
        'location',
        'is_public',
        'is_approved',
    ]
    search_fields = [
        'name',
        'email',
    ]
