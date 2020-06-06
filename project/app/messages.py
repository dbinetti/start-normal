# Local
# First-Party
from django_rq import job

from .models import *
from .tasks import build_email


@job
def send_email(email):
    return email.send()


def send_first():

    signatures = Signature.objects.exclude(
        email=None,
    )

    for signature in signatures:

        template = 'emails/initials.txt'
        context = {'signature': signature}
        subject = "Start Normal - Update #1"
        to = [signature.email]

        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
        )
        send_email.delay(email)
