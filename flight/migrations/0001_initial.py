# Generated by Django 5.2 on 2025-04-10 06:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('airport', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('flight_id', models.AutoField(primary_key=True, serialize=False)),
                ('flight_no', models.CharField(max_length=10)),
                ('scheduled_departure', models.DateTimeField()),
                ('scheduled_arrival', models.DateTimeField()),
                ('status', models.CharField(max_length=20)),
                ('actual_departure', models.DateTimeField(blank=True, null=True)),
                ('actual_arrival', models.DateTimeField(blank=True, null=True)),
                ('aircraft', models.ForeignKey(db_column='aircraft_code', on_delete=django.db.models.deletion.CASCADE, to='airport.aircraft')),
                ('arrival_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrivals', to='airport.airport')),
                ('departure_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departures', to='airport.airport')),
            ],
            options={
                'verbose_name': 'Flight',
                'verbose_name_plural': 'Flights',
                'db_table': 'flights',
            },
        ),
    ]
