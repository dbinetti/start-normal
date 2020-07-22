# Generated by Django 3.0.8 on 2020-07-22 15:07

import app.models
import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0057_auto_20200721_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, max_length=255, populate_from=app.models.get_populate_from, unique=True)),
                ('status', models.IntegerField(choices=[(0, 'New'), (10, 'Active')], default=0)),
                ('grade', models.IntegerField(choices=[(2, 'Transitional Kindergarten'), (5, 'Kindergarten'), (10, 'First  Grade'), (20, 'Second  Grade'), (30, 'Third  Grade'), (40, 'Fourth  Grade'), (50, 'Fifth  Grade'), (60, 'Sixth  Grade'), (70, 'Seventh Grade'), (80, 'Eighth Grade'), (90, 'Ninth Grade'), (100, 'Tenth Grade'), (110, 'Eleventh Grade'), (120, 'Twelfth Grade'), (130, 'Freshman'), (140, 'Sophomore')])),
                ('lat', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('lon', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cohorts', to='app.Parent')),
            ],
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, max_length=255, populate_from=app.models.get_populate_from, unique=True)),
                ('status', models.IntegerField(choices=[(0, 'New'), (10, 'Active')], default=0)),
                ('subject', models.IntegerField(choices=[(110, 'English'), (120, 'History'), (130, 'Mathematics'), (140, 'Science'), (150, 'Art'), (160, 'Music'), (170, 'PE'), (180, 'Other')], null=True)),
                ('venue', models.CharField(blank=True, default='', max_length=255)),
                ('address', models.CharField(blank=True, default='', max_length=255)),
                ('city', models.CharField(default='', max_length=255)),
                ('state', models.CharField(default='', max_length=255)),
                ('zipcode', models.CharField(blank=True, default='', max_length=255)),
                ('county', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(blank=True, default='', max_length=255)),
                ('lat', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('lon', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('cohort', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classrooms', to='app.Cohort')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classrooms', to='app.Teacher')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='cohort',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='app.Cohort'),
        ),
    ]
