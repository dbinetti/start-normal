from django.core.mail import EmailMessage

# from django_rq import job


# @job
def queue_email(subject, body, to):
    mail = EmailMessage(
        subject=subject,
        body=body,
        from_email='David Binetti <dbinetti@gmail.com>',
        to=to,
        bcc=['dbinetti@gmail.com'],
    )
    return mail.send()
