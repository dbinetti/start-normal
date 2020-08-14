# Django
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import SearchVector
from django.core.management.base import BaseCommand
from django.db.models import F
from django.db.models import Value

# First-Party
from app.models import Homeroom
from app.models import School


class Command(BaseCommand):
    def handle(self, *args, **options):
        School.objects.update(
            search_vector=SearchVector(
                'name',
                'city',
                'state',
            )
        )
        hs = Homeroom.objects.annotate(
            sv=SearchVector(
                'parent__name',
                'parent__email',
                StringAgg('students__name', ' '),
            )
        )
        for h in hs:
            h.search_vector = h.sv
            h.save()
        self.stdout.write("Complete.")
        return
