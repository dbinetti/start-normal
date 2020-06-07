# Generated by Django 3.0.7 on 2020-06-07 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20200606_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signature',
            name='location',
            field=models.CharField(choices=[('ATH', 'Atherton'), ('BEL', 'Belmont'), ('BRB', 'Brisbane'), ('BUR', 'Burlingame'), ('COL', 'Colma'), ('DC', 'Daly City'), ('EPA', 'East Palo Alto'), ('FC', 'Foster City'), ('HMB', 'Half Moon Bay'), ('HIL', 'Hillsborough'), ('MP', 'Menlo Park'), ('MIL', 'Millbrae'), ('PAC', 'Pacifica'), ('PV', 'Portola Valley'), ('RC', 'Redwood City'), ('SB', 'San Bruno'), ('SC', 'San Carlos'), ('SM', 'San Mateo'), ('SSF', 'South San Francisco'), ('WS', 'Woodside'), ('UN', 'Unincorporated San Mateo County'), ('OUT', 'Outside of San Mateo County')], max_length=255, null=True),
        ),
    ]
