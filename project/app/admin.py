# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Local
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, Signature


@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'name',
        'is_approved',
        'location',
        'district',
        'phone',
        'is_public',
        'is_volunteer',
        'is_teacher',
        'is_doctor',
        'email',
        'notes',
        'user',
    ]
    list_display = [
        'name',
        'location',
        'district',
        'is_public',
        'is_teacher',
        'is_doctor',
        'created',
        'updated',
    ]
    list_filter = [
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




class CustomUserAdmin(UserAdmin):
    save_on_top = True
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'email',
        'created',
        'last_login'
        # 'signature',
    ]
    list_filter = [
        'is_admin',
        'created',
    ]
    search_fields = [
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


admin.site.register(CustomUser, CustomUserAdmin)
