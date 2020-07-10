# Django
# Third-Party
from mptt.admin import MPTTModelAdmin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase

# Local
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import AffiliationInline
from .inlines import ContactInline
from .models import Account
from .models import Affiliation
from .models import Contact
from .models import Organization
from .models import Report
from .models import User


def approve_affiliation(modeladmin, request, queryset):
    queryset.update(is_approved=True)

approve_affiliation.short_description = "Approve Affiliations"

@admin.register(Organization)
class OrganizationAdmin(MPTTModelAdmin):
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
        # ContactInline,
    ]
    autocomplete_fields = [
        'parent',
    ]



@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'text',
        'user',
        'organization',
    ]
    list_display = [
        'name',
        'status',
        'user',
        'organization',
    ]
    list_filter = [
        'status',
    ]
    search_fields = [
        'name',
    ]
    autocomplete_fields = [
        'user',
        'organization',
    ]



@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'status',
        'is_approved',
        'message',
        'user',
        'organization',
    ]
    list_display = [
        'status',
        'is_approved',
        'user',
        'organization',
        'created',
        'updated',
    ]
    list_filter = [
        'status',
        'is_approved',
        'created',
        'updated',
    ]
    search_fields = [
        'user__name',
    ]
    autocomplete_fields = [
        'user',
        'organization',
    ]
    actions = [
        approve_affiliation
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
        # AffiliationInline,
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
