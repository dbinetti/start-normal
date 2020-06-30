# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase

# Local
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import ContactInline
from .models import District
from .models import Faq
from .models import Registration
from .models import Signature
from .models import User


def approve_signature(modeladmin, request, queryset):
    queryset.update(is_approved=True)

approve_signature.short_description = "Approve Signatures"


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'name',
        'short',
        'status',
        'schedule',
        'masks',
        'meeting_date',
    ]
    list_display = [
        'name',
        'short',
        'schedule',
        'masks',
        'meeting_date',
    ]
    list_filter = [
        'created',
        'schedule',
        'masks',
    ]
    search_fields = [
        'name',
        'short',
    ]
    inlines = [
        ContactInline,
    ]
    ordering = [
        'name',
    ]
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'name',
        'email',
        'notes',
    ]
    list_display = [
        'name',
        'email',
        'notes',
        'created',
    ]
    list_filter = [
        'created',
    ]
    search_fields = [
        'name',
        'email',
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
        'name',
        'is_approved',
        'location',
        'phone',
        'is_public',
        'is_volunteer',
        'is_teacher',
        'is_doctor',
        'email',
        'notes',
        'message',
        'user',
    ]
    list_display = [
        'name',
        'location',
        'is_public',
        'is_teacher',
        'is_doctor',
        # 'notes',
        'message',
        'created',
        'updated',
    ]
    list_filter = [
        'is_approved',
        'location',
        'is_public',
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
        'user',
    ]
    actions = [
        approve_signature
    ]



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


admin.site.register(User, UserAdmin)
