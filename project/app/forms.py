# Django
from django import forms
from django.contrib.auth.forms import (SetPasswordForm, UserChangeForm,
                                       UserCreationForm)

# Local
from .models import CustomUser, Signature


class CustomSetPasswordForm(SetPasswordForm):
    pass


class DeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
    )

class AccountForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = [
            'name',
            'is_public',
            'location',
            'district',
            'is_volunteer',
            'is_teacher',
            'is_doctor',
            # 'phone',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control h-25',
                    'placeholder': 'Brief Notes (optional, private)',
                    'rows': 5,
                    }
                ),
            }

class SignatureForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = [
            'name',
            'handle',
            'email',
            'is_public',
            'is_subscribed',
            'location',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control h-25',
                    'placeholder': 'Brief Notes (optional, private)',
                    'rows': 5,
                    }
                ),
            }

class SubscribeForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    def clean_email(self):
        data = self.cleaned_data['email']
        return data.lower()


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)
