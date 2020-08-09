# Django
# Third-Party
from autoslug import AutoSlugField
from hashid_field import HashidAutoField
from model_utils import Choices
from multiselectfield import MultiSelectField

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

# Local
from .managers import UserManager

# class Classmate(models.Model):
#     id = HashidAutoField(
#         primary_key=True,
#     )
#     STATUS = Choices(
#         (0, 'new', 'New'),
#         (10, 'invited', 'Invited'),
#         (20, 'accepted', 'Accepted'),
#     )
#     status = models.IntegerField(
#         blank=False,
#         choices=STATUS,
#         default=STATUS.new,
#     )
#     student = models.ForeignKey(
#         'Student',
#         on_delete=models.CASCADE,
#         related_name='classmates',
#     )
#     homeroom = models.ForeignKey(
#         'Homeroom',
#         on_delete=models.CASCADE,
#         related_name='classmates',
#     )

#     def __str__(self):
#         return str(self.student.name)


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
    homeroom = models.ForeignKey(
        'Homeroom',
        on_delete=models.CASCADE,
        related_name='asks',
    )
    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        related_name='asks',
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


class Parent(models.Model):
    MASKS = Choices(
        (0, 'none', "No Preference"),
        (10, 'required', "Required"),
        (20, 'optional', "Optional"),
    )
    DISTANCE = Choices(
        (0, 'none', "No Preference"),
        (10, 'required', "Required"),
        (20, 'optional', "Optional"),
    )
    id = HashidAutoField(
        primary_key=True,
    )
    is_host = models.BooleanField(
        default=False,
    )
    masks = models.IntegerField(
        blank=True,
        null=True,
        choices=MASKS,
        default=MASKS.none
    )
    distance = models.IntegerField(
        blank=True,
        null=True,
        choices=DISTANCE,
        default=DISTANCE.none
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
        return str(self.id)


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
        return (self.lat, self.lon)

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
    cd_id = models.BigIntegerField(
        blank=True,
        null=True,
        unique=True,
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
    district = models.ForeignKey(
        'District',
        on_delete=models.SET_NULL,
        related_name='schools',
        null=True,
        blank=True,
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
    MASKS = Choices(
        (0, 'none', "No Preference"),
        (10, 'required', "Required"),
        (20, 'optional', "Optional"),
    )
    DISTANCE = Choices(
        (0, 'none', "No Preference"),
        (10, 'required', "Required"),
        (20, 'optional', "Optional"),
    )
    SCHEDULE = Choices(
        (0, 'none', "No Preference"),
        (10, 'light', "1-2 Days"),
        (20, 'moderate', "3-4 Days"),
        (30, 'heavy', "5 Days"),
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
    status = models.IntegerField(
        blank=False,
        choices=STATUS,
        default=STATUS.open,
    )
    kind = models.IntegerField(
        blank=False,
        choices=KIND,
        default=KIND.public,
    )
    masks = models.IntegerField(
        blank=True,
        null=True,
        choices=MASKS,
        default=MASKS.none
    )
    distance = models.IntegerField(
        blank=True,
        null=True,
        choices=DISTANCE,
        default=DISTANCE.none
    )
    schedule = models.IntegerField(
        blank=True,
        null=True,
        choices=SCHEDULE,
        default=SCHEDULE.none
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

    @property
    def size(self):
        return self.students.count()

    @property
    def nomen(self):
        nomen = "{0} - {1} - {2}".format(
            self.parent.user.name,
            ", ".join(self.schools),
            ", ".join(self.grades),
        )
        return nomen

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
        return str(self.id)

        # return "{0} - {1}".format(
        #     self.parent,
        #     ", ".join(
        #         self.students.values_list('name', flat=True),
        #     )
        # )


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
