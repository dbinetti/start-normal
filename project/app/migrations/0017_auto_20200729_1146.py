# Generated by Django 3.0.8 on 2020-07-29 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20200729_0802'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homeroom',
            old_name='description',
            new_name='notes',
        ),
        migrations.RemoveField(
            model_name='homeroom',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='homeroom',
            name='max_size',
        ),
        migrations.RemoveField(
            model_name='homeroom',
            name='name',
        ),
        migrations.RemoveField(
            model_name='homeroom',
            name='school',
        ),
        migrations.RemoveField(
            model_name='homeroom',
            name='slug',
        ),
        migrations.AlterField(
            model_name='homeroom',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homerooms', to='app.Parent'),
        ),
    ]
