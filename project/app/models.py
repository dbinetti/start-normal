# Django
# First-Party
import shortuuid
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.text import slugify
from shortuuidfield import ShortUUIDField

# Local
from .managers import CustomUserManager


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


class Signature(models.Model):
    user = models.OneToOneField(
        'app.CustomUser',
        on_delete=models.CASCADE,
        null=True,
        related_name='signature',
    )

    class Location(models.TextChoices):
        ATHERTON = 'ATH', ('Atherton')
        BELMONT = 'BEL', ('Belmont')
        BRISBANE = 'BRB', ('Brisbane')
        BURLINGAME = 'BUR', ('Burlingame')
        COLMA = 'COL', ('Colma')
        DC = 'DC', ('Daly City')
        EPA = 'EPA', ('East Palo Alto')
        FC = 'FC', ('Foster City')
        HMB = 'HMB', ('Half Moon Bay')
        HILLSBOROUGH = 'HIL', ('Hillsborough')
        MP = 'MP', ('Menlo Park')
        MILLBRAE = 'MIL', ('Millbrae')
        PACIFICA = 'PAC', ('Pacifica')
        PV = 'PV', ('Portola Valley')
        RC = 'RC', ('Redwood City')
        SB = 'SB', ('San Bruno')
        SC = 'SC', ('San Carlos')
        SM = 'SM', ('San Mateo')
        SSF = 'SSF', ('South San Francisco')
        WOODSIDE = 'WS', ('Woodside')
        UN = 'UN', ('Unincorporated San Mateo County')
        OUT = 'OUT', ('Outside of San Mateo County')

    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        help_text="""Real name strongly encouraged.  However, if necessary use a descriptor like 'Concerned Parent' or 'Father of Two'. (Required)""",
    )
    handle = models.CharField(
        max_length=255,
        null=False,
        blank=True,
        help_text="""Your public name is how it will appear on the website.  This could be your real name (which is the most powerful), or first name initial last name, or something like 'Father of Two'.  If blank, defaults to your real name.""",
    )
    is_approved = models.BooleanField(
        default=False,
    )
    city = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    is_public = models.BooleanField(
        default=False,
        help_text="""List My Name on the Website.""",

    )
    is_subscribed = models.BooleanField(
        default=True,
    )
    location = models.CharField(
        max_length=255,
        choices=Location.choices,
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
        max_length=255,
        null=True,
        blank=True,
        default=None,
        help_text="""Feel free to include anything else you think we should know.""",
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return str(self.name)




class CustomUser(AbstractBaseUser):
    id = ShortUUIDField(
        primary_key=True,
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
    ]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

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
