# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase

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


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    exclude = [
        'slug',
    ]
    list_display = [
        'name',
        'cd_status',
        'cd_id',
        'nces_district_id',
        'county',
        'soc',
        'funding_type',
        'is_charter',
        'edops_type',
        'eil',
        'grade_span',
        'virtual_type',
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
        'cd_status',
        'soc',
        'funding_type',
        'is_charter',
        'edops_type',
        'eil',
        'grade_span',
        'virtual_type',
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
        'status',
        'schedule',
        'masks',
        'meeting_date',
    ]
    list_display = [
        'name',
        'cd_status',
        'cd_id',
        'nces_district_id',
        'county',
    ]
    list_filter = [
        'is_active',
        'cd_status',
        'doc',
        'created',
        'schedule',
        'masks',
    ]
    search_fields = [
        'name',
    ]
    inlines = [
        ContactInline,
    ]
    ordering = [
        'name',
    ]


@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'status',
        'name',
        'text',
        'district',
    ]
    list_display = [
        'status',
        'name',
        'district',
        'created',
        'updated',
    ]
    list_filter = [
        'status',
        'created',
    ]
    search_fields = [
        'name',
    ]
    inlines = [
    ]
    ordering = [
        'name',
    ]
    autocomplete_fields = [
        'district',
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
        'created',
        'num',
        'question',
        'answer',
        'is_active',
    ]
    list_editable = [
        'num',
        'question',
        'answer',
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
        'name',
        'is_approved',
        'is_public',
        'message',
        'account',
        'petition',
    ]
    list_display = [
        'status',
        'name',
        'is_approved',
        'is_public',
        'account',
        'petition',
        'created',
        'updated',
    ]
    list_filter = [
        'status',
        'is_approved',
        'is_public',
        'created',
        'updated',
    ]
    search_fields = [
        'name',
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
        'name',
        'location',
        'phone',
        'is_volunteer',
        'is_teacher',
        'is_doctor',
        'email',
        'notes',
        # 'user',
    ]
    list_display = [
        'name',
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
        'name',
        'email',
    ]
    autocomplete_fields = [
        # 'user',
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
        'username',
        'email',
        'created',
        'last_login'
        # 'signature',
    ]
    list_filter = [
        'is_active',
        'is_admin',
        'created',
        'last_login',
    ]
    search_fields = [
        'username',
        'email',
    ]
    autocomplete_fields = [
        # 'signature',
    ]
    ordering = [
        '-last_login',
        '-created',
    ]
    fieldsets = (
        (None, {
            'fields': [
                'username',
                'email',
                # 'signature',
            ]
        }
        ),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': [
                'username',
                'email',
                'password1',
                'password2',
                'is_admin',
                'is_active',
            ]
        }
        ),
    )
    ordering = ['email']
    filter_horizontal = ()
