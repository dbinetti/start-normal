# Django
from django import forms

# Local
from .models import Signature


class SignatureForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = [
            'name',
            'email',
            'city',
            'notes',
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Name/Anonymous (public)',
                    }
                ),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'City (public)',
                    }
                ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Email (kept private, only for updates)',
                    }
                ),
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Notes (kept private, only for context)',
                    }
                ),
            }
