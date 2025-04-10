from django.contrib import admin
from .models import Airport, Aircraft

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('airport_code', 'airport_name', 'city', 'timezone')
    search_fields = ('airport_code', 'airport_name')

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('aircraft_code', 'model', 'range')
    search_fields = ('aircraft_code', 'model')
