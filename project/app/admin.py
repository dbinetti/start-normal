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
        'notes',
    ]
    list_display = [
        'name',
        'email',
        'city',
        'timestamp',
        'is_approved',
        'is_volunteer',
        'is_public',
        'is_subscribed',
        'notes',
    ]
    list_filter = [
        'is_approved',
    ]
    search_fields = [
        'name',
        'email',
    ]
