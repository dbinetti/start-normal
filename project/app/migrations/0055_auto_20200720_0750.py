# Generated by Django 3.0.8 on 2020-07-20 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0054_auto_20200719_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='status',
            field=models.IntegerField(choices=[(0, 'New'), (10, 'Active'), (20, 'Closed'), (30, 'Merged')], default=0),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='notes',
            field=models.TextField(blank=True, default='', help_text='If you are a teacher please add some notes here...', max_length=512),
        ),
    ]
