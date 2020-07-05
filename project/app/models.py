# Django
# Third-Party
import shortuuid
from hashid_field import HashidAutoField
from model_utils import Choices
from shortuuidfield import ShortUUIDField

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils.text import slugify

# Local
from .managers import UserManager


class Account(models.Model):

    LOCATION = Choices(
        ('ath', 'Atherton'),
        ('bel', 'Belmont'),
        ('brb', 'Brisbane'),
        ('bur', 'Burlingame'),
        ('col', 'Colma'),
        ('dc', 'Daly City'),
        ('epa', 'East Palo Alto'),
        ('fc', 'Foster City'),
        ('hmb', 'Half Moon Bay'),
        ('hil', 'Hillsborough'),
        ('mp', 'Menlo Park'),
        ('mil', 'Millbrae'),
        ('pac', 'Pacifica'),
        ('pv', 'Portola Valley'),
        ('rc', 'Redwood City'),
        ('sb', 'San Bruno'),
        ('sc', 'San Carlos'),
        ('sm', 'San Mateo'),
        ('ssf', 'South San Francisco'),
        ('ws', 'Woodside'),
        ('un', 'Unincorporated San Mateo County'),
        ('out', 'Outside of San Mateo County'),
    )

    id = HashidAutoField(
        primary_key=True,
    )
    name = models.CharField(
        max_length=255,
        help_text="""Real name strongly encouraged.  However, if necessary use a descriptor like 'Concerned Parent' or 'Father of Two'. (Required)""",
    )
    email = models.EmailField(
        blank=False,
        unique=True,
        help_text="""Your email is private and not shared.  It's used to manage preferences and send adminstrative updates. (Required)""",
    )
    location = models.CharField(
        max_length=255,
        choices=LOCATION,
        blank=True,
        help_text="""Your city. (Required)""",
    )
    phone = models.CharField(
        max_length=255,
        blank=True,
        help_text="""Your mobile phone. (Optional)""",
    )
    is_volunteer = models.BooleanField(
        default=False,
        help_text="""If you're willing to volunteer please check this box.""",
    )
    is_teacher = models.BooleanField(
        default=False,
        help_text="""If you're an educator please check this box.""",
    )
    is_doctor = models.BooleanField(
        default=False,
        help_text="""If you're a physician please check this box.""",
    )
    notes = models.TextField(
        max_length=512,
        blank=True,
        default='',
        help_text="""Feel free to include private notes just for us.""",
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    user = models.OneToOneField(
        'app.User',
        on_delete=models.CASCADE,
        related_name='account',
    )

    def __str__(self):
        return str(self.name)


class Contact(models.Model):
    ROLE = Choices(
        (10, 'super', 'Superintendent'),
        (20, 'president', 'Board President'),
        (30, 'vice', 'Board Vice-President'),
        (40, 'clerk', 'Board Clerk'),
        (50, 'trustee', 'Board Trustee'),
    )
    id = HashidAutoField(
        primary_key=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    name = models.CharField(
        max_length=255,
        blank=False,
    )
    role = models.IntegerField(
        null=True,
        blank=True,
        choices=ROLE,
    )
    email = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )
    phone = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    district = models.ForeignKey(
        'District',
        on_delete=models.CASCADE,
        related_name='contacts',
    )


    def __str__(self):
        return str(self.name)


# class School(models.Model):
#     id = HashidAutoField(
#         primary_key=True,
#     )
#     is_active = models.BooleanField(
#         default=False,
#     )


#     cdcode_id = models.IntegerField(
#         null=True,
#         blank=True,
#     )

#     nces_district_id = models.IntegerField(
#         null=True,
#         blank=True,
#     )

#     nces_school_id = models.IntegerField(
#         null=True,
#         blank=True,
#     )

#     district_name = models.CharField(
#         max_length=255,
#         default='',
#         blank=True,
#     )

#     school_name = models.CharField(
#         max_length=255,
#         default='',
#         blank=True,
#     )

#     school_kind = models.

#     county = models.CharField(
#         max_length=15,
#         default='',
#         blank=True,
#     )

#     phone = models.CharField(
#         max_length=14,
#         default='',
#         blank=True,
#     )
#     email = models.CharField(
#         max_length=50,
#         default='',
#         blank=True,
#     )
#     latitude = models.DecimalField(
#         max_digits=10,
#         null=True,
#     )
#     longitude = models.DecimalField(
#         max_digits=10,
#         null=True,
#     )
#     doc = models.IntegerField(
#         null=True,
#         blank=True,
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





class District(models.Model):

    DOC = Choices(
        (0, 'county', 'County Office of Education'),
        (2, 'state', 'State Board of Education'),
        (3, 'charter', 'Statewide Benefit Charter'),
        (31, 'special', 'State Special Schools'),
        (34, 'non', 'Non-school Location*'),
        (42, 'jpa', 'Joint Powers Authority (JPA)'),
        (52, 'elementary', 'Elementary School District'),
        (54, 'unified', 'Unified School District'),
        (56, 'high', 'High School District'),
        (58, 'ccd', 'Community College District'),
        (98, 'roc', 'Regional Occupational Center/Program (ROC/P)'),
        (99, 'admin', 'Administration Only'),
    )


    CDSTATUS = Choices(
        (10, 'active', "Active"),
        (20, 'closed', "Closed"),
        (30, 'merged', "Merged"),
    )
    SCHEDULE = Choices(
        (0, 'unknown', "(Unknown)"),
        (10, 'person', "In-Person"),
        (20, 'blended', "Blended"),
        (30, 'distance', "Distance"),
        (40, 'undecided', "Undecided"),
    )
    MASKS = Choices(
        (0, 'unknown', "(Unknown)"),
        (10, 'required', "Required"),
        (20, 'optional', "Optional"),
        (30, 'disallowed', "Disallowed"),
    )

    id = HashidAutoField(
        primary_key=True,
    )
    is_active = models.BooleanField(
        default=False,
    )
    name = models.CharField(
        max_length=255,
        blank=False,
    )
    short = models.CharField(
        max_length=255,
        blank=False,
    )
    status = models.TextField(
        blank=True,
    )
    schedule = models.IntegerField(
        null=True,
        blank=False,
        choices=SCHEDULE,
        default=SCHEDULE.unknown,
    )
    masks = models.IntegerField(
        null=True,
        blank=False,
        choices=MASKS,
        default=MASKS.unknown,
    )
    is_masks = models.BooleanField(
        default=True,
    )
    meeting_date = models.DateField(
        null=True,
        blank=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    cd_status = models.IntegerField(
        null=True,
        blank=True,
        choices=CDSTATUS,
    )
    cd_id = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
    )
    nces_district_id = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
    )
    district_name = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )
    county_name = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )
    address = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )
    city = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )
    state = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )
    zipcode = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )
    phone = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )
    website = models.URLField(
        blank=True,
        default='',
    )
    doc = models.IntegerField(
        null=True,
        blank=True,
        choices=DOC,
    )
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        blank=True,
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        blank=True,
    )
    admin_first_name = models.CharField(
        max_length=255,
        blank=True,
        default = '',
    )
    admin_last_name = models.CharField(
        max_length=255,
        blank=True,
        default = '',
    )
    admin_email = models.EmailField(
        max_length=255,
        blank=True,
        default = '',
    )

    def should_index(self):
        return self.is_active

    def location(self):
        return(self.latitude, self.longitude)

    def __str__(self):
        return str(self.name)


class Faq(models.Model):

    id = HashidAutoField(
        primary_key=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    num = models.IntegerField(
        default=50,
    )
    question = models.TextField(
        max_length=255,
        blank=False,
    )
    answer = models.TextField(
        max_length=1024,
        blank=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    def __str__(self):
        return str(slugify(self.question))


class Petition(models.Model):

    STATUS = Choices(
        (0, 'new', 'New'),
        (10, 'open', 'Open'),
        (20, 'delivered', 'Delivered'),
    )

    id = HashidAutoField(
        primary_key=True,
    )
    name = models.CharField(
        max_length=255,
        blank=False,
    )
    status = models.IntegerField(
        blank=False,
        choices=STATUS,
        default=STATUS.new,
    )
    text = models.TextField(
        blank=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    district = models.ForeignKey(
        'app.District',
        on_delete=models.CASCADE,
        related_name='petitions',
    )
    def __str__(self):
        return str(self.name)


class Signature(models.Model):
    STATUS = Choices(
        (0, 'new', 'New'),
        (10, 'signed', 'Signed'),
        (20, 'removed', 'Removed'),
    )
    id = HashidAutoField(
        primary_key=True,
    )
    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        help_text="""Real name strongly encouraged.  However, if necessary use a descriptor like 'Concerned Parent' or 'Father of Two'. (Required)""",
    )
    is_approved = models.BooleanField(
        default=False,
    )
    is_public = models.BooleanField(
        default=False,
        help_text="""List My Name on the Website.""",
    )
    message = models.TextField(
        max_length=512,
        blank=True,
        default='',
        help_text="""Feel free to include a public message attached to your signature.""",
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    account = models.ForeignKey(
        'app.Account',
        on_delete=models.CASCADE,
        related_name='signatures',
    )
    petition = models.ForeignKey(
        'app.Petition',
        on_delete=models.CASCADE,
        related_name='signatures',
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    'account',
                    'petition',
                ],
                name='unique_signature',
            )
        ]


class User(AbstractBaseUser):
    id = HashidAutoField(
        primary_key=True,
    )
    username = models.CharField(
        max_length=150,
        blank=False,
        unique=True,
    )
    email = models.EmailField(
        blank=False,
        unique=True,
    )
    is_active = models.BooleanField(
        default=False,
    )
    is_admin = models.BooleanField(
        default=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
