# Django
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from django.forms.models import inlineformset_factory

# First-Party
from dal import autocomplete

# Local
from .models import Account
from .models import Cohort
from .models import Contact
from .models import District
from .models import Parent
from .models import Report
from .models import School
from .models import Student
from .models import Teacher
from .models import User

StudentFormSet = inlineformset_factory(
    Parent,
    Student,
    fields=[
        'grade',
        'school',
        'parent',
    ],
    widgets = {
        'school': autocomplete.ModelSelect2(
            url='school-autocomplete',
            attrs={
                'data-container-css-class': '',
                'data-close-on-select': 'false',
                'data-scroll-after-select': 'true',
                'data-placeholder': 'Start typing to search....',
                'data-minimum-input-length': 3,
            },
        )
    },
    extra=0,
    # max_num=5,
    can_delete=True,
)


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = [
            'kind',
            'name',
            'kind',
            'nces_id',
            'address',
            'city',
            'state',
            'zipcode',
            'county',
            'phone',
            'website',
            'lat',
            'lon',
        ]


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = [
            'kind',
            'name',
            'kind',
            'nces_id',
            'address',
            'city',
            'state',
            'zipcode',
            'county',
            'phone',
            'website',
            'lat',
            'lon',
        ]


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'message',
            'teacher',
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
            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your Message to your Public Officials',
                    'rows': 5,
                }
            ),
        }


class TeacherForm(forms.ModelForm):

    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='school-autocomplete',
            attrs={
                'data-container-css-class': '',
                'data-close-on-select': 'false',
                'data-scroll-after-select': 'true',
                'data-placeholder': 'Nearby School',
                'data-minimum-input-length': 3,
            },
        ),
        help_text="Pick a school near where you'd like to teach (dosn't have to be your own school; this is just for location.)",
    )

    class Meta:
        model = Teacher
        fields = [
            'is_credential',
            'kinds',
            'subjects',
            'school',
            'notes',
        ]
        labels = {
            "is_credential": "Credentialed?",
            "kinds": "School Level",
            "subjects": "School Subjects",
        }
        help_texts = {
            "is_credential": "If you are credentialed please check the box.",
        }


class CohortForm(forms.ModelForm):
    class Meta:
        model = Cohort
        fields = [
            'name',
            'description',
            'grade',
        ]


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'name',
            'role',
            'email',
            'phone',
        ]


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            'title',
            'text',
        ]

    def clean_title(self):
        data = self.cleaned_data['title']
        return data.title()


class DeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
    )


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
        help_text="""A password is necessary to manage preferences. (Required)""",
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
        help_text="""Please keep your message civil.  I won't post messages that are vulgar, profane, or otherwise inappropriate. (Optional)""",
        widget=forms.Textarea(
            attrs={
                'class': 'form-control h-25',
                'placeholder': 'Your Message to your Public Officials',
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
