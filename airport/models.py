from django.db import models


class Airport(models.Model):
    airport_code = models.CharField(max_length=3, primary_key=True)
    airport_name = models.JSONField()
    city = models.JSONField()
    coordinates = models.CharField(max_length=100)
    timezone = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.airport_code} - {self.airport_name.get('en', '')}"

    class Meta:
        verbose_name = 'Airport'
        verbose_name_plural = 'Airports'
        db_table = 'airports_data'
        managed = False


class Aircraft(models.Model):
    aircraft_code = models.CharField(primary_key=True, max_length=3)
    model = models.JSONField()
    range = models.IntegerField()

    def __str__(self):
        return f"{self.aircraft_code} - {self.model.get('en', 'No Model Name')}"

    class Meta:
        verbose_name = 'Aircraft'
        verbose_name_plural = 'Aircrafts'
        db_table = 'aircrafts_data'
        managed = False
