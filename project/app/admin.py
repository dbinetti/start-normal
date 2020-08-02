# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase

# Local
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import ClassmateInline
from .inlines import HomeroomInline
from .inlines import StudentInline
from .models import Account
from .models import District
from .models import Homeroom
from .models import Parent
from .models import School
from .models import Student
from .models import Teacher
from .models import User


@admin.register(Homeroom)
class HomeroomAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'status',
        'notes',
        'parent',
    ]
    list_display = [
        'parent',
        'status',
        'created',
        'updated',
    ]
    list_filter = [
        'status',
        'created',
        'updated',
    ]
    search_fields = [
        'students__school__name',
    ]
    autocomplete_fields = [
        'parent',
    ]
    inlines = [
        ClassmateInline,
    ]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'phone',
        'is_welcomed',
        'user',
    ]
    list_display = [
        'user',
        'created',
        'updated',
    ]
    list_filter = [
        'is_welcomed',
        'created',
    ]
    search_fields = [
        'user__name',
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
    ]


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'user',
        'notes',
    ]
    list_display = [
        'user',
        'created',
        'updated',
    ]
    list_filter = [
        'created',
        'updated',
    ]
    search_fields = [
        'user__name',
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
        StudentInline,
        HomeroomInline,
    ]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'user',
        'is_credential',
        'levels',
        'subjects',
        'school',
        'notes',
    ]
    list_display = [
        'user',
        'created',
        'updated',
    ]
    list_filter = [
        'created',
        'updated',
    ]
    search_fields = [
        'user__name',
    ]
    autocomplete_fields = [
        'user',
        'school',
    ]
    inlines = [
        # StudentInline,
    ]


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    exclude = [
        'slug',
    ]
    list_display = [
        'name',
        'kind',
        'website',
    ]
    list_filter = [
        'kind',
        'status',
        'county',
        'state',
    ]
    search_fields = [
        'name',
        'nces_id',
    ]
    inlines = [
        # SchoolInline,
        # ReportInline,
        # ContactInline,
    ]
    autocomplete_fields = [
        # 'parent',
    ]


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'level',
        'low_grade',
        'high_grade',
        'website',
    ]
    list_display = [
        'name',
        'level',
        'low_grade',
        'high_grade',
        'website',
    ]
    list_filter = [
        'level',
        'status',
    ]
    search_fields = [
        'name',
        'nces_id',
    ]
    inlines = [
        # StudentInline,
    ]
    autocomplete_fields = [
        'district',
    ]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'parent',
        'school',
        'grade',
    ]
    list_filter = [
        'grade',
        'created',
        'updated',
    ]
    search_fields = [
        'name',
        'parent__user__name',
    ]
    inlines = [
    ]
    autocomplete_fields = [
        'parent',
        'school',
    ]



@admin.register(User)
class UserAdmin(UserAdminBase):
    save_on_top = True
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = [
        'name',
        'email',
        'username',
        'created',
        'last_login'
    ]
    list_filter = [
        'is_active',
        'is_admin',
        'created',
        'last_login',
    ]
    search_fields = [
        'name',
        'email',
        'username',
    ]
    ordering = [
        '-created',
    ]
    fieldsets = (
        (None, {
            'fields': [
                'name',
                'email',
                'username',
            ]
        }
        ),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': [
                'name',
                'email',
                'username',
                'is_admin',
                'is_active',
            ]
        }
        ),
    )
    filter_horizontal = ()
    inlines = [
        # StudentInline,
    ]
