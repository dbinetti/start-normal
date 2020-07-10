# Standard Library
import datetime

# Third-Party
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

# Django
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_delete
from django.db.models.signals import post_save

# Local
from .models import Account
from .models import Contact
from .models import Petition
from .models import Report
from .models import Signature
from .models import User


@mute_signals(post_delete, post_save)
class AccountFactory(DjangoModelFactory):
    is_public = True
    user = RelatedFactory(
        'app.factories.AccountFactory',
        factory_related_name='account',
    )
    class Meta:
        model = Account


class ContactFactory(DjangoModelFactory):
    is_active = True
    name = 'Seymour Skinner'
    role = Contact.ROLE.principal
    # petition = RelatedFactory(
    #     'app.factories.PetitionFactory',
    #     factory_related_name='petition',
    # )
    class Meta:
        model = Contact


class ReportFactory(DjangoModelFactory):
    status = Report.STATUS.approved
    name = 'Bad News'
    text = 'Now is the time for all good men to come to the aid of their schools.'
    # petition = RelatedFactory(
    #     'app.factories.PetitionFactory',
    #     factory_related_name='petition',
    # )
    # user = RelatedFactory(
    #     'app.factories.UserFactory',
    #     factory_related_name='user',
    # )
    class Meta:
        model = Report


class PetitionFactory(DjangoModelFactory):
    is_active = True
    name = 'Central Middle'
    status = Petition.STATUS.active
    kind = Petition.KIND.intmidjr
    nces_id = 5401
    address = '123 Main St'
    city = 'San Carlos'
    state = 'CA'
    website = Faker('url')
    lon = 32.0
    lat = -122.0
    class Meta:
        model = Petition


class SignatureFactory(DjangoModelFactory):
    is_approved = True
    message = "Foo to the Bar!"
    # petition = RelatedFactory(
    #     'app.factories.PetitionFactory',
    #     factory_related_name='petition',
    # )
    # user = RelatedFactory(
    #     'app.factories.UserFactory',
    #     factory_related_name='user',
    # )
    class Meta:
        model = Signature


@mute_signals(post_delete, post_save)
class UserFactory(DjangoModelFactory):
    name = Faker('name_male')
    email = Faker('email')
    password = PostGenerationMethodCall('set_unusable_password')
    is_active = True
    account = SubFactory(
        'app.factories.AccountFactory',
        user=None,
    )
    class Meta:
        model = User
