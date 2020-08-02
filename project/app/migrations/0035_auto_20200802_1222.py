# Generated by Django 3.0.8 on 2020-08-02 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_auto_20200802_0800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invite',
            name='email',
        ),
        migrations.AddField(
            model_name='invite',
            name='parent_email',
            field=models.EmailField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='invite',
            name='parent_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='invite',
            name='student_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.DeleteModel(
            name='Classmate',
        ),
    ]
