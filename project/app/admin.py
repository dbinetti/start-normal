# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Local
from .forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
)
from .models import (
    CustomUser,
    Signature,
)


@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'is_approved',
        'name',
        'handle',
        'email',
        'phone',
        'is_volunteer',
        'is_public',
        'is_subscribed',
        'location',
        'notes',
    ]
    list_display = [
        'email',
        'name',
        'handle',
        'location',
        'is_public',
        'is_subscribed',
    ]
    list_editable = [
        'name',
        'handle',
        'location',
        'is_public',
        'is_subscribed',
    ]
    list_filter = [
        'location',
        'is_public',
        'is_approved',
    ]
    search_fields = [
        'name',
        'email',
    ]






class CustomUserAdmin(UserAdmin):
    save_on_top = True
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'email',
    ]
    search_fields = [
        'email',
    ]
    fieldsets = (
        (None, {
            'fields': [
                'email',
            ]
        }
        ),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': [
                'email',
                'password1',
                'password2',
                'is_staff',
                'is_active',
            ]
        }
        ),
    )
    ordering = ['email']

admin.site.register(CustomUser, CustomUserAdmin)
