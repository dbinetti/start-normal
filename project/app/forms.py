# Django
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase

# Local
from .models import Account
from .models import Registration
from .models import Signature
from .models import User


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
        model = Account
        fields = [
            'name',
            # 'email',
            'location',
            'is_teacher',
            'is_doctor',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control h-25',
                    'placeholder': 'Private Notes (Optional)',
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
            'location',
            'message',
            'is_public',
            'is_teacher',
            'is_doctor',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control h-25',
                    'placeholder': 'Private Notes (Optional)',
                    'rows': 5,
                }
            ),
            'message': forms.Textarea(
                attrs={
                    'class': 'form-control h-25',
                    'placeholder': 'Public Message (Optional)',
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


class UserCreationForm(UserCreationFormBase):

    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2',)


class UserChangeForm(UserChangeFormBase):

    class Meta:
        model = User
        fields = ('username', 'email',)
