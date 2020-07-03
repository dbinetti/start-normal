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
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0
from django_rq import job
from mailchimp3 import MailChimp
from mailchimp3.helpers import get_subscriber_hash
from mailchimp3.mailchimpclient import MailChimpError


def auth0_get_client():
    get_token = GetToken(settings.AUTH0_DOMAIN)
    token = get_token.client_credentials(
        settings.AUTH0_CLIENT_ID,
        settings.AUTH0_SECRET,
        'https://{}/api/v2/'.format(settings.AUTH0_DOMAIN),
    )
    mgmt_api_token = token['access_token']
    client = Auth0(
        settings.AUTH0_DOMAIN,
        mgmt_api_token,
    )
    return client

@job
def auth0_delete_user(username):
    client = auth0_get_client()
    result = client.users.delete(username)
    return


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


# @job
# def mailchimp_add_tag(signature):
#     client = get_mailchimp_client()
#     email = signature.email
#     location = signature.get_location_display()
#     list_id = settings.MAILCHIMP_AUDIENCE_ID
#     subscriber_hash = get_subscriber_hash(email)
#     data = {
#         'tags': [
#             {'name': location, 'status': 'active'},
#         ]
#     }
#     try:
#         result =  client.lists.members.tags.update(
#             list_id=list_id,
#             subscriber_hash=subscriber_hash,
#             data=data,
#         )
#     except MailChimpError as e:
#         error = json.loads(str(e).replace("\'", "\""))
#         if error['title'] == 'Resource Not Found':
#             result =  "Resource Not Found"
#         else:
#             raise e # Invalid Resource
#     except Exception as e:
#         result = e
#     return result


@job
def mailchimp_create_or_update_from_account(account):
    client = get_mailchimp_client()
    list_id = settings.MAILCHIMP_AUDIENCE_ID
    subscriber_hash = get_subscriber_hash(account.email)
    data = {
        'status_if_new': 'subscribed',
        'email_address': account.email,
        'merge_fields': {
            'NAME': account.name,
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
                email=account.email,
            )
            user.is_active = False
            user.save()
            result = 'Invalid Resource'
        else:
            raise e
    return result
