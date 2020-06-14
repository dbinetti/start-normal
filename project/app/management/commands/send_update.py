from app.tasks import build_email, send_email
from django.contrib.auth import get_user_model
# Django
from django.core.management.base import BaseCommand

# First-Party
User = get_user_model()


class Command(BaseCommand):
    help = "Send update."

    def add_arguments(self, parser):
        parser.add_argument(
            '--template',
            dest='template',
            help='Template Path.',
        )

        parser.add_argument(
            '--subject',
            dest='subject',
            help='Subject Line.',
        )


    def handle(self, *args, **options):

        self.stdout.write("Queuing Update.")

        template = options['template']
        subject = options['subject']

        users = User.objects.filter(
            is_active=True,
        ).order_by('created')
        t = users.count()
        i = 0
        for user in users:
            i += 1
            self.stdout.flush()
            self.stdout.write("Queueing {0} of {1} Messages...".format(i, t), ending='\r')
            to = [user.email]
            context = {'user': user}
            email = build_email(
                template=template,
                subject=subject,
                context=context,
                to=to,
            )
            send_email.delay(email)

        self.stdout.write("")
        self.stdout.write("Queued {0} Messages".format(t))
