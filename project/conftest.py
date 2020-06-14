import pytest
# Django
from django.test.client import Client


@pytest.fixture
def anon_client():
    client = Client()
    return client
