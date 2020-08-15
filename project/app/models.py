# Django
# Third-Party
from autoslug import AutoSlugField
from django_fsm import FSMIntegerField
from hashid_field import HashidAutoField
from model_utils import Choices
from multiselectfield import MultiSelectField

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

# Local
from .managers import UserManager


class Classmate(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATUS = Choices(
        (0, 'new', "New"),
        (10, 'pending', "Pending"),
        (20, 'accepted', "Accepted"),
        (30, 'rejected', "Rejected"),
    )
    status = FSMIntegerField(
        blank=True,
        choices=STATUS,
        default=STATUS.new,
    )
    message = models.TextField(
        blank=True,
        default='',
    )
    from_student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        blank=False,
        related_name='classmates_from',
    )
    to_student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        blank=False,
        related_name='classmates_to',
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )


class Ask(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATUS = Choices(
        (0, 'new', "New"),
        (10, 'invited', "Invited"),
    )
    GENDER = Choices(
        (None, 'none', '-- Choose Gender --'),
        (10, 'boy', 'Boy'),
        (20, 'girl', 'Girl'),
    )
    GRADE = Choices(
        (None, 'none', '-- Choose Grade --'),
        (-1, 'p', 'Preschool'),
        (0, 'k', 'Kindergarten'),
        (1, 'first', 'First Grade'),
        (2, 'second', 'Second Grade'),
        (3, 'third', 'Third Grade'),
        (4, 'fourth', 'Fourth Grade'),
        (5, 'fifth', 'Fifth Grade'),
        (6, 'sixth', 'Sixth Grade'),
        (7, 'seventh', 'Seventh Grade'),
        (8, 'eighth', 'Eighth Grade'),
        (9, 'ninth', 'Ninth Grade'),
        (10, 'tenth', 'Tenth Grade'),
        (11, 'eleventh', 'Eleventh Grade'),
        (12, 'twelfth', 'Twelfth Grade'),
    )
    status = FSMIntegerField(
        blank=True,
        choices=STATUS,
        default=STATUS.new,
    )
    student_name = models.CharField(
        max_length=255,
        blank=False,
        default='',
    )
    parent_name = models.CharField(
        max_length=255,
        blank=False,
        default='',
    )
    parent_email = models.EmailField(
        max_length=255,
        blank=False,
        default='',
    )
    gender = models.IntegerField(
        blank=True,
        null=True,
        choices=GENDER,
    )
    grade = models.IntegerField(
        blank=True,
        choices=GRADE,
        null=True,
    )
    message = models.TextField(
        blank=True,
        default='',
    )
    homeroom = models.ForeignKey(
        'Homeroom',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='asks',
    )
    student = models.ForeignKey(
        'Student',
        on_delete=models.SET_NULL,
        null=True,
        related_name='asks',
        blank=True,
    )
    school = models.ForeignKey(
        'app.School',
        related_name='asks',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )


class Account(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    is_welcomed = models.BooleanField(
        default=False,
    )
    phone = models.CharField(
        max_length=255,
        blank=True,
        help_text="""Your mobile phone. (Optional)""",
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


class Parent(models.Model):
    SCHEDULE = Choices(
        (0, 'none', "No Schedule Preference"),
        (10, 'morning', "Morning"),
        (20, 'afternoon', "Afternoon"),
        (30, 'full', "Full Day"),
    )
    FREQUENCY = Choices(
        (0, 'none', "No Frequency Preference"),
        (10, 'light', "1-2 Days"),
        (20, 'moderate', "3-4 Days"),
        (30, 'heavy', "5 Days"),
    )
    SAFETY = Choices(
        (0, 'none', "No Safety Preference"),
        (10, 'standard', "Standard"),
        (20, 'enhanced', "Enhanced"),
    )
    id = HashidAutoField(
        primary_key=True,
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )
    email = models.EmailField(
        blank=True,
        default='',
    )
    phone = models.CharField(
        max_length=255,
        blank=True,
        help_text="""Your mobile phone. (Optional)""",
        default='',
    )
    is_host = models.BooleanField(
        default=False,
    )
    is_welcomed = models.BooleanField(
        default=False,
    )
    safety = models.IntegerField(
        blank=False,
        choices=SAFETY,
        default=SAFETY.none
    )
    schedule = models.IntegerField(
        blank=False,
        choices=SCHEDULE,
        default=SCHEDULE.none
    )
    frequency = models.IntegerField(
        blank=False,
        choices=FREQUENCY,
        default=FREQUENCY.none
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
        on_delete=models.SET_NULL,
        null=True,
        related_name='parent',
    )

    def __str__(self):
        return str(self.user)


class Teacher(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    LEVEL = Choices(
        (510, 'ps', 'Preschool'),
        (520, 'elem', 'Elementary'),
        (530, 'intmidjr', 'Intermediate/Middle/Junior High'),
        (540, 'hs', 'High School'),
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
    is_credential = models.BooleanField(
        default=False,
        help_text="""Are you credentialed?""",
    )
    levels = MultiSelectField(
        choices=LEVEL,
        null=True,
        help_text="""What levels do you teach?""",
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
        help_text="""Pick a school near where you'd like to teach (doesn't have to be your own school; this is just for location.)""",
    )
    rate = models.CharField(
        max_length=512,
        blank=True,
        default='',
        help_text="""What is your hourly rate range?""",
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


class School(models.Model):

    STATUS = Choices(
        (0, 'new', "New"),
        (10, 'active', "Active"),
        (20, 'closed', "Closed"),
        (30, 'merged', "Merged"),
    )
    KIND = Choices(
        (0, 'new', "New"),
        (10, 'public', "Public"),
        (20, 'private', "Private"),
    )
    LEVEL = Choices(
        (510, 'ps', 'Preschool'),
        (520, 'elem', 'Elementary'),
        (530, 'intmidjr', 'Intermediate/Middle/Junior High'),
        (540, 'hs', 'High School'),
        (550, 'elemhigh', 'Elementary-High Combination'),
        (555, 'secondary', 'Secondary'),
        (560, 'a', 'Adult'),
        (570, 'ug', 'Ungraded'),
    )
    GRADE = Choices(
        (-1, 'p', 'Preschool'),
        (0, 'k', 'Kindergarten'),
        (1, 'first', 'First Grade'),
        (2, 'second', 'Second Grade'),
        (3, 'third', 'Third Grade'),
        (4, 'fourth', 'Fourth Grade'),
        (5, 'fifth', 'Fifth Grade'),
        (6, 'sixth', 'Sixth Grade'),
        (7, 'seventh', 'Seventh Grade'),
        (8, 'eighth', 'Eighth Grade'),
        (9, 'ninth', 'Ninth Grade'),
        (10, 'tenth', 'Tenth Grade'),
        (11, 'eleventh', 'Eleventh Grade'),
        (12, 'twelfth', 'Twelfth Grade'),
    )
    id = HashidAutoField(
        primary_key=True,
    )
    status = FSMIntegerField(
        blank=False,
        choices=STATUS,
        default=STATUS.new,
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
    kind = models.IntegerField(
        blank=False,
        choices=KIND,
        default=KIND.new,
    )
    level = models.IntegerField(
        blank=True,
        null=True,
        choices=LEVEL,
    )
    nces_id = models.CharField(
        max_length=50,
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
    grades = ArrayField(
        models.IntegerField(
            choices=GRADE,
        ),
        blank=True,
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
    geo = models.JSONField(
        encoder=DjangoJSONEncoder,
        null=True,
        blank=True,
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
    search_vector = SearchVectorField(
        null=True,
    )

    def __str__(self):
        return "{0} - {1}, {2}".format(
            self.name,
            self.city,
            self.state,
        )

    def location(self):
        return (self.lat, self.lon)

    def grades_display(self):
        return [self.GRADE[x] for x in self.grades]

    def should_index(self):
        if self.status == self.STATUS.active:
            return True
        return False

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector'])
        ]


class Homeroom(models.Model):

    STATUS = Choices(
        (10, 'open', "Open"),
        (20, 'closed', "Closed"),
    )
    KIND = Choices(
        (10, 'public', "Public"),
        (20, 'private', "Private"),
    )
    GOAL = Choices(
        (10, 'instruction', "Instruction"),
        (20, 'social', "Social"),
    )
    SCHEDULE = Choices(
        (0, 'none', "No Schedule Preference"),
        (10, 'morning', "Morning"),
        (20, 'afternoon', "Afternoon"),
        (30, 'full', "Full Day"),
    )
    FREQUENCY = Choices(
        (0, 'none', "No Frequency Preference"),
        (10, 'light', "1-2 Days"),
        (20, 'moderate', "3-4 Days"),
        (30, 'heavy', "5 Days"),
    )
    SAFETY = Choices(
        (0, 'none', "No Safety Preference"),
        (10, 'standard', "Standard"),
        (20, 'enhanced', "Enhanced"),
    )
    GRADE = Choices(
        (-1, 'p', 'Preschool'),
        (0, 'k', 'Kindergarten'),
        (1, 'first', 'First Grade'),
        (2, 'second', 'Second Grade'),
        (3, 'third', 'Third Grade'),
        (4, 'fourth', 'Fourth Grade'),
        (5, 'fifth', 'Fifth Grade'),
        (6, 'sixth', 'Sixth Grade'),
        (7, 'seventh', 'Seventh Grade'),
        (8, 'eighth', 'Eighth Grade'),
        (9, 'ninth', 'Ninth Grade'),
        (10, 'tenth', 'Tenth Grade'),
        (11, 'eleventh', 'Eleventh Grade'),
        (12, 'twelfth', 'Twelfth Grade'),
    )
    id = HashidAutoField(
        primary_key=True,
    )
    status = FSMIntegerField(
        blank=False,
        choices=STATUS,
        default=STATUS.open,
    )
    kind = models.IntegerField(
        blank=False,
        choices=KIND,
        default=KIND.public,
    )
    goal = models.IntegerField(
        blank=False,
        choices=GOAL,
        default=GOAL.instruction,
    )
    safety = models.IntegerField(
        blank=True,
        null=True,
        choices=SAFETY,
        default=SAFETY.none
    )
    schedule = models.IntegerField(
        blank=True,
        null=True,
        choices=SCHEDULE,
        default=SCHEDULE.none
    )
    frequency = models.IntegerField(
        blank=True,
        null=True,
        choices=FREQUENCY,
        default=FREQUENCY.none
    )
    lat = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        blank=True,
        default=0.0,
    )
    lon = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        default=0.0,
        blank=True,
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
    search_vector = SearchVectorField(
        null=True,
    )

    @property
    def size(self):
        return self.students.count()

    @property
    def schools(self):
        schools = self.students.values_list(
            'school__name', flat=True
        ).order_by(
            'school__name',
        ).distinct()
        return list(set(schools))

    @property
    def grades(self):
        grades = self.students.values_list(
            'grade', flat=True,
        ).order_by(
            'grade',
        ).distinct()
        return list(set([self.GRADE[x] for x in grades]))

    def parent_name(self):
        try:
            parent = self.parent
        except AttributeError:
            return "(No Owner)"
        return parent.user.name

    def student_names(self):
        try:
            students = self.students.values_list('name', flat=True)
        except AttributeError:
            return "(No Students)"
        return ", ".join(list(students))

    def location(self):
        try:
            school = self.students.first().school
        except AttributeError:
            return (0.0, 0.0)
        return (school.lat, school.lon)

    def should_index(self):
        if self.kind == self.KIND.public:
            return True
        return False

    def __str__(self):
        return "{0} - {1}".format(
            self.parent,
            ", ".join(
                self.students.values_list('name', flat=True),
            )
        )

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector'])
        ]


class Student(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATUS = Choices(
        (0, 'new', 'New'),
        (10, 'approved', 'Approved'),
        (20, 'rejected', 'Rejected'),
    )
    GENDER = Choices(
        (None, 'none', '-- Choose Gender --'),
        (10, 'boy', 'Boy'),
        (20, 'girl', 'Girl'),
    )
    GRADE = Choices(
        (None, 'none', '-- Choose Grade --'),
        (-1, 'p', 'Preschool'),
        (0, 'k', 'Kindergarten'),
        (1, 'first', 'First Grade'),
        (2, 'second', 'Second Grade'),
        (3, 'third', 'Third Grade'),
        (4, 'fourth', 'Fourth Grade'),
        (5, 'fifth', 'Fifth Grade'),
        (6, 'sixth', 'Sixth Grade'),
        (7, 'seventh', 'Seventh Grade'),
        (8, 'eighth', 'Eighth Grade'),
        (9, 'ninth', 'Ninth Grade'),
        (10, 'tenth', 'Tenth Grade'),
        (11, 'eleventh', 'Eleventh Grade'),
        (12, 'twelfth', 'Twelfth Grade'),
    )
    status = FSMIntegerField(
        blank=False,
        choices=STATUS,
        default=STATUS.new,
    )
    name = models.CharField(
        max_length=100,
        blank=False,
        help_text="""This will be shown to other parents on the private site; it will not appear on the public site.  """,
    )
    gender = models.IntegerField(
        blank=False,
        null=True,
        choices=GENDER,
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
        on_delete=models.SET_NULL,
        null=True,
    )
    homeroom = models.ForeignKey(
        'Homeroom',
        related_name='students',
        on_delete=models.SET_NULL,
        null=True,
    )
    search_vector = SearchVectorField(
        null=True,
    )

    @property
    def initials(self):
        return str(self.name[:1])

    def __str__(self):
        return "{0} - {1}".format(
            self.name,
            self.parent.name,
        )
    class Meta:
        indexes = [
            GinIndex(fields=['search_vector'])
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
