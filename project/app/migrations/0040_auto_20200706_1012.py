# Generated by Django 3.0.8 on 2020-07-06 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_auto_20200706_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='district',
            name='cd_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='district',
            name='city',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='district',
            name='county',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='district',
            name='doc',
            field=models.IntegerField(choices=[(0, 'County Office of Education'), (2, 'State Board of Education'), (3, 'Statewide Benefit Charter'), (31, 'State Special Schools'), (34, 'Non-school Location*'), (42, 'Joint Powers Authority (JPA)'), (52, 'Elementary School District'), (54, 'Unified School District'), (56, 'High School District'), (58, 'Community College District'), (98, 'Regional Occupational Center/Program (ROC/P)'), (99, 'Administration Only')]),
        ),
        migrations.AlterField(
            model_name='district',
            name='nces_district_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='district',
            name='state',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='district',
            name='status',
            field=models.IntegerField(choices=[(10, 'Active'), (20, 'Closed'), (30, 'Merged')], default=10),
        ),
        migrations.AlterField(
            model_name='district',
            name='zipcode',
            field=models.CharField(max_length=255),
        ),
    ]
