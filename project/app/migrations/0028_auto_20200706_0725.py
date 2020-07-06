# Generated by Django 3.0.8 on 2020-07-06 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_auto_20200706_0712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='soc',
            field=models.IntegerField(blank=True, choices=[(8, 'Preschool'), (9, 'Special Education Schools (Public)'), (10, 'County Community'), (11, 'Youth Authority Facilities (CEA)'), (13, 'Opportunity Schools'), (14, 'Juvenile Court Schools'), (15, 'Other County or District Programs'), (31, 'State Special Schools'), (60, 'Elementary School (Public)'), (61, 'Elementary School in 1 School District (Public)'), (62, 'Intermediate/Middle Schools (Public)'), (63, 'Alternative Schools of Choice'), (64, 'Junior High Schools (Public)'), (65, 'K-12 Schools (Public)'), (66, 'High Schools (Public)'), (67, 'High Schools in 1 School District (Public)'), (68, 'Continuation High Schools'), (69, 'District Community Day Schools'), (70, 'Adult Education Centers'), (98, 'Regional Occupational Center/Program (ROC/P)')], null=True),
        ),
    ]
