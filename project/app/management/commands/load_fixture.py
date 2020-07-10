# Django
# Third-Party
from algoliasearch_django.decorators import disable_auto_indexing
from factory import Faker  # post_generation,
from factory import Iterator
from factory import LazyAttribute
from factory import PostGenerationMethodCall
from factory import RelatedFactory
from factory import Sequence
from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.django import mute_signals
from factory.fuzzy import FuzzyInteger

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

# First-Party
from app.factories import AccountFactory
from app.factories import ContactFactory
from app.factories import PetitionFactory
from app.factories import ReportFactory
from app.factories import SignatureFactory
from app.factories import UserFactory
from app.models import Contact
from app.models import Petition
from app.models import Report


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
            username='auth0|5f086f442eb3030019c85c54',
            name='Foo Bar',
            email='foo@startnormal.com',
            is_active=True,
            is_admin=False,
        )
        account = AccountFactory(
            user=user,
        )
        scsd = PetitionFactory(
            is_active=True,
            name='San Carlos School District',
            status=Petition.STATUS.active,
            kind=Petition.KIND.elementary,
            nces_id=5400,
            address='123 Main St',
            city='San Carlos',
            state='CA',
            website=Faker('url'),
            lon=32.0,
            lat=-122.0,
        )

        central = PetitionFactory(
            parent=scsd,
        )

        ba = PetitionFactory(
            is_active=True,
            name='Brittan Acres',
            status=Petition.STATUS.active,
            kind=Petition.KIND.elem,
            nces_id=5402,
            address='123 Main St',
            city='San Carlos',
            state='CA',
            website=Faker('url'),
            lon=32.0,
            lat=-122.0,
            parent=scsd,
        )
        SignatureFactory(
            user=user,
            petition=central,
        )
        ContactFactory(
            name='Mao Harmeier',
            role=Contact.ROLE.super,
            petition=scsd,
        )
        ContactFactory(
            name='Suzanne Fast',
            role=Contact.ROLE.principal,
            petition=ba,
        )
        ContactFactory(
            name='Tom Domer',
            role=Contact.ROLE.principal,
            petition=central,
        )
        ReportFactory(
            name='Bad news',
            status=Report.STATUS.approved,
            text="Now is the time for all good men to come to the aid of their schools!",
            petition=central,
            user=user,
        )
        self.stdout.write("Complete.")
        return
