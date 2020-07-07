# Django
from django.test.client import Client

# First-Party
import pytest


@pytest.fixture
def anon_client():
    client = Client()
    return client
