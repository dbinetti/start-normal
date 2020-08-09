# Django
from django.contrib.postgres.search import SearchVector
from django.core.management.base import BaseCommand

# First-Party
from app.models import School


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Set Cursor
        School.objects.update(
            search_vector=SearchVector(
                'name',
                'city',
                'state',
            )
        )
        self.stdout.write("Complete.")
        return
