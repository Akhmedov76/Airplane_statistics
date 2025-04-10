from django.db.models import F, Avg, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from airport.models import Airport
from ticket.models import Ticket
from .models import Flight
from .serializers import FlightSerializer, FlightStatisticsSerializer


class FlightView(APIView):

    def get(self, request):
        flights = Flight.objects.all()
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FlightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Flight
from datetime import timedelta


class FlightStatisticsView(APIView):
    """
    Tanlangan aeroport uchun statistikani olish:
    - Qaysi aeroportga qo'nishi (arrival_airport)
    - Masofa (distance_km)
    - Passajirlar soni (passengers_count)
    - O'rtacha vaqt (flight_time)
    """

    def get(self, request, airport_code):
        flights = Flight.objects.filter(
            arrival_airport__airport_code=airport_code
        )

        total_flights = flights.count()
        total_passengers = 0
        total_flight_time = timedelta()

        for flight in flights:
            total_passengers += flight.flight_id.count()
            if flight.flight_time:  # Flight time mavjud bo'lsa
                total_flight_time += flight.flight_time

        if total_flights > 0:
            average_flight_time = total_flight_time.total_seconds() / total_flights / 60
        else:
            average_flight_time = 0

        statistics = {
            "airport_code": airport_code,
            "total_flights": total_flights,
            "total_passengers": total_passengers,
            "average_flight_time": round(average_flight_time, 2),
        }

        return Response(statistics, status=status.HTTP_200_OK)


class FlightStatistics(APIView):
    def get(self, request, airport_code, from_date=None, to_date=None):
        try:
            # Tanlangan airport
            airport = Airport.objects.get(airport_code=airport_code)

            # Filter: sana oralig'i bo'yicha
            flights_query = Flight.objects.filter(
                arrival_airport=airport,
            )

            if from_date:
                flights_query = flights_query.filter(scheduled_departure__gte=from_date)
            if to_date:
                flights_query = flights_query.filter(scheduled_departure__lte=to_date)

            # Statistikalar
            flight_count = flights_query.count()  # Parvozlar soni
            average_flight_time = flights_query.aggregate(Avg('flight_time'))[
                'flight_time__avg']  # O'rtacha parvoz vaqti
            total_distance = sum([flight.distance_km for flight in flights_query])  # Masofa hisoblash
            passengers_count = Ticket.objects.filter(flight__in=flights_query).count()  # Passajirlar soni

            # Eng yaqin aeroportlar
            nearest_airports = Airport.objects.all().exclude(airport_code=airport_code).order_by('airport_code')[:5]

            # Natijani qaytarish
            return Response({
                'airport': airport.airport_name.get('en', ''),
                'flight_count': flight_count,
                'average_flight_time': average_flight_time,
                'total_distance': total_distance,
                'passengers_count': passengers_count,
                'nearest_airports': [airport.airport_name.get('en', '') for airport in nearest_airports],
            }, status=status.HTTP_200_OK)

        except Airport.DoesNotExist:
            return Response({"detail": "Airport not found."}, status=status.HTTP_404_NOT_FOUND)


class FlightStatisticsAPIView(APIView):
    def get(self, request, airport_code, from_date=None, to_date=None):
        try:
            airport = Airport.objects.get(airport_code=airport_code)

            # Sana oralig'i bo'yicha filtr
            filters = {}
            if from_date:
                filters['scheduled_departure__gte'] = from_date
            if to_date:
                filters['scheduled_departure__lte'] = to_date

            # Parvozlar statistikasi olish
            flights = Flight.objects.filter(arrival_airport=airport, **filters)

            # Agar kerak bo'lsa, masofa va o'rtacha vaqtni hisoblash
            flight_stats = flights.annotate(
                avg_flight_time=Avg('flight_time'),
                total_passengers=Count('passengers_count'),
                avg_distance=Avg('distance_km')
            )

            # Statistika ma'lumotlarini serializer orqali yuboramiz
            serializer = FlightStatisticsSerializer(flight_stats, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Airport.DoesNotExist:
            return Response({"detail": "Airport not found."}, status=status.HTTP_404_NOT_FOUND)


class FlightByAirportView(APIView):
    """
    Tanlangan aeroportga tegishli parvozlarni olish.
    """

    def get(self, request, airport_code):
        flights = Flight.objects.filter(
            departure_airport__airport_code=airport_code
        )
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
