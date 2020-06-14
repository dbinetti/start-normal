# Standard Libary
from textwrap import wrap

# Django
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# First-Party
from django_rq import job
from mailchimp3 import MailChimp


# Utility
def build_email(template, context, subject, to=[], cc=[], bcc=[], attachments=[]):
    body = render_to_string(template, context)
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email='David Binetti <dbinetti@startnormal.com>',
        to=to,
        cc=cc,
        bcc=bcc,
    )
    for attachment in attachments:
        with attachment[1].open() as f:
            email.attach(attachment[0], f.read(), attachment[2])
    return email

@job
def send_email(email):
    return email.send()


@job
def subscribe_email(email):
    client = MailChimp(mc_api=settings.MAILCHIMP_API_KEY)
    data = {
        'email_address': email,
        'status': 'subscribed',
    }
    result = client.lists.members.create(
        list_id=settings.MAILCHIMP_AUDIENCE_ID,
        data=data,
    )
    return result
