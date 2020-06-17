# Django
from django import forms
from django.contrib.auth.forms import (
    SetPasswordForm,
    UserChangeForm,
    UserCreationForm,
)

# Local
from .models import (
    CustomUser,
    Registration,
    Signature,
)


class CustomSetPasswordForm(SetPasswordForm):
    pass


class DeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
    )

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            'email',
            'name',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control h-25',
                    'placeholder': 'Brief Notes/Question (optional, private)',
                    'rows': 5,
                    }
                ),
            }

class AccountForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = [
            'name',
            'location',
            # 'district',
            # 'is_volunteer',
            'is_public',
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
            'email',
            'is_public',
            'is_teacher',
            'is_doctor',
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

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')
        email = email.strip().lower()
        try:
            Signature.objects.get(email__iexact=email)
        except Signature.DoesNotExist:
            return email
        raise forms.ValidationError('This email address is already in use.')


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
