# Django
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

# First-Party
from app.models import Account
from app.models import Petition
from app.models import Signature
from app.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Set Cursor

        admin = UserFactory(
            username='auth0|5f07d616a1f6030019b0a1ea',
            name='Admin',
            email='dbinetti@startnormal.com',
            is_active=True,
            is_admin=True,
        )
        user = UserFactory(
            username='auth0|5f07d7e7fd30e200136652f6',
            name='Foo Bar',
            email='foo@startnormal.com',
            is_active=True,
            is_admin=False,
        )
        user.refresh_from_db()
        account = user.account
        petition = PetitionFactory()
        SignatureFactory(
            account=account,
            petition=petition,
        )
        self.stdout.write("Complete.")
        return
