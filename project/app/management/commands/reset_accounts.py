# Django
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

# First-Party
from app.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.filter(
            email__endswith='@startnormal.com',
        )
        users.delete()
        self.stdout.write("Complete.")
        return
