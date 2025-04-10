from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket, TicketFlight
from .serializers import TicketSerializer, TicketFlightSerializer


class TicketView(APIView):

    def get(self, request):
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketFlightView(APIView):

    def get(self, request):
        ticket_flights = TicketFlight.objects.all()
        serializer = TicketFlightSerializer(ticket_flights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TicketFlightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
