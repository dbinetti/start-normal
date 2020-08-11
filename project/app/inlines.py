
# Django
from django.contrib import admin

# Local
from .models import Homeroom
from .models import Invite
from .models import School
from .models import Student


class HomeroomInline(admin.TabularInline):
    model = Homeroom
    fields = [
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
        'homeroom',
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
        'homeroom',
    ]


class InviteInline(admin.TabularInline):
    model = Invite
    fields = [
        'student_name',
        'parent_name',
        'parent_email',
        'homeroom',
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
        'homeroom',
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
