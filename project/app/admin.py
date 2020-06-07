# Django
from django.contrib import admin

# Local
from .models import Signature


@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    fields = [
        'is_approved',
        'name',
        'email',
        'phone',
        'is_volunteer',
        'is_public',
        'is_subscribed',
        'city',
        'location',
        'notes',
    ]
    list_display = [
        'email',
        'name',
        'city',
        'location',
        'is_public',
        'is_subscribed',
    ]
    list_editable = [
        'name',
        'location',
        'is_public',
        'is_subscribed',
    ]
    list_filter = [
        'location',
        'is_approved',
    ]
    search_fields = [
        'name',
        'email',
    ]
