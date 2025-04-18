# Generated by Django 5.2 on 2025-04-10 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('aircraft_code', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('model', models.JSONField()),
                ('range', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Aircraft',
                'verbose_name_plural': 'Aircrafts',
                'db_table': 'aircrafts_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('airport_code', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('airport_name', models.JSONField()),
                ('city', models.JSONField()),
                ('coordinates', models.CharField(max_length=100)),
                ('timezone', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Airport',
                'verbose_name_plural': 'Airports',
                'db_table': 'airports_data',
                'managed': False,
            },
        ),
    ]
