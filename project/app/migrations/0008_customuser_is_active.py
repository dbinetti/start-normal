# Generated by Django 3.0.7 on 2020-06-14 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20200613_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
