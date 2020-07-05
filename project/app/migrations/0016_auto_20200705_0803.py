# Generated by Django 3.0.8 on 2020-07-05 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20200705_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='doc',
            field=models.IntegerField(blank=True, choices=[(0, 'County Office of Education'), (2, 'State Board of Education'), (3, 'Statewide Benefit Charter'), (31, 'State Special Schools'), (34, 'Non-school Location*'), (42, 'Joint Powers Authority (JPA)'), (52, 'Elementary School District'), (54, 'Unified School District'), (56, 'High School District'), (58, 'Community College District'), (98, 'Regional Occupational Center/Program (ROC/P)'), (99, 'Administration Only')], null=True),
        ),
    ]
