from rest_framework import serializers
from .models import Booking, Seats


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['book_ref', 'book_date', 'total_amount']


class SeatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seats
        fields = ['id', 'aircraft_code', 'seat_no', 'fare_conditions']
