# Generated by Django 3.1 on 2020-08-08 13:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_school_grades'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='grades',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(choices=[(-1, 'Preschool'), (0, 'Kindergarten'), (1, 'First Grade'), (2, 'Second Grade'), (3, 'Third Grade'), (4, 'Fourth Grade'), (5, 'Fifth Grade'), (6, 'Sixth Grade'), (7, 'Seventh Grade'), (8, 'Eighth Grade'), (9, 'Ninth Grade'), (10, 'Tenth Grade'), (11, 'Eleventh Grade'), (12, 'Twelfth Grade')]), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='school',
            name='high_grade',
            field=models.IntegerField(blank=True, choices=[(-1, 'Preschool'), (0, 'Kindergarten'), (1, 'First Grade'), (2, 'Second Grade'), (3, 'Third Grade'), (4, 'Fourth Grade'), (5, 'Fifth Grade'), (6, 'Sixth Grade'), (7, 'Seventh Grade'), (8, 'Eighth Grade'), (9, 'Ninth Grade'), (10, 'Tenth Grade'), (11, 'Eleventh Grade'), (12, 'Twelfth Grade')], null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='low_grade',
            field=models.IntegerField(blank=True, choices=[(-1, 'Preschool'), (0, 'Kindergarten'), (1, 'First Grade'), (2, 'Second Grade'), (3, 'Third Grade'), (4, 'Fourth Grade'), (5, 'Fifth Grade'), (6, 'Sixth Grade'), (7, 'Seventh Grade'), (8, 'Eighth Grade'), (9, 'Ninth Grade'), (10, 'Tenth Grade'), (11, 'Eleventh Grade'), (12, 'Twelfth Grade')], null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='grade',
            field=models.IntegerField(choices=[(-1, 'Preschool'), (0, 'Kindergarten'), (1, 'First Grade'), (2, 'Second Grade'), (3, 'Third Grade'), (4, 'Fourth Grade'), (5, 'Fifth Grade'), (6, 'Sixth Grade'), (7, 'Seventh Grade'), (8, 'Eighth Grade'), (9, 'Ninth Grade'), (10, 'Tenth Grade'), (11, 'Eleventh Grade'), (12, 'Twelfth Grade')]),
        ),
    ]
