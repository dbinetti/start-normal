# Generated by Django 3.0.8 on 2020-07-19 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0051_remove_student_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='district',
        ),
    ]
