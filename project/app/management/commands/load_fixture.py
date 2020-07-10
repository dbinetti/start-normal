# Django
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

# First-Party
from app.models import Account
from app.models import Affiliation
from app.models import Contact
from app.models import Organization
from app.models import Report
from app.models import Student
from app.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Set Cursor
        admin = User.objects.create(
            username='auth0|5f07d616a1f6030019b0a1ea',
            name='Admin',
            email='dbinetti@startnormal.com',
            is_active=True,
            is_admin=True,
        )
        user = User.objects.create(
            username='auth0|5f086f442eb3030019c85c54',
            name='Foo Bar',
            email='foo@startnormal.com',
            is_active=True,
            is_admin=False,
        )
        scsd = Organization.objects.create(
            is_active=True,
            name='San Carlos School District',
            status=Organization.STATUS.active,
            kind=Organization.KIND.elementary,
            nces_id=5400,
            address='123 Main St',
            city='San Carlos',
            state='CA',
            website='https://foobar.com',
            lon=32.0,
            lat=-122.0,
        )

        central = Organization.objects.create(
            is_active=True,
            name='Central Middle',
            status=Organization.STATUS.active,
            kind=Organization.KIND.hs,
            nces_id=5405,
            address='123 Main St',
            city='San Carlos',
            state='CA',
            website='https://www.foobar.com',
            lon=32.0,
            lat=-122.0,
            parent=scsd,
        )

        ba = Organization.objects.create(
            is_active=True,
            name='Brittan Acres',
            status=Organization.STATUS.active,
            kind=Organization.KIND.elem,
            nces_id=5402,
            address='123 Main St',
            city='San Carlos',
            state='CA',
            website='https://www.foobar.com',
            lon=32.0,
            lat=-122.0,
            parent=scsd,
        )
        Student.objects.create(
            grade=Student.GRADE.sixth,
            user=user,
            organization=central,
        )
        Student.objects.create(
            grade=Student.GRADE.third,
            user=user,
            organization=ba,
        )
        Contact.objects.create(
            name='Mao Harmeier',
            role=Contact.ROLE.super,
            organization=scsd,
        )
        Contact.objects.create(
            name='Suzanne Fast',
            role=Contact.ROLE.principal,
            organization=ba,
        )
        Contact.objects.create(
            name='Tom Domer',
            role=Contact.ROLE.principal,
            organization=central,
        )
        Report.objects.create(
            name='Bad news',
            status=Report.STATUS.approved,
            text="Now is the time for all good men to come to the aid of their schools!",
            organization=central,
            user=user,
        )
        self.stdout.write("Complete.")
        return
