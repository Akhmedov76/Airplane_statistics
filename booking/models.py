from django.db import models


class Booking(models.Model):
    book_ref = models.CharField(primary_key=True, max_length=6)
    book_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        db_table = 'bookings'
        managed = False


class Seats(models.Model):
    aircraft_code = models.ForeignKey(
        'airport.Aircraft',
        # to_field='aircraft_code',
        on_delete=models.CASCADE,
    )
    seat_no = models.CharField(max_length=4)
    fare_conditions = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Seat'
        verbose_name_plural = 'Seats'
        db_table = 'seats'
        managed = False
