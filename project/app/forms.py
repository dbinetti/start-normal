# Django
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase

# First-Party
from dal import autocomplete

# Local
from .models import Account
from .models import Affiliation
from .models import Student
from .models import User


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'message',
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
                    'placeholder': 'Share a Message with your Public Officials (Optional)',
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


class AffiliationForm(forms.ModelForm):
    class Meta:
        model = Affiliation
        fields = [
            'status',
            'message',
            'organization',
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
            'organization': forms.HiddenInput(),
            'user': forms.HiddenInput(),
        }


class SignExistingForm(forms.ModelForm):
    class Meta:
        model = Affiliation
        fields = [
            'message',
            'organization',
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
            'organization': forms.HiddenInput(),
            'user': forms.HiddenInput(),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'grade',
            'organization',
            'user',
        ]
        widgets = {
            'organization': autocomplete.ModelSelect2(
                url='school-search',
                attrs={
                    'data-container-css-class': '',
                    'data-close-on-select': 'false',
                    'data-scroll-after-select': 'true',
                },
            ),
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
                'placeholder': 'Your Message with your Public Officials (Optional)',
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


# class District(models.Model):
#     STATUS = Choices(
#         (10, 'active', "Active"),
#         (20, 'closed', "Closed"),
#         (30, 'merged', "Merged"),
#     )
#     DOC = Choices(
#         (0, 'county', 'County Office of Education'),
#         (2, 'state', 'State Board of Education'),
#         (3, 'charter', 'Statewide Benefit Charter'),
#         (31, 'special', 'State Special Schools'),
#         (34, 'non', 'Non-school Location*'),
#         (42, 'jpa', 'Joint Powers Authority (JPA)'),
#         (52, 'elementary', 'Elementary School District'),
#         (54, 'unified', 'Unified School District'),
#         (56, 'high', 'High School District'),
#         (58, 'ccd', 'Community College District'),
#         (98, 'roc', 'Regional Occupational Center/Program (ROC/P)'),
#         (99, 'admin', 'Administration Only'),
#     )
#     id = HashidAutoField(
#         primary_key=True,
#     )
#     is_active = models.BooleanField(
#         default=False,
#     )
#     name = models.CharField(
#         max_length=255,
#         blank=False,
#     )
#     slug = AutoSlugField(
#         max_length=255,
#         always_update=False,
#         populate_from=get_populate_from,
#         unique=True,
#     )
#     status = models.IntegerField(
#         blank=False,
#         choices=STATUS,
#         default=STATUS.active,
#     )
#     cd_id = models.IntegerField(
#         null=False,
#         blank=False,
#         unique=True,
#     )
#     nces_district_id = models.IntegerField(
#         null=False,
#         blank=False,
#         unique=True,
#     )
#     county = models.CharField(
#         max_length=255,
#         blank=False,
#     )
#     address = models.CharField(
#         max_length=255,
#         blank=False,
#     )
#     city = models.CharField(
#         max_length=255,
#         blank=False,
#     )
#     state = models.CharField(
#         max_length=255,
#         blank=False,
#     )
#     zipcode = models.CharField(
#         max_length=255,
#         blank=False,
#     )
#     phone = models.CharField(
#         max_length=255,
#         blank=True,
#         default='',
#     )
#     website = models.URLField(
#         blank=True,
#         default='',
#     )
#     doc = models.IntegerField(
#         blank=False,
#         choices=DOC,
#     )
#     latitude = models.DecimalField(
#         max_digits=10,
#         decimal_places=6,
#         blank=True,
#         null=True,
#     )
#     longitude = models.DecimalField(
#         max_digits=10,
#         decimal_places=6,
#         blank=True,
#         null=True,
#     )
#     admin_first_name = models.CharField(
#         max_length=255,
#         blank=True,
#         default = '',
#     )
#     admin_last_name = models.CharField(
#         max_length=255,
#         blank=True,
#         default = '',
#     )
#     admin_email = models.EmailField(
#         max_length=255,
#         blank=True,
#         default = '',
#     )
#     created = models.DateTimeField(
#         auto_now_add=True,
#     )
#     updated = models.DateTimeField(
#         auto_now=True,
#     )
#     def location(self):
#         return(self.latitude, self.longitude)

#     def __str__(self):
#         return str(self.name)


# class School(models.Model):
#     STATUS = Choices(
#         (10, 'active', "Active"),
#         (20, 'closed', "Closed"),
#         (30, 'merged', "Merged"),
#     )
#     SOC = Choices(
#         (8, 'preschool', 'Preschool'),
#         (9, 'specialedu', 'Special Education Schools (Public)'),
#         (10, 'county', 'County Community'),
#         (11, 'yaf', 'Youth Authority Facilities (CEA)'),
#         (13, 'opportunity', 'Opportunity Schools'),
#         (14, 'juvenile', 'Juvenile Court Schools'),
#         (15, 'other', 'Other County or District Programs'),
#         (31, 'specialschool', 'State Special Schools'),
#         (60, 'elementary', 'Elementary School (Public)'),
#         (61, 'elementary1', 'Elementary School in 1 School District (Public)'),
#         (62, 'intermediate', 'Intermediate/Middle Schools (Public)'),
#         (63, 'alternative', 'Alternative Schools of Choice'),
#         (64, 'junior', 'Junior High Schools (Public)'),
#         (65, 'k12', 'K-12 Schools (Public)'),
#         (66, 'high', 'High Schools (Public)'),
#         (67, 'high1', 'High Schools in 1 School District (Public)'),
#         (68, 'continuuation', 'Continuation High Schools'),
#         (69, 'communityday', 'District Community Day Schools'),
#         (70, 'adult', 'Adult Education Centers'),
#         (98, 'roc', 'Regional Occupational Center/Program (ROC/P)'),
#     )
#     FUNDING = Choices(
#         (0, 'unknown', "(Unknown)"),
#         (10, 'direct', "Direct Funding"),
#         (20, 'indirect', "Indirect Funding"),
#         (30, 'disallowed', "Disallowed"),
#     )
#     EDOPS = Choices(
#         (10, 'altsoc', 'Alternative School of Choice'),
#         (20, 'comm', 'County Community School'),
#         (30, 'commday', 'Community Day School'),
#         (40, 'con', 'Continuation School'),
#         (50, 'juv', 'Juvenile Court School'),
#         (60, 'opp', 'Opportunity School'),
#         (70, 'yth', 'Youth Authority School'),
#         (80, 'sss', 'State Special School'),
#         (90, 'spec', 'Special Education School'),
#         (100, 'trad', 'Traditional'),
#         (110, 'rop', 'Regional Occupational Program'),
#         (120, 'homhos', 'Home and Hospital'),
#         (130, 'specon', 'District Consortia Special Education School'),
#     )
#     EIL = Choices(
#         (10, 'ps', 'Preschool'),
#         (20, 'elem', 'Elementary'),
#         (30, 'intmidjr', 'Intermediate/Middle/Junior High'),
#         (40, 'hs', 'High School'),
#         (50, 'elemhigh', 'Elementary-High Combination'),
#         (60, 'a', 'Adult'),
#         (70, 'ug', 'Ungraded'),
#     )
#     VIRTUAL = Choices(
#         (10, 'f', 'Exclusively Virutal'),
#         (20, 'v', 'Primarily Virtual'),
#         (30, 'c', 'Primarily Classroom'),
#         (40, 'n', 'Not Virtual'),
#         (50, 'p', 'Partial Virtual'),
#     )
#     id = HashidAutoField(
#         primary_key=True,
#     )
#     is_active = models.BooleanField(
#         default=False,
#     )
#     name = models.CharField(
#         max_length=255,
#         blank=False,
#     )
#     slug = AutoSlugField(
#         max_length=255,
#         always_update=False,
#         populate_from=get_populate_from,
#         unique=True,
#     )
#     status = models.IntegerField(
#         blank=False,
#         choices=STATUS,
#         default=STATUS.active,
#     )
#     cd_id = models.IntegerField(
#         blank=False,
#         unique=True,
#     )
#     nces_school_id = models.IntegerField(
#         blank=False,
#         unique=True,
#     )
#     county = models.CharField(
#         max_length=255,
#         blank=False,
#         default='',
#     )
#     address = models.CharField(
#         max_length=255,
#         blank=False,
#         default='',
#     )
#     city = models.CharField(
#         max_length=255,
#         blank=False,
#         default='',
#     )
#     state = models.CharField(
#         max_length=255,
#         blank=False,
#         default='',
#     )
#     zipcode = models.CharField(
#         max_length=255,
#         blank=False,
#         default='',
#     )
#     phone = models.CharField(
#         max_length=255,
#         blank=True,
#         default='',
#     )
#     website = models.URLField(
#         blank=True,
#         default='',
#     )
#     soc = models.IntegerField(
#         blank=False,
#         choices=SOC,
#     )
#     is_charter = models.BooleanField(
#         default=False,
#     )
#     charter_number = models.IntegerField(
#         null=True,
#         blank=True,
#     )
#     funding = models.IntegerField(
#         choices=FUNDING,
#         blank=True,
#         null=True,
#     )
#     edops = models.IntegerField(
#         choices=EDOPS,
#         blank=True,
#         null=True,
#     )
#     eil = models.IntegerField(
#         choices=EIL,
#         blank=True,
#         null=True,
#     )
#     grades = models.CharField(
#         max_length=255,
#         blank=True,
#         default='',
#     )
#     virtual = models.IntegerField(
#         choices=VIRTUAL,
#         blank=True,
#         null=True,
#     )
#     is_magnet = models.BooleanField(
#         default=False,
#     )
#     latitude = models.DecimalField(
#         max_digits=10,
#         decimal_places=6,
#         null=True,
#         blank=True,
#     )
#     longitude = models.DecimalField(
#         max_digits=10,
#         decimal_places=6,
#         null=True,
#         blank=True,
#     )
#     admin_first_name = models.CharField(
#         max_length=255,
#         blank=True,
#         default = '',
#     )
#     admin_last_name = models.CharField(
#         max_length=255,
#         blank=True,
#         default = '',
#     )
#     admin_email = models.EmailField(
#         max_length=255,
#         blank=True,
#         default = '',
#     )
#     created = models.DateTimeField(
#         auto_now_add=True,
#     )
#     updated = models.DateTimeField(
#         auto_now=True,
#     )
#     district = models.ForeignKey(
#         'District',
#         on_delete=models.CASCADE,
#         related_name='schools',
#     )
#     def location(self):
#         return(self.latitude, self.longitude)

#     def __str__(self):
#         return str(self.name)
