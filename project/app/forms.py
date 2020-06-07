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
