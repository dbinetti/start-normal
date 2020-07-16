# Django
from django.test.client import Client

# First-Party
import pytest
from algoliasearch_django.decorators import disable_auto_indexing
from app.factories import UserFactory


@pytest.fixture
def anon_client():
    client = Client()
    return client


@pytest.fixture
def user_client():
    user = UserFactory(
        username='auth0|5f07d7e7fd30e200136652f6',
        name='Foo Bar',
        email='foo@startnormal.com',
        is_active=True,
        is_admin=False,
    )
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def admin_client():
    admin = UserFactory(
        username='auth0|5f07d616a1f6030019b0a1ea',
        name='Admin',
        email='dbinetti@startnormal.com',
        is_active=True,
        is_admin=True,
    )
    client = Client()
    client.force_login(admin)
    return client


@pytest.fixture
def school():
    school = SchoolFactory()
    return school

@pytest.fixture
def district():
    district = DistrictFactory()
    return district
