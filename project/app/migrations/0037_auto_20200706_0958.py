# Generated by Django 3.0.8 on 2020-07-06 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_auto_20200706_0957'),
    ]

    operations = [
        migrations.RenameField(
            model_name='school',
            old_name='cd_status',
            new_name='status',
        ),
    ]
