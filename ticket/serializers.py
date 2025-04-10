from rest_framework import serializers
from .models import Ticket, TicketFlight


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['ticket_no', 'book_ref', 'passenger_id', 'passenger_name', 'contact_data']


class TicketFlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketFlight
        fields = ['ticket', 'flight', 'fare_conditions', 'amount']
