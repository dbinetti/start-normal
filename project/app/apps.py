# Django
from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'
    def ready(self):
        from .signals import user_post_delete, user_post_save

        import algoliasearch_django as algoliasearch

        from .indexes import SchoolIndex
        School = self.get_model('school')
        algoliasearch.register(School, SchoolIndex)

        from .indexes import HomeroomIndex
        Homeroom = self.get_model('homeroom')
        algoliasearch.register(Homeroom, HomeroomIndex)
