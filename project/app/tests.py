# Django
# Third-Party
import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# First-Party
from app.forms import SignatureForm


class IndexView(TestCase):
    def test_index(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    # def test_transcript(self):
    #     """
    #     If no questions exist, an appropriate message is displayed.
    #     """
    #     response = self.client.get(reverse('transcript'))
    #     self.assertEqual(response.status_code, 200)

    # def test_letter(self):
    #     """
    #     If no questions exist, an appropriate message is displayed.
    #     """
    #     response = self.client.get(reverse('letter'))
    #     self.assertEqual(response.status_code, 200)

    def test_thanks(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('thanks'))
        self.assertEqual(response.status_code, 200)

    def test_signature_form(self):
        form_data = {
            'name': 'foobar',
            'email': 'foo@bar.com',
            'location': 'sc',
        }
        form = SignatureForm(data=form_data)
        self.assertTrue(form.is_valid())


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='normal@user.com',
            password='foo',
        )
        self.assertEqual(user.email, 'normal@user.com')
        self.assertFalse(user.is_admin)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_admin)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_admin=False)


def test_homepage(anon_client):
    path = reverse('index')
    response = anon_client.get(path)
    assert response.status_code == 200

@pytest.mark.django_db
def test_sign(anon_client):
    path = reverse('sign')
    response = anon_client.post(
        path, {
            'name': 'Foo Bar',
            'email': 'foo@bar.com',
            'location': 'sc',
        }
    )
    assert response.status_code == 302
