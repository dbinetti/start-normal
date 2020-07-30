# Django
from django.test.client import Client

# First-Party
import pytest
from algoliasearch_django.decorators import disable_auto_indexing
from app.factories import AccountFactory
from app.factories import UserFactory


@pytest.fixture
def anon_client():
    client = Client()
    return client


@pytest.fixture
def user_client():
    user = UserFactory(
        username='user',
        name='User',
        email='user@startnormal.com',
        is_active=True,
        is_admin=False,
    )
    AccountFactory(
        user=user,
    )
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def admin_client():
    admin = UserFactory(
        username='admin',
        name='Admin',
        email='admin@startnormal.com',
        is_active=True,
        is_admin=True,
    )
    client = Client()
    client.force_login(admin)
    return client
