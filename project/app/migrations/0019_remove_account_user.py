# Generated by Django 3.0.8 on 2020-07-04 00:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_signature_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='user',
        ),
    ]
