from math import radians, sin, cos, sqrt, atan2

from django.db import models

from airport.models import Airport


class Flight(models.Model):
    flight_id = models.AutoField(primary_key=True)
    flight_no = models.CharField(max_length=10)
    scheduled_departure = models.DateTimeField()
    scheduled_arrival = models.DateTimeField()
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    status = models.CharField(max_length=20)
    aircraft = models.ForeignKey('airport.Aircraft', to_field='aircraft_code',
                                 db_column='aircraft_code', on_delete=models.CASCADE)
    actual_departure = models.DateTimeField(null=True, blank=True)
    actual_arrival = models.DateTimeField(null=True, blank=True)



    def __str__(self):
        return f"{self.flight_no} - {self.departure_airport} to {self.arrival_airport}"

    class Meta:
        verbose_name = 'Flight'
        verbose_name_plural = 'Flights'
        db_table = 'flights'
