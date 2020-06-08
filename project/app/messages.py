# Local
# First-Party
from django_rq import job

from .models import *
from .tasks import build_email


@job
def send_email(email):
    return email.send()


def send_first():

    signatures = Signature.objects.filter(
        email__isnull=False,
        is_subscribed=True,
    ).order_by('timestamp')

    for signature in signatures:

        template = 'emails/second.txt'
        context = {'signature': signature}
        subject = "Start Normal - Update #2"
        to = [signature.email]

        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
        )
        send_email.delay(email)
