# Django
from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'
    def ready(self):
        from app.signals import (
            # user_post_save,
            # user_post_delete,
        )
