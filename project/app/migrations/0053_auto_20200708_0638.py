# Generated by Django 3.0.8 on 2020-07-08 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0052_auto_20200708_0506'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='signature',
            name='unique_signature',
        ),
    ]
