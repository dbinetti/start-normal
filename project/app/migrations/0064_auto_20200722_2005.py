# Generated by Django 3.0.8 on 2020-07-23 03:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0063_invitation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('grade', models.IntegerField(choices=[(2, 'Transitional Kindergarten'), (5, 'Kindergarten'), (10, 'First  Grade'), (20, 'Second  Grade'), (30, 'Third  Grade'), (40, 'Fourth  Grade'), (50, 'Fifth  Grade'), (60, 'Sixth  Grade'), (70, 'Seventh Grade'), (80, 'Eighth Grade'), (90, 'Ninth Grade'), (100, 'Tenth Grade'), (110, 'Eleventh Grade'), (120, 'Twelfth Grade'), (130, 'Freshman'), (140, 'Sophomore')])),
                ('status', models.IntegerField(choices=[(0, 'New'), (10, 'Sent'), (20, 'Accepted')], default=0)),
                ('parent_name', models.CharField(max_length=255)),
                ('parent_email', models.EmailField(max_length=254)),
                ('student_name', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, default='', max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('cohort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invites', to='app.Cohort')),
                ('inviter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Invitation',
        ),
    ]
