# Django
from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'
    def ready(self):
        pass
        # from .signals import user_post_delete, user_post_save
        # import algoliasearch_django as algoliasearch

        # from .indexes import DepartmentIndex
        # Department = self.get_model('department')
        # algoliasearch.register(Department, DepartmentIndex)
