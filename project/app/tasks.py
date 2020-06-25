# Standard Libary
# Standard Library
import json
from textwrap import wrap

# Django
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# First-Party
from django_rq import job
from mailchimp3 import MailChimp
from mailchimp3.helpers import get_subscriber_hash
from mailchimp3.mailchimpclient import MailChimpError


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
def mailchimp_subscribe_email(email):
    client = MailChimp(mc_api=settings.MAILCHIMP_API_KEY)
    data = {
        'email_address': email,
        'status': 'subscribed',
    }
    try:
        result = client.lists.members.create(
            list_id=settings.MAILCHIMP_AUDIENCE_ID,
            data=data,
        )
    except MailChimpError as e:
        result = str(e)
    return result


@job
def mailchimp_subscribe_signature(signature):
    client = MailChimp(mc_api=settings.MAILCHIMP_API_KEY)
    data = {
        'email_address': signature.email,
        'status': 'subscribed',
        'tags': [
            {'name': signature.location, 'status': 'active'}
        ],
    }
    try:
        result = client.lists.members.create(
            list_id=settings.MAILCHIMP_AUDIENCE_ID,
            data=data,
        )
    except MailChimpError as e:
        error = json.loads(str(e).replace("\'", "\""))
        if error['title'] == 'Member Exists':
            result =  "Member Exists"
        elif error['title'] == 'Invalid Resource':
            user = CustomUser.objects.get(
                email=email,
            )
            user.is_active = False
            user.save()
            result = 'Invalid Resource'
        else:
            raise e
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

@job
def mailchimp_add_tag(signature):
    email = signature.email
    location = signature.get_location_display()
    list_id = settings.MAILCHIMP_AUDIENCE_ID
    subscriber_hash = get_subscriber_hash(email)
    data = {
        'tags': [
            {'name': location, 'status': 'active'},
        ]
    }
    client = MailChimp(mc_api=settings.MAILCHIMP_API_KEY)
    try:
        result =  client.lists.members.tags.update(
            list_id=list_id,
            subscriber_hash=subscriber_hash,
            data=data,
        )
    except MailChimpError as e:
        error = json.loads(str(e).replace("\'", "\""))
        if error['title'] == 'Resource Not Found':
            result =  "Resource Not Found"
        else:
            raise e # Invalid Resource
    except Exception as e:
        result = e
    return result
