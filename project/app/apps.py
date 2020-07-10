# Django
from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'
    def ready(self):
        from .signals import user_post_delete, user_post_save

        import algoliasearch_django as algoliasearch
        from .indexes import OrganizationIndex
        Organization = self.get_model('organization')
        algoliasearch.register(Organization, OrganizationIndex)
