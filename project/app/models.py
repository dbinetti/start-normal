# Django
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.text import slugify

# First-Party
import shortuuid
from model_utils import Choices
from shortuuidfield import ShortUUIDField

# Local
from .managers import UserManager


class Contact(models.Model):
    ROLE = Choices(
        (10, 'super', 'Superintendent'),
        (20, 'super', 'Board President'),
        (30, 'super', 'Board Vice-President'),
        (40, 'super', 'Board Clerk'),
        (50, 'super', 'Board Trustee'),
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


class District(models.Model):

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
    def __str__(self):
        return str(self.name)


class Faq(models.Model):

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


class Registration(models.Model):

    email = models.EmailField(
        blank=False,
        unique=True,
        help_text="""Your email will not be used for any purpose other than registration for this Q&A."""
    )
    name = models.CharField(
        max_length=255,
        blank=False,
        help_text="""Your name will be used during the Q&A but otherwise will remain private.  Registration for the Q&A DOES NOT signify support for Start Normal."""
    )
    notes = models.TextField(
        max_length=512,
        blank=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    def __str__(self):
        return str(self.name)


class Signature(models.Model):
    user = models.OneToOneField(
        'app.User',
        on_delete=models.CASCADE,
        null=True,
        related_name='signature',
    )
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
    location = models.CharField(
        max_length=255,
        choices=LOCATION,
        null=True,
        blank=False,
        help_text="""Your city. (Required)""",
    )
    district = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="""Your school district. (Optional)""",
    )
    phone = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="""Your mobile phone. (Optional)""",
    )
    is_volunteer = models.BooleanField(
        default=False,
        help_text="""If you're willing to volunteer in some manner please check this box. """,
    )
    is_teacher = models.BooleanField(
        default=False,
        help_text="""If you're an educator please check this box. """,
    )
    is_doctor = models.BooleanField(
        default=False,
        help_text="""If you're a physician please check this box. """,
    )
    email = models.EmailField(
        null=True,
        blank=False,
        unique=True,
        help_text="""Your email is private and not shared.  It's used to manage preferences and send adminstrative updates. (Required)""",
    )
    notes = models.TextField(
        max_length=512,
        null=True,
        blank=True,
        default=None,
        help_text="""Feel free to include private notes just for us.""",
    )
    message = models.TextField(
        max_length=512,
        null=True,
        blank=True,
        default=None,
        help_text="""Feel free to include a public message attached to your signature.""",
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return str(self.name)


class User(AbstractBaseUser):
    id = ShortUUIDField(
        primary_key=True,
    )

    username = models.CharField(
        max_length=150,
        blank=False,
        unique=True,
    )

    email = models.EmailField(
        blank=True,
        unique=True,
        null=True,
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
    REQUIRED_FIELDS = [
    ]

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
