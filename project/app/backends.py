# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# Local
from .models import User


class Auth0Backend(ModelBackend):

    def authenticate(self, request, **kwargs):
        username = kwargs.get('username', None)
        email = kwargs.get('email', None)
        name = kwargs.get('name', None)
        # TODO CSRF attack mitigation
        # browser_state = kwargs.get('state', None)
        # session_state = request.session.get('state', None)
        # if browser_state != session_state:
        #     return None
        try:
            user = User.objects.get(
                username=username,
            )
        except User.DoesNotExist:
            user = User(
                username=username,
                email=email,
                name=name,
            )
            user.set_unusable_password()
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
