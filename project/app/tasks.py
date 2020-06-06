# Standard Libary
from textwrap import wrap

# Django
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# First-Party
from django_rq import job


# Utility
def build_email(template, context, subject, to, cc=[], bcc=[], attachments=[]):
    # Clean as necessary
    # Remove commas
    # to = [x.replace(",", "") for x in to]
    # cc = [x.replace(",", "") for x in cc]
    # bcc = [x.replace(",", "") for x in bcc]

    # # Remove duplicate emails, keeping only the first
    # full = []
    # clean_to = []
    # clean_cc = []
    # clean_bcc = []
    # for address in to:
    #     if not address.partition("<")[2].partition(">")[0] in full:
    #         clean_to.append(address)
    #     full.append(address.partition("<")[2].partition(">")[0])
    # for address in cc:
    #     if not address.partition("<")[2].partition(">")[0] in full:
    #         clean_cc.append(address)
    #     full.append(address.partition("<")[2].partition(">")[0])
    # for address in bcc:
    #     if not address.partition("<")[2].partition(">")[0] in full:
    #         clean_bcc.append(address)
    #     full.append(address.partition("<")[2].partition(">")[0])


    body = render_to_string(template, context)
    # wrapped = wrap(body)
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email='David Binetti <dbinetti@gmail.com>',
        to=to,
    )
    for attachment in attachments:
        with attachment[1].open() as f:
            email.attach(attachment[0], f.read(), attachment[2])
    return email
