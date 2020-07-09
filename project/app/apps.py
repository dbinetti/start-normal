# Django
from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'
    def ready(self):
        from .signals import user_post_delete, user_post_save

        import algoliasearch_django as algoliasearch
        from .indexes import PetitionIndex
        Petition = self.get_model('petition')
        algoliasearch.register(Petition, PetitionIndex)
