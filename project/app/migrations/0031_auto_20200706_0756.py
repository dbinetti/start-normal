# Generated by Django 3.0.8 on 2020-07-06 14:56

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_auto_20200706_0748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='name', unique=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='name', unique=True),
        ),
    ]
