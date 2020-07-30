# Django
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# First-Party
import pytest


def test_deploy():
    assert False


def test_index_anon(anon_client):
    path = reverse('index')
    response = anon_client.get(path)
    assert response.status_code == 200

# @pytest.mark.django_db
# def test_index_user(user_client):
#     path = reverse('index')
#     response = user_client.get(path)
#     assert response.status_code == 200

# def test_account_anon(anon_client):
#     path = reverse('account')
#     response = anon_client.get(path)
#     assert response.status_code == 302

# @pytest.mark.django_db
# def test_account_user(user_client):
#     path = reverse('account')
#     response = user_client.get(path)
#     assert response.status_code == 200

# def test_about(anon_client):
#     path = reverse('about')
#     response = anon_client.get(path)
#     assert response.status_code == 200
