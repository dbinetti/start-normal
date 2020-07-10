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
            # 'location',
            'is_public',
            'is_subscribe',
            'is_volunteer',
            'is_teacher',
            'is_doctor',
        ]
        labels = {
            "is_public": "List my Name on the Website",
            "is_subscribe": "Send Updates",
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


class SignForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
    )


class SignatureForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = [
            'status',
            'message',
            'petition',
            'user',
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
            'user': forms.HiddenInput(),
        }


class SignupForm(forms.Form):
    name = forms.CharField(
        required=True,
        help_text="""Real name strongly encouraged.  However, if necessary use a descriptor like 'Concerned Parent' or 'Father of Two'. (Required)""",
    )
    email = forms.EmailField(
        required=True,
        help_text="""Your email is private and not shared.  It's used to manage preferences and send adminstrative updates. (Required)""",
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="""A password is required to manage preferences. (Required)""",
    )
    is_public = forms.BooleanField(
        initial=True,
        label='List My Name on the Website',
    )
    is_subscribe = forms.BooleanField(
        initial=True,
        label='Receive Updates (roughly once/week)',
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control h-25',
                'placeholder': 'Attach a Public Message to your Signature (Optional)',
                'rows': 5,
            }
        )
    )
    def clean_email(self):
        data = self.cleaned_data['email']
        return data.lower()

    def clean_name(self):
        data = self.cleaned_data['name']
        return data.title()


class SubscribeForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    def clean_email(self):
        data = self.cleaned_data['email']
        return data.lower()


class UserCreationForm(UserCreationFormBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()
        if commit:
            user.save()
        return user

    def clean_email(self):
        data = self.cleaned_data['email']
        return data.lower()

    def clean_name(self):
        data = self.cleaned_data['name']
        return data.title()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'name',
        ]



class UserChangeForm(UserChangeFormBase):

    def clean_email(self):
        data = self.cleaned_data['email']
        return data.lower()

    def clean_name(self):
        data = self.cleaned_data['name']
        return data.title()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'name',
        ]
