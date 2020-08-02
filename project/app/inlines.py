
# Django
from django.contrib import admin

# Local
from .models import Homeroom
from .models import School
from .models import Student


class HomeroomInline(admin.TabularInline):
    model = Homeroom
    fields = [
        'name',
        'parent',
    ]
    autocomplete_fields = [
        'parent',
    ]


class StudentInline(admin.TabularInline):
    model = Student
    fields = [
        'name',
        'parent',
        'school',
        'grade',
        # 'homeroom',
    ]
    readonly_fields = [
    ]
    ordering = [
        '-created',
    ]
    show_change_link = True
    extra = 0
    classes = [
        # 'collapse',
    ]
    autocomplete_fields = [
        'school',
        'parent',
    ]


class SchoolInline(admin.TabularInline):
    model = School
    fields = [
        'name',
        'level',
        'district',
    ]
    readonly_fields = [
    ]
    ordering = [
        'name',
    ]
    show_change_link = True
    extra = 0
    classes = [
        # 'collapse',
    ]
    autocomplete_fields = [
        'district',
    ]
