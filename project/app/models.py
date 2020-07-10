# Standard Library
from operator import attrgetter

# Third-Party
import shortuuid
from autoslug import AutoSlugField
from hashid_field import HashidAutoField
from model_utils import Choices
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from shortuuidfield import ShortUUIDField

# Django
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils.text import slugify

# Local
from .managers import UserManager


def get_populate_from(instance):
    if instance.kind in range(400, 500):
        fields = [
            'name',
            'county',
            'state',
        ]
    elif instance.kind in range(500, 600):
        fields = [
            'name',
            'city',
            'state',
        ]
    else:
        fields = [
            'name',
        ]
    values = [getattr(instance, field) for field in fields]
    return slugify("-".join(values))

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
    is_public = models.BooleanField(
        default=True,
        help_text="""List name on website.""",
    )
    is_subscribe = models.BooleanField(
        default=True,
        help_text="""Subscribe for updates.""",
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
    message = models.TextField(
        max_length=512,
        blank=True,
        default='',
        help_text="""Feel free to include private notes just for us.""",
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
        return str(self.user)


class Contact(models.Model):
    ROLE = Choices(
        (410, 'super', 'Superintendent'),
        (420, 'president', 'Board President'),
        (430, 'vice', 'Board Vice-President'),
        (440, 'clerk', 'Board Clerk'),
        (450, 'trustee', 'Board Trustee'),
        (510, 'principal', 'Principal'),
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
    organization = models.ForeignKey(
        'app.Organization',
        related_name='contacts',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.name)


class Report(models.Model):
    STATUS = Choices(
        (0, 'new', 'New'),
        (10, 'approved', 'Approved'),
        (20, 'rejected', 'Rejected'),
    )
    id = HashidAutoField(
        primary_key=True,
    )
    status = models.IntegerField(
        blank=False,
        choices=STATUS,
        default=STATUS.new,
    )
    name = models.CharField(
        max_length=100,
        blank=False,
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
    organization = models.ForeignKey(
        'app.Organization',
        related_name='reports',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'app.User',
        related_name='reports',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.name)


class Organization(MPTTModel):

    STATUS = Choices(
        (10, 'active', "Active"),
        (20, 'closed', "Closed"),
        (30, 'merged', "Merged"),
    )
    KIND = Choices(
        ('District', [
            (400, 'county', 'County Office of Education'),
            (402, 'state', 'State Board of Education'),
            (403, 'charter', 'Statewide Benefit Charter'),
            (431, 'special', 'State Special Schools'),
            (434, 'non', 'Non-school Location*'),
            (442, 'jpa', 'Joint Powers Authority (JPA)'),
            (452, 'elementary', 'Elementary School District'),
            (454, 'unified', 'Unified School District'),
            (456, 'high', 'High School District'),
            (458, 'ccd', 'Community College District'),
            (498, 'roc', 'Regional Occupational Center/Program (ROC/P)'),
            (499, 'admin', 'Administration Only'),
        ]),
        ('School', [
            (510, 'ps', 'Preschool'),
            (520, 'elem', 'Elementary'),
            (530, 'intmidjr', 'Intermediate/Middle/Junior High'),
            (540, 'hs', 'High School'),
            (550, 'elemhigh', 'Elementary-High Combination'),
            (560, 'a', 'Adult'),
            (570, 'ug', 'Ungraded'),
        ]),
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
    text = models.TextField(
        blank=True,
    )
    slug = AutoSlugField(
        max_length=255,
        always_update=True,
        populate_from=get_populate_from,
        unique=True,
    )
    status = models.IntegerField(
        blank=False,
        choices=STATUS,
        default=STATUS.active,
    )
    kind = models.IntegerField(
        blank=True,
        null=True,
        choices=KIND,
    )
    nces_id = models.IntegerField(
        blank=True,
        null=True,
        unique=True,
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )
    city = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )
    state = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )
    zipcode = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )
    county = models.CharField(
        max_length=255,
        blank=True,
    )
    phone = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )
    website = models.URLField(
        blank=True,
        default='',
    )
    lat = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        blank=True,
    )
    lon = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        blank=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )

    def __str__(self):
        return str(self.name)

    def location(self):
        return(self.lat, self.lon)

    def should_index(self):
        if self.is_active and self.kind >=500:
            return True
        return False

    class MPTTMeta:
        order_insertion_by = ['name']


class Affiliation(models.Model):
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
        default=STATUS.signed,
    )
    is_approved = models.BooleanField(
        default=False,
    )
    message = models.TextField(
        max_length=512,
        blank=True,
        default='',
        help_text="""Feel free to include a public message attached to your affiliation.""",
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    user = models.ForeignKey(
        'app.User',
        on_delete=models.CASCADE,
        related_name='affiliations',
    )
    organization = models.ForeignKey(
        'app.Organization',
        related_name='affiliations',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.name)

    # class Meta:
    #     constraints = [
    #         UniqueConstraint(
    #             fields=[
    #                 'user',
    #                 'organization',
    #             ],
    #             name='unique_affiliation',
    #         )
    #     ]


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
    name = models.CharField(
        max_length=255,
        blank=False,
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
        'name',
    ]

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
