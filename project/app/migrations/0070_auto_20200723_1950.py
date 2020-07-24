# Generated by Django 3.0.8 on 2020-07-24 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0069_account_is_welcomed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='notes',
            field=models.TextField(blank=True, default='', help_text='Please add any other notes you think we should know.', max_length=2000),
        ),
    ]
