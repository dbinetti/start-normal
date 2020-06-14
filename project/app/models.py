# Django
# Third-Party
import shortuuid
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from shortuuidfield import ShortUUIDField

# Local
from .managers import CustomUserManager


class Signature(models.Model):
    user = models.OneToOneField(
        'app.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
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
        help_text="""Be aware your real name makes a real a difference.  However, we recognize the need for privacy so use something like 'Concerned Parent' or 'Father of Two' if you feel you must.  Your signature will be part of the public record.""",
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
    )
    is_subscribed = models.BooleanField(
        default=True,
    )
    location = models.CharField(
        max_length=255,
        choices=Location.choices,
        null=True,
        blank=False,
        help_text="""This helps provide specificity to Mr. Callagy.""",
    )
    phone = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    is_volunteer = models.BooleanField(
        default=False,
    )
    email = models.EmailField(
        null=True,
        blank=False,
        help_text="""Your email is private and not shared.  We need it to manage preferences and send updates.  If you do not wish updates, unclick the 'Send Updates' checkbox.""",
    )
    notes = models.TextField(
        max_length=255,
        null=True,
        blank=True,
        default=None,
        help_text="""Feel free to include anything you think we should know.  For instance, many have used this box to indicate they are teachers who are supportive of starting normal -- and we love to hear that!""",
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
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

# @receiver(post_save, sender=User)
# def update_signature_signal(sender, instance, created, **kwargs):
#     if created:
#         Signature.objects.create(user=instance)
#     instance.profile.save()
