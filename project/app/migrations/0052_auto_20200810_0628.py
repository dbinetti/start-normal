# Generated by Django 3.1 on 2020-08-10 13:28

import django.contrib.postgres.indexes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0051_school_search_vector'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(10, 'Boy'), (20, 'Girl')], null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(help_text='This will be shown to other parents on the private site; it will not appear on the public site.  ', max_length=100),
        ),
        migrations.AddIndex(
            model_name='school',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='app_school_search__6fab6e_gin'),
        ),
    ]
