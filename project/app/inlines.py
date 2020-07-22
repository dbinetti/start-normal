
# Django
from django.apps import apps
from django.contrib import admin

# Local
from .models import Contact
from .models import Report
from .models import School
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


class ReportInline(admin.TabularInline):
    model = Report
    fields = [
        'status',
        'title',
    ]
    readonly_fields = [
    ]
    ordering = [
        'created',
    ]
    show_change_link = True
    extra = 0
    classes = [
        # 'collapse',
    ]


class StudentInline(admin.TabularInline):
    model = Student
    fields = [
        'parent',
        'cohort',
        'school',
        'grade',
    ]
    readonly_fields = [
    ]
    ordering = [
        'grade',
    ]
    show_change_link = True
    extra = 0
    classes = [
        # 'collapse',
    ]
    autocomplete_fields = [
        'cohort',
        'parent',
        'school',
    ]


class SchoolInline(admin.TabularInline):
    model = School
    fields = [
        'name',
        'kind',
        'district',
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
    autocomplete_fields = [
        'district',
    ]
