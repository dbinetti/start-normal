# Django
from django.db import models


class Signature(models.Model):

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
        blank=True,
    )
    notes = models.TextField(
        max_length=255,
        null=True,
        blank=True,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )
