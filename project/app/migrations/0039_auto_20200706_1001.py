# Generated by Django 3.0.8 on 2020-07-06 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_auto_20200706_1001'),
    ]

    operations = [
        migrations.RenameField(
            model_name='district',
            old_name='cd_status',
            new_name='status',
        ),
    ]
