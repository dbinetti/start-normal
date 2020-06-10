# Django
from django.db import models


class Signature(models.Model):

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
        help_text="""Be aware your real name makes a real a difference.  However, we recognize that we're parents not protestors, and so use something like 'Concerned Parent' if you wish.""",
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
        help_text="""Feel free to include anything you think we should know.  For instance, many have used this box to indicate they are teachers who are supportive of starting normal -- and we love to hear that!""",
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return str(self.name)
