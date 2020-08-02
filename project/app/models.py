# Django
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

# First-Party
from autoslug import AutoSlugField
from hashid_field import HashidAutoField
from model_utils import Choices
from multiselectfield import MultiSelectField

# Local
from .managers import UserManager


class Classmate(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATUS = Choices(
        (0, 'new', 'New'),
        (10, 'invited', 'Invited'),
        (20, 'accepted', 'Accepted'),
    )
    status = models.IntegerField(
        blank=False,
        choices=STATUS,
        default=STATUS.new,
    )
    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        related_name='classmates',
    )
    homeroom = models.ForeignKey(
        'Homeroom',
        on_delete=models.CASCADE,
        related_name='classmates',
    )

    def __str__(self):
        return str(self.student.name)


class Roomparent(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATUS = Choices(
        (0, 'new', 'New'),
        (10, 'invited', 'Invited'),
        (20, 'accepted', 'Accepted'),
    )
    status = models.IntegerField(
        blank=False,
        choices=STATUS,
        default=STATUS.new,
    )
    parent = models.ForeignKey(
        'Parent',
        on_delete=models.CASCADE,
        related_name='roomparents',
    )
    homeroom = models.ForeignKey(
        'Homeroom',
        on_delete=models.CASCADE,
        related_name='roomparents',
    )


class Account(models.Model):
    id = HashidAutoField(
        primary_key=True,
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
        help_text="""Your mobile phone. (Optional)""",
    )
    is_welcomed = models.BooleanField(
        default=False,
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

    def has_classmates(self):
        return bool(self.user.parent.students.filter(classmates__isnull=False))


class Parent(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    is_host = models.BooleanField(
        default=False,
    )
    notes = models.TextField(
        max_length=512,
        blank=True,
        default='',
        help_text="""Notes.""",
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


class Invite(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    email = models.EmailField(
        blank=False,
        default='',
    )
    message = models.TextField(
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
        on_delete=models.CASCADE,
        related_name='invites',
    )

    def __str__(self):
        return str(self.email)


class Teacher(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    is_credential = models.BooleanField(
        default=False,
        help_text="""Are you credentialed?""",
    )
    LEVEL = Choices(
        (510, 'ps', 'Preschool'),
        (520, 'elem', 'Elementary'),
        (530, 'intmidjr', 'Intermediate/Middle/Junior High'),
        (540, 'hs', 'High School'),
    )
    levels = MultiSelectField(
        choices=LEVEL,
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
        help_text="""Pick a school near where you'd like to teach (dosn't have to be your own school; this is just for location.)""",
    )
    notes = models.TextField(
        max_length=2000,
        blank=True,
        default='',
        help_text="""Please add any other notes you think we should know.""",
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
    LEVEL = Choices(
        (510, 'ps', 'Preschool'),
        (520, 'elem', 'Elementary'),
        (530, 'intmidjr', 'Intermediate/Middle/Junior High'),
        (540, 'hs', 'High School'),
        (550, 'elemhigh', 'Elementary-High Combination'),
        (560, 'a', 'Adult'),
        (570, 'ug', 'Ungraded'),
    )
    GRADE = Choices(
        (2, 'tk', 'Preschool/PreK/Transitional K'),
        (5, 'k', 'Kindergarten'),
        (10, 'first', 'First Grade'),
        (20, 'second', 'Second Grade'),
        (30, 'third', 'Third Grade'),
        (40, 'fourth', 'Fourth Grade'),
        (50, 'fifth', 'Fifth Grade'),
        (60, 'sixth', 'Sixth Grade'),
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
        populate_from='__str__',
        unique=True,
    )
    status = models.IntegerField(
        blank=False,
        choices=STATUS,
        default=STATUS.new,
    )
    level = models.IntegerField(
        blank=False,
        null=True,
        choices=LEVEL,
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
    low_grade = models.IntegerField(
        blank=True,
        choices=GRADE,
        null=True,
    )
    high_grade = models.IntegerField(
        blank=True,
        choices=GRADE,
        null=True,
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
        (10, 'open', "Open"),
        (20, 'closed', "Closed"),
    )
    GRADE = Choices(
        (2, 'tk', 'Preschool'),
        (5, 'k', 'Kindergarten'),
        (10, 'first', 'First Grade'),
        (20, 'second', 'Second Grade'),
        (30, 'third', 'Third Grade'),
        (40, 'fourth', 'Fourth Grade'),
        (50, 'fifth', 'Fifth Grade'),
        (60, 'sixth', 'Sixth Grade'),
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
    status = models.IntegerField(
        blank=False,
        choices=STATUS,
        default=STATUS.new,
    )
    notes = models.TextField(
        blank=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    parent = models.ForeignKey(
        'Parent',
        on_delete=models.CASCADE,
        related_name='homerooms',
    )

    @property
    def grades(self):
        grades = self.classmates.values_list(
            'student__grade', flat=True,
        ).order_by(
            'student__grade',
        ).distinct()
        return list(set([self.GRADE[x] for x in grades]))

    @property
    def schools(self):
        schools = self.classmates.values_list(
            'student__school__name', flat=True
        ).order_by(
            'student__name',
        ).distinct()
        return list(set(schools))

    def __str__(self):
        return "{0}".format(
            self.id,
        )


class Student(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATUS = Choices(
        (0, 'new', 'New'),
        (10, 'approved', 'Approved'),
        (20, 'rejected', 'Rejected'),
    )
    status = models.IntegerField(
        blank=False,
        choices=STATUS,
        default=STATUS.new,
    )
    GRADE = Choices(
        (2, 'tk', 'Preschool'),
        (5, 'k', 'Kindergarten'),
        (10, 'first', 'First Grade'),
        (20, 'second', 'Second Grade'),
        (30, 'third', 'Third Grade'),
        (40, 'fourth', 'Fourth Grade'),
        (50, 'fifth', 'Fifth Grade'),
        (60, 'sixth', 'Sixth Grade'),
        (70, 'seventh', 'Seventh Grade'),
        (80, 'eighth', 'Eighth Grade'),
        (90, 'ninth', 'Ninth Grade'),
        (100, 'tenth', 'Tenth Grade'),
        (110, 'eleventh', 'Eleventh Grade'),
        (120, 'twelfth', 'Twelfth Grade'),
        (130, 'fresh', 'Freshman'),
        (140, 'soph', 'Sophomore'),
    )
    name = models.CharField(
        max_length=100,
        blank=False,
        help_text="""Your Student's name will be shown to other parents on the private site; it will not appear on the public site.  """,
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
    )

    @property
    def initials(self):
        return str(self.name[:1])

    def __str__(self):
        return "{0} - {1}".format(
            self.name,
            self.parent.user.name,
        )


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
        return str(self.name)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
