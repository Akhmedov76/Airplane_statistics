from rest_framework import serializers
from .models import Flight

class FlightSerializer(serializers.ModelSerializer):
    distance_km = serializers.FloatField(read_only=True)
    flight_time = serializers.DurationField(read_only=True)

    class Meta:
        model = Flight
        fields = ['flight_id', 'flight_no', 'scheduled_departure', 'scheduled_arrival',
                  'departure_airport', 'arrival_airport', 'status', 'aircraft', 'actual_departure',
                  'actual_arrival', 'distance_km', 'flight_time']


class FlightStatisticsSerializer(serializers.ModelSerializer):
    distance_km = serializers.ReadOnlyField()
    flight_time = serializers.ReadOnlyField()

    class Meta:
        model = Flight
        fields = (
        'flight_no', 'scheduled_departure', 'scheduled_arrival', 'arrival_airport', 'distance_km', 'flight_time',
        'passengers_count')