from django.contrib import admin
from .models import Flight

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_no', 'departure_airport', 'arrival_airport', 'status', 'scheduled_departure', 'scheduled_arrival')
    search_fields = ('flight_no',)
    list_filter = ('departure_airport', 'arrival_airport', 'status')
