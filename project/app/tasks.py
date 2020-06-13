# Standard Libary
from textwrap import wrap

# Django
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# First-Party
from django_rq import job


# Utility
def build_email(template, context, subject, to=[], cc=[], bcc=[], attachments=[]):
    body = render_to_string(template, context)
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email='David Binetti <dbinetti@gmail.com>',
        to=to,
        cc=cc,
        bcc=bcc,
    )
    for attachment in attachments:
        with attachment[1].open() as f:
            email.attach(attachment[0], f.read(), attachment[2])
    return email
