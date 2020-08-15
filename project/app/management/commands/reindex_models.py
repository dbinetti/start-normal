# Django
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import SearchVector
from django.core.management.base import BaseCommand
from django.db.models import F
from django.db.models import Value

# First-Party
from app.models import Homeroom
from app.models import School
from app.models import Student


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
        ss = Student.objects.annotate(
            sv=SearchVector(
                'name',
                # 'get_gender_display',
                'school__name',
                # 'school__get_grade_display',
                'parent__name',
                'parent__email',
            )
        )
        for s in ss:
            s.search_vector = s.sv
            s.save()
        self.stdout.write("Complete.")
        return
