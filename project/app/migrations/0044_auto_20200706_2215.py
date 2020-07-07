# Generated by Django 3.0.8 on 2020-07-07 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='kind',
            field=models.IntegerField(blank=True, choices=[('District', [(400, 'County Office of Education'), (402, 'State Board of Education'), (403, 'Statewide Benefit Charter'), (431, 'State Special Schools'), (434, 'Non-school Location*'), (442, 'Joint Powers Authority (JPA)'), (452, 'Elementary School District'), (454, 'Unified School District'), (456, 'High School District'), (458, 'Community College District'), (498, 'Regional Occupational Center/Program (ROC/P)'), (499, 'Administration Only')]), ('School', [(510, 'Preschool'), (520, 'Elementary'), (530, 'Intermediate/Middle/Junior High'), (540, 'High School'), (550, 'Elementary-High Combination'), (560, 'Adult'), (570, 'Ungraded')])], null=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='address',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='department',
            name='city',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='department',
            name='nces_id',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='state',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='department',
            name='zipcode',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
