from django.contrib import admin
from .models import Booking, Seats


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('book_ref', 'book_date', 'total_amount')
    search_fields = ('book_ref',)
    list_filter = ('book_date',)


@admin.register(Seats)
class SeatsAdmin(admin.ModelAdmin):
    list_display = ('aircraft_code', 'seat_no', 'fare_conditions')
    search_fields = ('seat_no', 'aircraft_code__aircraft_code')
    list_filter = ('fare_conditions', 'aircraft_code')
