# Django
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

    def test_transcript(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('transcript'))
        self.assertEqual(response.status_code, 200)

    def test_letter(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('letter'))
        self.assertEqual(response.status_code, 200)

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
            'city': 'city',
        }
        form = SignatureForm(data=form_data)
        self.assertTrue(form.is_valid())
