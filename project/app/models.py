# Standard Library
from operator import attrgetter

# Django
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils.text import slugify

# First-Party
import shortuuid
from autoslug import AutoSlugField
from hashid_field import HashidAutoField
from model_utils import Choices
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from multiselectfield import MultiSelectField
from shortuuidfield import ShortUUIDField

# Local
from .managers import UserManager


def get_populate_from(instance):
    fields = [
        'name',
        'city',
        'state',
    ]
    values = [getattr(instance, field) for field in fields]
    return slugify("-".join(values))


class Account(models.Model):
    TEACHER = Choices(
        (510, 'ps', 'Preschool'),
        (520, 'elem', 'Elementary'),
        (530, 'intmidjr', 'Intermediate/Middle/Junior High'),
        (540, 'hs', 'High School'),
        (550, 'elemhigh', 'Elementary-High Combination'),
        (560, 'a', 'Adult'),
        (570, 'ug', 'Ungraded'),
    )

    id = HashidAutoField(
        primary_key=True,
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
    teacher = models.IntegerField(
        blank=True,
        null=True,
        choices=TEACHER,
    )
    message = models.TextField(
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

    # TODO Cruft
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
    location = models.CharField(
        max_length=255,
        choices=LOCATION,
        blank=True,
        help_text="""Your city. (Required)""",
    )
    notes = models.TextField(
        max_length=512,
        blank=True,
        default='',
        help_text="""Feel free to include private notes just for us.""",
    )


    def __str__(self):
        return str(self.user)


class Parent(models.Model):
    id = HashidAutoField(
        primary_key=True,
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
        related_name='parent',
    )

    def __str__(self):
        return str(self.user)


class Teacher(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    is_credential = models.BooleanField(
        default=False,
        help_text="""Are you credentialed?""",
    )
    KIND = Choices(
        (510, 'ps', 'Preschool'),
        (520, 'elem', 'Elementary'),
        (530, 'intmidjr', 'Intermediate/Middle/Junior High'),
        (540, 'hs', 'High School'),
    )
    kinds = MultiSelectField(
        choices=KIND,
        null=True,
        help_text="""What levels do you teach?""",
    )
    SUBJECT = Choices(
        (110, 'ps', 'English'),
        (120, 'ps', 'History'),
        (130, 'ps', 'Mathematics'),
        (140, 'ps', 'Science'),
        (150, 'ps', 'Art'),
        (160, 'ps', 'Music'),
        (170, 'ps', 'PE'),
        (180, 'ps', 'Other'),
    )
    subjects = MultiSelectField(
        choices=SUBJECT,
        null=True,
        help_text="""What subjects do you teach?""",
    )
    school = models.ForeignKey(
        'app.School',
        related_name='teachers',
        on_delete=models.SET_NULL,
        null=True,
        help_text="""Pick a near where you'd like to teach (dosn't have to be your own school; this is just for location.)""",
    )
    notes = models.TextField(
        max_length=512,
        blank=True,
        default='',
        help_text="""Please add anything else you think we should know.""",
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
        related_name='teacher',
    )
    def __str__(self):
        return str(self.user)


class District(models.Model):

    STATUS = Choices(
        (10, 'active', "Active"),
        (20, 'closed', "Closed"),
        (30, 'merged', "Merged"),
    )
    KIND = Choices(
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
        (470, 'private', 'Private'),
        (498, 'roc', 'Regional Occupational Center/Program (ROC/P)'),
        (499, 'admin', 'Administration Only'),
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
    description = models.TextField(
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
    cd_id = models.BigIntegerField(
        blank=True,
        null=True,
        unique=True,
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

    def __str__(self):
        return "{0} - {1}, {2}".format(
            self.name,
            self.city,
            self.state,
        )

    def location(self):
        return(self.lat, self.lon)

    def should_index(self):
        if self.status == self.STATUS.active:
            return True
        return False


class School(models.Model):

    STATUS = Choices(
        (0, 'new', "New"),
        (10, 'active', "Active"),
        (20, 'closed', "Closed"),
        (30, 'merged', "Merged"),
    )
    KIND = Choices(
        (510, 'ps', 'Preschool'),
        (520, 'elem', 'Elementary'),
        (530, 'intmidjr', 'Intermediate/Middle/Junior High'),
        (540, 'hs', 'High School'),
        (550, 'elemhigh', 'Elementary-High Combination'),
        (560, 'a', 'Adult'),
        (570, 'ug', 'Ungraded'),
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
    description = models.TextField(
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
        default=STATUS.new,
    )
    kind = models.IntegerField(
        blank=False,
        null=True,
        choices=KIND,
    )
    cd_id = models.BigIntegerField(
        blank=True,
        null=True,
        unique=True,
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
        blank=False,
        default='',
    )
    state = models.CharField(
        max_length=255,
        blank=False,
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
    district = models.ForeignKey(
        'District',
        on_delete=models.SET_NULL,
        related_name='schools',
        null=True,
    )

    def __str__(self):
        return "{0} - {1}, {2}".format(
            self.name,
            self.city,
            self.state,
        )

    def location(self):
        return(self.lat, self.lon)

    def should_index(self):
        if self.status == self.STATUS.active:
            return True
        return False


class Homeroom(models.Model):

    STATUS = Choices(
        (0, 'new', "New"),
        (10, 'active', "Active"),
    )
    GRADE = Choices(
        (2, 'tk', 'Transitional Kindergarten'),
        (5, 'k', 'Kindergarten'),
        (10, 'first', 'First  Grade'),
        (20, 'second', 'Second  Grade'),
        (30, 'third', 'Third  Grade'),
        (40, 'fourth', 'Fourth  Grade'),
        (50, 'fifth', 'Fifth  Grade'),
        (60, 'sixth', 'Sixth  Grade'),
        (70, 'seventh', 'Seventh Grade'),
        (80, 'eighth', 'Eighth Grade'),
        (90, 'ninth', 'Ninth Grade'),
        (100, 'tenth', 'Tenth Grade'),
        (110, 'eleventh', 'Eleventh Grade'),
        (120, 'twelfth', 'Twelfth Grade'),
        (130, 'fresh', 'Freshman'),
        (140, 'soph', 'Sophomore'),
    )
    id = HashidAutoField(
        primary_key=True,
    )
    name = models.CharField(
        max_length=255,
        blank=False,
    )
    description = models.TextField(
        blank=True,
    )
    slug = AutoSlugField(
        max_length=255,
        always_update=True,
        populate_from='name',
        unique=True,
    )
    status = models.IntegerField(
        blank=False,
        choices=STATUS,
        default=STATUS.new,
    )
    grade = models.IntegerField(
        blank=False,
        choices=GRADE,
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
    owner = models.ForeignKey(
        'Parent',
        on_delete=models.SET_NULL,
        related_name='homerooms',
        null=True,
    )

    def __str__(self):
        return str(self.name)

    def location(self):
        return(self.lat, self.lon)


class Classroom(models.Model):

    STATUS = Choices(
        (0, 'new', "New"),
        (10, 'active', "Active"),
    )
    SUBJECT = Choices(
        (110, 'ps', 'English'),
        (120, 'ps', 'History'),
        (130, 'ps', 'Mathematics'),
        (140, 'ps', 'Science'),
        (150, 'ps', 'Art'),
        (160, 'ps', 'Music'),
        (170, 'ps', 'PE'),
        (180, 'ps', 'Other'),
    )
    id = HashidAutoField(
        primary_key=True,
    )
    name = models.CharField(
        max_length=255,
        blank=False,
    )
    description = models.TextField(
        blank=True,
    )
    status = models.IntegerField(
        blank=False,
        choices=STATUS,
        default=STATUS.new,
    )
    subjects = MultiSelectField(
        choices=SUBJECT,
        null=True,
    )
    venue = models.CharField(
        max_length=255,
        blank=True,
        default='',
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
    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        related_name='classrooms',
        null=True,
    )
    homeroom = models.ForeignKey(
        'Homeroom',
        on_delete=models.SET_NULL,
        related_name='classrooms',
        null=True,
    )

    def __str__(self):
        return "{0} - {1}".format(
            self.teacher,
            self.homeroom,
        )

    def location(self):
        return(self.lat, self.lon)

    def should_index(self):
        if self.status == self.STATUS.active:
            return True
        return False


class Contact(models.Model):
    ROLE = Choices(
        (410, 'super', 'Superintendent'),
        (420, 'president', 'Board President'),
        (430, 'vice', 'Board Vice-President'),
        (440, 'clerk', 'Board Clerk'),
        (450, 'trustee', 'Board Trustee'),
        (460, 'admin', 'Administrative'),
        (510, 'principal', 'Principal'),
        (900, 'unknown', 'Unknown'),
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
        blank=False,
        choices=ROLE,
    )
    email = models.EmailField(
        blank=False,
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
    user = models.ForeignKey(
        'app.User',
        related_name='contacts',
        on_delete=models.SET_NULL,
        null=True,
    )
    def __str__(self):
        return str(self.name)


class Invite(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATUS = Choices(
        (0, 'new', 'New'),
        (10, 'sent', 'Sent'),
        (20, 'accepted', 'Accepted'),
    )
    GRADE = Choices(
        (2, 'tk', 'Transitional Kindergarten'),
        (5, 'k', 'Kindergarten'),
        (10, 'first', 'First  Grade'),
        (20, 'second', 'Second  Grade'),
        (30, 'third', 'Third  Grade'),
        (40, 'fourth', 'Fourth  Grade'),
        (50, 'fifth', 'Fifth  Grade'),
        (60, 'sixth', 'Sixth  Grade'),
        (70, 'seventh', 'Seventh Grade'),
        (80, 'eighth', 'Eighth Grade'),
        (90, 'ninth', 'Ninth Grade'),
        (100, 'tenth', 'Tenth Grade'),
        (110, 'eleventh', 'Eleventh Grade'),
        (120, 'twelfth', 'Twelfth Grade'),
        (130, 'fresh', 'Freshman'),
        (140, 'soph', 'Sophomore'),
    )
    grade = models.IntegerField(
        blank=True,
        choices=GRADE,
        null=True,
    )
    status = models.IntegerField(
        blank=False,
        choices=STATUS,
        default=STATUS.new,
    )
    parent_name = models.CharField(
        max_length=255,
        blank=False,
    )
    parent_email = models.EmailField(
        blank=False,
    )
    student_name = models.CharField(
        max_length=255,
        blank=False,
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
    inviter = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='invites',
    )
    homeroom = models.ForeignKey(
        'Homeroom',
        related_name='invites',
        on_delete=models.SET_NULL,
        null=True,
    )
    def __str__(self):
        return str(self.id)

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
    title = models.CharField(
        max_length=100,
        blank=False,
        help_text="""Give a brief title (ideally no more than five words.)""",
    )
    text = models.TextField(
        blank=False,
        help_text="""Use your own voice, but please stick to the facts as much as possible; we want to be a credible source to all parents.""",
    )
    is_district = models.BooleanField(
        default=True,
        help_text="""Keep this checked if your update applies to the entire school district.  If unsure, keep it checked -- it probably does.""",
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    user = models.ForeignKey(
        'app.User',
        related_name='reports',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.title)


class Student(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    GRADE = Choices(
        (2, 'tk', 'Transitional Kindergarten'),
        (5, 'k', 'Kindergarten'),
        (10, 'first', 'First  Grade'),
        (20, 'second', 'Second  Grade'),
        (30, 'third', 'Third  Grade'),
        (40, 'fourth', 'Fourth  Grade'),
        (50, 'fifth', 'Fifth  Grade'),
        (60, 'sixth', 'Sixth  Grade'),
        (70, 'seventh', 'Seventh Grade'),
        (80, 'eighth', 'Eighth Grade'),
        (90, 'ninth', 'Ninth Grade'),
        (100, 'tenth', 'Tenth Grade'),
        (110, 'eleventh', 'Eleventh Grade'),
        (120, 'twelfth', 'Twelfth Grade'),
        (130, 'fresh', 'Freshman'),
        (140, 'soph', 'Sophomore'),
    )
    grade = models.IntegerField(
        blank=False,
        choices=GRADE,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    parent = models.ForeignKey(
        'app.Parent',
        on_delete=models.CASCADE,
        related_name='students',
    )
    school = models.ForeignKey(
        'app.School',
        related_name='students',
        on_delete=models.CASCADE,
    )
    homeroom = models.ForeignKey(
        'Homeroom',
        related_name='students',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.id)


class Transmission(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    report = models.ForeignKey(
        'app.Report',
        on_delete=models.CASCADE,
        related_name='transmissions',
    )
    school = models.ForeignKey(
        'app.School',
        on_delete=models.CASCADE,
        related_name='transmissions',
    )
    def __str__(self):
        return str(self.id)


class Entry(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    contact = models.ForeignKey(
        'app.Contact',
        on_delete=models.CASCADE,
        related_name='entries',
    )
    school = models.ForeignKey(
        'app.School',
        on_delete=models.CASCADE,
        related_name='entries',
    )
    def __str__(self):
        return str(self.id)


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
