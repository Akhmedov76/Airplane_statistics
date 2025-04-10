from django.db import models
from django.forms import JSONField

from flight.models import Flight


class Ticket(models.Model):
    ticket_no = models.CharField(primary_key=True, max_length=13)
    book_ref = models.ForeignKey('booking.Booking', on_delete=models.CASCADE)
    passenger_id = models.CharField(max_length=20)
    passenger_name = models.TextField()
    contact_data = models.JSONField()

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        db_table = 'tickets'
        managed = False


class TicketFlight(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='flights')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')
    fare_conditions = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Ticket flight"
        verbose_name_plural = "Ticket flights"
        db_table = 'ticket_flights'
        managed = False
