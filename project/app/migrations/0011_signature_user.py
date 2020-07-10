# Generated by Django 3.0.8 on 2020-07-10 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20200710_0543'),
    ]

    operations = [
        migrations.AddField(
            model_name='signature',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='signatures', to=settings.AUTH_USER_MODEL),
        ),
    ]
