# Django
# Third-Party
from mptt.admin import MPTTModelAdmin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase

# Local
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import ContactInline
from .inlines import SchoolInline
from .inlines import StudentInline
from .models import Account
from .models import Contact
from .models import District
from .models import Report
from .models import School
from .models import User


def approve_report(modeladmin, request, queryset):
    for report in queryset:
        report.status = Report.STATUS.approved
        if report.is_district:
            district = report.organization.parent
            schools = district.children.exclude(
                id=report.organization.id,
            )
            for school in schools:
                school.reports.create(
                    status=Report.STATUS.approved,
                    title=report.title,
                    text=report.text,
                    user=report.user,
                )
    return



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
        SchoolInline,
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


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    fields = [
        'status',
        'title',
        'text',
        'user',
        'district',
    ]
    list_display = [
        'title',
        'status',
        'user',
        'district',
    ]
    list_filter = [
        'status',
    ]
    search_fields = [
        'name',
    ]
    autocomplete_fields = [
        'user',
        'district',
    ]
    actions = [
        approve_report,
    ]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'user',
        'location',
        'phone',
        'is_public',
        'is_subscribe',
        'is_volunteer',
        'is_teacher',
        'is_doctor',
        'notes',
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
        '-last_login',
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
