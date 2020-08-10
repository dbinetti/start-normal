# Generated by Django 3.1 on 2020-08-10 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0054_parent_safety'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='frequency',
            field=models.IntegerField(blank=True, choices=[(0, 'No Preference'), (10, '1-2 Days'), (20, '3-4 Days'), (30, '5 Days')], default=0, null=True),
        ),
        migrations.AlterField(
            model_name='parent',
            name='schedule',
            field=models.IntegerField(blank=True, choices=[(0, 'No Preference'), (10, 'Morning'), (20, 'Afternoon'), (30, 'Full Day')], default=0, null=True),
        ),
    ]
