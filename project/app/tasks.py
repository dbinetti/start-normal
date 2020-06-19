# Standard Libary
from textwrap import wrap

# Third-Party
from django_rq import job
from mailchimp3 import MailChimp
from mailchimp3.helpers import get_subscriber_hash

# Django
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@job
def claim_account(user):
    email = user.email
    signature = user.signature
    form = PasswordResetForm({'email': email})
    if form.is_valid():
        return form.save(
            domain_override='www.startnormal.com',
            subject_template_name='emails/account_claim_subject.txt',
            from_email='David Binetti <dbinetti@startnormal.com>',
            email_template_name='emails/account_claim.html',
            extra_email_context={'signature':signature},
        )
    return 'Error {0}'.format(user)

# Utility
def build_email(template, subject, context=None, to=[], cc=[], bcc=[], attachments=[]):
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
def welcome_email(signature):
    email = signature.email
    form = PasswordResetForm({'email': email})
    if form.is_valid():
        return form.save(
            domain_override='www.startnormal.com',
            subject_template_name='emails/welcome_subject.txt',
            email_template_name='emails/welcome.html',
            from_email='David Binetti <dbinetti@startnormal.com>',
            extra_email_context={'signature': signature},
        )
    return 'Error {0}'.format(email)


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


@job
def mailchimp_delete_email(email):
    subscriber_hash = get_subscriber_hash(email)
    client = MailChimp(mc_api=settings.MAILCHIMP_API_KEY)
    result = client.lists.members.delete_permanent(
        list_id=settings.MAILCHIMP_AUDIENCE_ID,
        subscriber_hash=subscriber_hash,
    )
    return result
