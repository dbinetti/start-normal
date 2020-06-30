# Django
from django.db.models.signals import post_delete
from django.dispatch import receiver

# First-Party
from app.models import User
from app.tasks import build_email
from app.tasks import mailchimp_delete_email
from app.tasks import send_email

# @receiver(post_delete, sender=User)
# def user_post_delete(sender, instance, **kwargs):
#     user = instance
#     result = mailchimp_delete_email.delay(user.email)
#     email = build_email(
#         to=[user.email],
#         subject='Signature Deleted',
#         template='emails/delete.txt',
#         bcc=['dbinetti@startnormal.com'],
#     )
#     send_email.delay(email)
#     return
