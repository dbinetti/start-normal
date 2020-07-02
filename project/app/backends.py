# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# Local
from .models import User


class Auth0Backend(ModelBackend):

    def authenticate(self, request, username, **kwargs):
        try:
            user = User.objects.get(
                username=username,
            )
        except User.DoesNotExist:
            user = User(
                username=username,
                is_active=True,
            )
            user.set_unusable_password()
            user.save()
        # if user.is_active:
        #     return user
        # return None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
