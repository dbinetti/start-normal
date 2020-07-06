# Generated by Django 3.0.8 on 2020-07-06 15:25

import app.models
import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_auto_20200706_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, max_length=255, populate_from=app.models.get_populate_from, unique=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, max_length=255, populate_from=app.models.get_populate_from, unique=True),
        ),
    ]
