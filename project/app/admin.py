# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase

# First-Party
from mptt.admin import MPTTModelAdmin

# Local
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import ContactInline
from .inlines import SignatureInline
from .models import Account
from .models import District
from .models import Faq
from .models import Petition
from .models import School
from .models import Signature
from .models import User


def approve_signature(modeladmin, request, queryset):
    queryset.update(is_approved=True)

approve_signature.short_description = "Approve Signatures"

@admin.register(Petition)
class PetitionAdmin(MPTTModelAdmin):
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


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    exclude = [
        'slug',
    ]
    list_display = [
        'name',
        'status',
        'cd_id',
        'county',
        'soc',
        'funding',
        'is_charter',
        'edops',
        'eil',
        'grades',
        'virtual',
        'is_magnet',
        'address',
        'website',
        'phone',
        'admin_first_name',
        'admin_last_name',
        'admin_email',
    ]
    list_filter = [
        'is_active',
        'status',
        'soc',
        'funding',
        'is_charter',
        'edops',
        'eil',
        'virtual',
        'is_magnet',
    ]
    search_fields = [
        'name',
    ]
    inlines = [
        # ContactInline,
    ]


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    save_on_top = True
    exclude = [
        'name',
        'meeting_date',
    ]
    list_display = [
        'name',
        'status',
        'cd_id',
        'nces_district_id',
        'county',
    ]
    list_filter = [
        'is_active',
        'status',
        'doc',
        'created',
    ]
    search_fields = [
        'name',
    ]
    inlines = [
        # ContactInline,
    ]
    ordering = [
        'name',
    ]


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'is_active',
        'num',
        'question',
        'answer',
    ]
    list_display = [
        'question',
        'num',
        'is_active',
    ]
    list_editable = [
        'num',
    ]
    list_filter = [
        'is_active',
        'created',
        'updated',
    ]
    search_fields = [
        'question',
        'answer',
    ]


@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'status',
        'is_approved',
        'message',
        'account',
        'petition',
    ]
    list_display = [
        'status',
        'is_approved',
        'account',
        'petition',
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
        'account__user__name',
    ]
    autocomplete_fields = [
        'account',
        'petition',
    ]
    actions = [
        approve_signature
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
        SignatureInline,
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
