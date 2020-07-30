# Django
from django import forms
from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from django.forms.models import inlineformset_factory

# First-Party
from dal import autocomplete

# Local
from .models import Classmate
from .models import District
from .models import Homeroom
from .models import Parent
from .models import School
from .models import Student
from .models import Teacher
from .models import User

StudentFormSet = inlineformset_factory(
    Parent,
    Student,
    fields=[
        'grade',
        'name',
        'school',
        'parent',
    ],
    widgets={
        'school': autocomplete.ModelSelect2(
            url='school-autocomplete',
            attrs={
                'data-container-css-class': '',
                'data-close-on-select': 'false',
                'data-scroll-after-select': 'true',
                'data-placeholder': 'Start typing to search....',
                'data-minimum-input-length': 3,
            },
        ),
    },
    extra=0,
    max_num=5,
    can_delete=True,
)


class SchoolForm(forms.ModelForm):

    class Meta:
        model = School
        fields = [
            'level',
            'name',
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
            'levels',
            'subjects',
            'school',
            'notes',
        ]
        labels = {
            "is_credential": "Credentialed?",
            "levels": "School Level",
            "subjects": "School Subjects",
        }
        help_texts = {
            "is_credential": "If you are credentialed please check the box.",
        }


class HomeroomForm(forms.ModelForm):

    class Meta:
        model = Homeroom
        fields = [
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control h-25',
                    'placeholder': 'Please provide some notes on your preferred safety regimen; i.e., masks, distance, hygenic requirements.',
                    'rows': 5,
                }
            )
        }



class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name',
            'school',
            'grade',
        ]
    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='school-autocomplete',
            attrs={
                'data-container-css-class': '',
                'data-close-on-select': 'false',
                'data-scroll-after-select': 'false',
                'data-placeholder': 'Search Schools',
                'data-minimum-input-length': 3,
            },
        ),
        help_text="Please select the school your student would be entering in the Fall.",
    )



class ClassmateForm(forms.ModelForm):
    class Meta:
        model = Classmate
        fields = [
            'status',
        ]


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
