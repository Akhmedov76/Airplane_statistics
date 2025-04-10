from django.contrib import admin
from .models import Ticket, TicketFlight

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_no', 'book_ref', 'passenger_id', 'passenger_name')
    search_fields = ('ticket_no', 'passenger_name')
    list_filter = ('book_ref',)

@admin.register(TicketFlight)
class TicketFlightAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'flight', 'fare_conditions', 'amount')
    search_fields = ('ticket__ticket_no', 'flight__flight_no')
