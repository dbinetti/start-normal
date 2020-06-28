# Standard Libary
# Standard Library
import json
from textwrap import wrap

# Django
from django.conf import settings
from django.contrib.auth import get_user_model
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



def get_segment_id(location):
    segment_map = {
        'ath': 684132,
        'bel': 684136,
        'brb': 684140,
        'bur': 684144,
        'col': 684148,
        'dc': 684152,
        'epa': 684156,
        'fc': 684160,
        'hmb': 684164,
        'hil': 684168,
        'mp': 684172,
        'mil': 684176,
        'pac': 684180,
        'pv': 684184,
        'rc': 684188,
        'sb': 684192,
        'sc': 684196,
        'sm': 684200,
        'ssf': 684204,
        'ws': 684208,
        'un': 684212,
        'out': 684216,
    }
    return segment_map[location]


def get_mailchimp_client():
    enabled = not settings.DEBUG
    return MailChimp(
        mc_api=settings.MAILCHIMP_API_KEY,
        enabled=enabled,
    )


@job
def mailchimp_subscribe_email(email):
    client = get_mailchimp_client()
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
def mailchimp_delete_email(email):
    client = get_mailchimp_client()
    subscriber_hash = get_subscriber_hash(email)
    client = MailChimp(mc_api=settings.MAILCHIMP_API_KEY)
    result = client.lists.members.delete(
        list_id=settings.MAILCHIMP_AUDIENCE_ID,
        subscriber_hash=subscriber_hash,
    )
    return result

@job
def mailchimp_add_tag(signature):
    client = get_mailchimp_client()
    email = signature.email
    location = signature.get_location_display()
    list_id = settings.MAILCHIMP_AUDIENCE_ID
    subscriber_hash = get_subscriber_hash(email)
    data = {
        'tags': [
            {'name': location, 'status': 'active'},
        ]
    }
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

@job
def mailchimp_subscribe_signature(signature):
    client = get_mailchimp_client()
    list_id = settings.MAILCHIMP_AUDIENCE_ID
    subscriber_hash = get_subscriber_hash(signature.email)
    data = {
        'status_if_new': 'subscribed',
        'email_address': signature.email,
        'merge_fields': {
            'NAME': signature.name,
            'LOCATION': signature.get_location_display(),
        }
    }
    try:
        result = client.lists.members.create_or_update(
            list_id=list_id,
            subscriber_hash=subscriber_hash,
            data=data,
        )
    except MailChimpError as e:
        error = json.loads(str(e).replace("\'", "\""))
        if error['title'] == 'Invalid Resource':
            User = get_user_model()
            user = User.objects.get(
                email=signature.email,
            )
            user.is_active = False
            user.save()
            result = 'Invalid Resource'
        else:
            raise e
    return result
