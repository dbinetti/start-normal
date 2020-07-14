
# Django
from django.apps import apps
from django.contrib import admin

# Local
from .models import Contact
from .models import Student


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


class StudentInline(admin.TabularInline):
    model = Student
    fields = [
        'user',
        'organization',
        'grade',
    ]
    readonly_fields = [
    ]
    ordering = (
        'grade',
    )
    show_change_link = True
    extra = 0
    classes = [
        # 'collapse',
    ]
