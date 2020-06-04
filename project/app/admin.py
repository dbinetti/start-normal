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
        'city',
        'notes',
    ]
    list_display = [
        'name',
        'email',
        'city',
        'is_approved',
    ]
    list_filter = [
        'is_approved',
    ]
    search_fields = [
        'name',
        'email',
    ]
