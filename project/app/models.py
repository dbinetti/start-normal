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
    )
    is_approved = models.BooleanField(
        default=False,
    )
    city = models.CharField(
        max_length=255,
        null=True,
        blank=False,
    )
    is_public = models.BooleanField(
        default=False,
    )
    is_subscribed = models.BooleanField(
        default=False,
    )
    location = models.CharField(
        max_length=255,
        choices=Location.choices,
        null=True,
        blank=False,
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
    )
    notes = models.TextField(
        max_length=255,
        null=True,
        blank=True,
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return str(self.name)
