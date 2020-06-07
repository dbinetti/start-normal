# Generated by Django 3.0.7 on 2020-06-07 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20200606_1918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signature',
            name='preferences',
        ),
        migrations.AlterField(
            model_name='signature',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='signature',
            name='location',
            field=models.CharField(choices=[('ATH', 'Atherton'), ('BEL', 'Belmont'), ('BRB', 'Brisbane'), ('BUR', 'Burlingame'), ('COL', 'Colma'), ('DC', 'Daly City'), ('EPA', 'East Palo Alto'), ('FC', 'Foster City'), ('HMB', 'Half Moon Bay'), ('HIL', 'Hillsborough'), ('MP', 'Menlo Park'), ('MIL', 'Millbrae'), ('PAC', 'Pacifica'), ('PV', 'Portola Valley'), ('RC', 'Redwood City'), ('SB', 'San Bruno'), ('SC', 'San Carlos'), ('SSF', 'South San Francisco'), ('WS', 'Woodside'), ('UN', 'Unincorporated San Mateo County'), ('OUT', 'Outside of San Mateo County')], max_length=255, null=True),
        ),
    ]
