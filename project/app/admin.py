# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase

# First-Party
from mptt.admin import MPTTModelAdmin

# Local
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import ContactInline
from .inlines import ReportInline
from .inlines import SchoolInline
from .inlines import StudentInline
from .models import Account
from .models import Contact
from .models import District
from .models import Parent
from .models import Report
from .models import School
from .models import Student
from .models import Teacher
from .models import User


def approve_report(modeladmin, request, queryset):
    for report in queryset:
        report.status = Report.STATUS.approved
        report.save()
    return


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'user',
        'phone',
        'is_public',
        'is_subscribe',
        'is_volunteer',
        'is_teacher',
        'is_doctor',
        'message',
    ]
    list_display = [
        'user',
        'location',
        'is_teacher',
        'is_doctor',
        'created',
        'updated',
    ]
    list_filter = [
        'location',
        'is_public',
        'is_subscribe',
        'is_teacher',
        'is_doctor',
        'is_volunteer',
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
    ]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'user',
        'is_credential',
        'kinds',
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
        'is_active',
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
    exclude = [
        'slug',
    ]
    list_display = [
        'name',
        'kind',
        'website',
    ]
    list_filter = [
        'is_active',
        'kind',
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
        'parent',
    ]
    inlines = [
    ]
    autocomplete_fields = [
        # 'parent',
    ]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'role',
        'email',
        'phone',
        'is_active',
    ]
    list_filter = [
        'is_active',
        'role',
        'created',
        'updated',
    ]
    search_fields = [
        'name',
    ]
    inlines = [
    ]
    autocomplete_fields = [
        # 'parent',
    ]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    fields = [
        'status',
        'title',
        'text',
        'user',
    ]
    list_display = [
        'title',
        'status',
        'user',
    ]
    list_filter = [
        'status',
    ]
    search_fields = [
        'name',
    ]
    autocomplete_fields = [
        'user',
    ]
    actions = [
        approve_report,
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
