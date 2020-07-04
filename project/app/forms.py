# Django
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase

# Local
from .models import Account
from .models import Signature
from .models import User


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'name',
            # 'email',
            # 'location',
            'is_volunteer',
            'is_teacher',
            'is_doctor',
            'notes',
        ]
        labels = {
            "is_volunteer": "I Can Volunteer",
            "is_teacher": "I'm an Educator",
            "is_doctor": "I'm a Physician",
        }
        widgets = {
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control h-25',
                    'placeholder': 'Private Notes (Optional)',
                    'rows': 5,
                }
            ),
        }


class DeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
    )


class RemoveForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
    )


class SignatureForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = [
            'name',
            'petition',
            'account',
            'is_public',
            'message',
        ]
        widgets = {
            'message': forms.Textarea(
                attrs={
                    'class': 'form-control h-25',
                    'placeholder': 'Public Message (Optional)',
                    'rows': 5,
                }
            ),
            'petition': forms.HiddenInput(),
            'account': forms.HiddenInput(),
        }


class SignupForm(forms.Form):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    is_public = forms.BooleanField(
        required=False,
        label='Public',
        widget=forms.CheckboxInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control h-25',
                'placeholder': 'Public Message (Optional)',
                'rows': 5,
            }
        )
    )
    def clean_email(self):
        data = self.cleaned_data['email']
        return data.lower()


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
