# Generated by Django 3.0.8 on 2020-07-18 18:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_delete_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=False)),
                ('kind', models.IntegerField(blank=True, choices=[(510, 'Preschool'), (520, 'Elementary'), (530, 'Intermediate/Middle/Junior High'), (540, 'High School'), (550, 'Elementary-High Combination'), (560, 'Adult'), (570, 'Ungraded')], null=True)),
                ('message', models.TextField(blank=True, default='', help_text='Feel free to include private notes just for us.', max_length=1024)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
