# Generated by Django 3.1 on 2020-08-12 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0067_auto_20200812_0157'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='rate',
            field=models.CharField(blank=True, default='', help_text='What is your hourly rate range?', max_length=512),
        ),
    ]
