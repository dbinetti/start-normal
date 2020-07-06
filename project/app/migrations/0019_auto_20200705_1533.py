# Generated by Django 3.0.8 on 2020-07-05 22:33

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20200705_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True),
        ),
    ]
