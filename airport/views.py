import ast
import logging

from drf_yasg.codecs import logger
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import connection

from .utils import haversine

logger = logging.getLogger(__name__)

from .models import Airport
from .serializers import AirportStatisticsSerializer, AirportDateStatisticsSerializer, AirportToDateStatisticsSerializer


# class AirportAllStatisticsViewSet(viewsets.GenericViewSet):
#     @action(detail=False, methods=["get"], url_path="airport-statistics")
#     def airport_statistics(self, request, *args, **kwargs):
#         from_date = request.query_params.get('from_date')
#         to_date = request.query_params.get('to_date')
#         order_by = request.query_params.get('order_by', 'flights_count')
#
#         try:
#             with connection.cursor() as cursor:
#                 query = """
#                     SELECT
#                     aa.airport_code AS airport_code,
#                     aa.airport_name->>'en' AS arrival_airport_name,
#                     COUNT(f.flight_id) AS flights_count,
#                     COUNT(DISTINCT tf.ticket_id) AS passengers_count,
#                     TO_CHAR(INTERVAL '1 second' * ROUND(AVG(EXTRACT(EPOCH FROM (f.scheduled_arrival - f.scheduled_departure)) / 60), 0),
#                     'HH24:MI:SS') AS flight_time
#                     FROM flights f
#                     JOIN airports_data aa ON f.arrival_airport_id = aa.airport_code
#                     LEFT JOIN ticket_flights tf ON f.flight_id = tf.flight_id
#                 """
#
#                 # Add filters for date range
#                 params = []
#                 if from_date:
#                     query += " WHERE f.scheduled_departure >= %s"
#                     params.append(from_date)
#                 if to_date:
#                     if from_date:
#                         query += " AND f.scheduled_departure <= %s"
#                     else:
#                         query += " WHERE f.scheduled_departure <= %s"
#                     params.append(to_date)
#
#                 query += " GROUP BY aa.airport_code, aa.airport_name"
#
#                 # Add ordering
#                 valid_order_fields = ['flights_count', 'passengers_count', 'flight_time']
#                 if order_by in valid_order_fields:
#                     query += f" ORDER BY {order_by}"
#
#                 cursor.execute(query, params)
#
#                 columns = [col[0] for col in cursor.description]
#                 results = [
#                     dict(zip(columns, row))
#                     for row in cursor.fetchall()
#                 ]
#
#                 return Response(results, status=status.HTTP_200_OK)
#
#         except Exception as e:
#             logger.error(f"Airport statistics error: {str(e)}")
#             return Response(
#                 {'message': "Statistika olishda xatolik yuz berdi"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

class AirportStatisticsViewSet(viewsets.GenericViewSet):
    queryset = []
    serializer_class = AirportStatisticsSerializer

    @swagger_auto_schema(query_serializer=AirportStatisticsSerializer)
    @action(detail=False, methods=["get"], url_path="airport-statistics")
    def airport_statistics(self, request, *args, **kwargs):
        serializer = AirportStatisticsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        airport_code = data['airport_code']
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        order_by = data.get('order_by')

        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT
                    aa.airport_code AS arrival_code,
                    aa.airport_name->>'en' AS arrival_airport_name,
                    COUNT(DISTINCT f.flight_id) AS flights_count,
                    COUNT(bp.boarding_no) AS passengers_count,
                    TO_CHAR(
                        INTERVAL '1 second' * ROUND(AVG(EXTRACT(EPOCH FROM (f.scheduled_arrival - f.scheduled_departure)) / 60), 0),
                        'HH24:MI:SS'
                    ) AS flight_time
                FROM flights f
                LEFT JOIN airports_data da ON f.departure_airport_id = da.airport_code
                LEFT JOIN airports_data aa ON f.arrival_airport_id = aa.airport_code
                LEFT JOIN boarding_passes bp ON f.flight_id = bp.flight_id
                WHERE f.departure_airport_id = %s
                """

                params = [airport_code]

                if from_date:
                    query += " AND f.scheduled_departure >= %s"
                    params.append(from_date)
                if to_date:
                    query += " AND f.scheduled_departure <= %s"
                    params.append(to_date)

                query += " GROUP BY aa.airport_code, aa.airport_name"

                valid_order_fields = ['flights_count', 'passengers_count', 'flight_time']
                if order_by in valid_order_fields:
                    query += f" ORDER BY {order_by}"

                cursor.execute(query, params)

                columns = [col[0] for col in cursor.description]
                results = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]

                departure_airport = Airport.objects.filter(airport_code=airport_code).first()

                if departure_airport and departure_airport.coordinates:
                    try:
                        dep_lon, dep_lat = ast.literal_eval(departure_airport.coordinates)
                        dep_name = departure_airport.airport_name.get('en', '')
                    except Exception as e:
                        logger.error(f"Departure airport coordinates parsing error: {str(e)}")
                        return Response({'message': "Manba aeroport koordinatalarini o‘qishda xatolik"}, status=400)

                    for result in results:
                        result['departure_airport'] = dep_name
                        arrival_code = result.get('arrival_code')
                        arrival_airport = Airport.objects.filter(airport_code=arrival_code).first()
                        if arrival_airport and arrival_airport.coordinates:
                            try:
                                arr_lon, arr_lat = ast.literal_eval(arrival_airport.coordinates)
                                distance = haversine(dep_lat, dep_lon, arr_lat, arr_lon)
                                result['distance_km'] = round(distance, 2)
                            except Exception as e:
                                logger.warning(f"Arrival airport coordinates parsing error: {str(e)}")

                        if 'arrival_code' in result:
                            del result['arrival_code']

                return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Airport statistics error: {str(e)}")
            return Response(
                {'message': "Statistika olishda xatolik yuz berdi"},
                status=status.HTTP_400_BAD_REQUEST
            )


class AirportDateStatisticsViewSet(viewsets.GenericViewSet):
    queryset = []
    serializer_class = AirportDateStatisticsSerializer

    @swagger_auto_schema(query_serializer=AirportDateStatisticsSerializer)
    @action(detail=False, methods=["get"], url_path="airport-statistics")
    def airport_statistics(self, request, *args, **kwargs):
        serializer = AirportDateStatisticsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        from_date = data['from_date']

        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT
                        da.airport_name->>'en' AS departure_airport_name,
                        aa.airport_name->>'en' AS arrival_airport_name,
                        COUNT(f.flight_id) AS flights_count,
                        COUNT(DISTINCT tf.ticket_id) AS passengers_count,
                        TO_CHAR(INTERVAL '1 second' * ROUND(AVG(EXTRACT(EPOCH FROM (f.scheduled_arrival - f.scheduled_departure)) / 60), 0),
                        'HH24:MI:SS') AS flight_time
                    FROM flights f
                    JOIN airports_data da ON f.departure_airport_id = da.airport_code
                    JOIN airports_data aa ON f.arrival_airport_id = aa.airport_code
                    LEFT JOIN ticket_flights tf ON f.flight_id = tf.flight_id
                    WHERE f.scheduled_departure >= %s
                    GROUP BY aa.airport_code, aa.airport_name, da.airport_code, da.airport_name
                """

                params = [from_date]

                cursor.execute(query, params)

                results = [
                    {col[0]: row[i] for i, col in enumerate(cursor.description)}
                    for row in cursor.fetchall()
                ]

                return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Airport statistics error: {str(e)}")
            return Response(
                {'message': "Statistika olishda xatolik yuz berdi"},
                status=status.HTTP_400_BAD_REQUEST
            )


class AirportToDateStatisticsViewSet(viewsets.GenericViewSet):
    queryset = []
    serializer_class = AirportToDateStatisticsSerializer

    @swagger_auto_schema(query_serializer=AirportToDateStatisticsSerializer)
    @action(detail=False, methods=["get"], url_path="airport-statistics")
    def airport_statistics(self, request, *args, **kwargs):
        serializer = AirportToDateStatisticsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        to_date = data['to_date']

        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT
                        da.airport_name->>'en' AS departure_airport_name,
                        aa.airport_name->>'en' AS arrival_airport_name,
                        COUNT(f.flight_id) AS flights_count,
                        COUNT(DISTINCT tf.ticket_id) AS passengers_count,
                        TO_CHAR(INTERVAL '1 second' * ROUND(AVG(EXTRACT(EPOCH FROM (f.scheduled_arrival - f.scheduled_departure)) / 60), 0),
                        'HH24:MI:SS') AS flight_time
                    FROM flights f
                    JOIN airports_data da ON f.departure_airport_id = da.airport_code
                    JOIN airports_data aa ON f.arrival_airport_id = aa.airport_code
                    LEFT JOIN ticket_flights tf ON f.flight_id = tf.flight_id
                    WHERE f.scheduled_departure <= %s
                    GROUP BY aa.airport_code, aa.airport_name, da.airport_code, da.airport_name
                """

                params = [to_date]

                cursor.execute(query, params)

                results = [
                    {col[0]: row[i] for i, col in enumerate(cursor.description)}
                    for row in cursor.fetchall()
                ]

                return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Airport statistics error: {str(e)}")
            return Response(
                {'message': "Statistika olishda xatolik yuz berdi"},
                status=status.HTTP_400_BAD_REQUEST
            )

# class AirportLangStatisticsViewSet(viewsets.GenericViewSet):
#     queryset = []
#     serializer_class = AirportStatisticsSerializer
#
#     @swagger_auto_schema(query_serializer=AirportStatisticsSerializer)
#     @action(detail=False, methods=["get"], url_path="airport-statistics")
#     def airport_statistics(self, request, *args, **kwargs):
#         serializer = AirportStatisticsSerializer(data=request.query_params)
#         serializer.is_valid(raise_exception=True)
#         data = serializer.validated_data
#
#         airport_code = data['airport_code']
#         from_date = data.get('from_date')
#         to_date = data.get('to_date')
#         order_by = data.get('order_by')
#
#         try:
#             with connection.cursor() as cursor:
#                 query = """
#                     SELECT
#                         aa.airport_code AS arrival_code,
#                         aa.airport_name->>'en' AS arrival_airport_name,
#                         COUNT(f.flight_id) AS flights_count,
#                         COUNT(DISTINCT tf.ticket_id) AS passengers_count,
#                         TO_CHAR(INTERVAL '1 second' * ROUND(AVG(EXTRACT(EPOCH FROM (f.scheduled_arrival - f.scheduled_departure))), 0),
#                         'HH24:MI:SS') AS flight_time
#                     FROM flights f
#                     JOIN airports_data da ON f.departure_airport_id = da.airport_code
#                     JOIN airports_data aa ON f.arrival_airport_id = aa.airport_code
#                     LEFT JOIN ticket_flights tf ON f.flight_id = tf.flight_id
#                     WHERE f.departure_airport_id = %s
#                 """
#
#                 params = [airport_code]
#
#                 if from_date:
#                     query += " AND f.scheduled_departure >= %s"
#                     params.append(from_date)
#                 if to_date:
#                     query += " AND f.scheduled_departure <= %s"
#                     params.append(to_date)
#
#                 query += " GROUP BY aa.airport_code, aa.airport_name"
#
#                 valid_order_fields = ['flights_count', 'passengers_count', 'flight_time']
#                 sql_order_by = order_by if order_by in valid_order_fields else None
#                 if sql_order_by:
#                     query += f" ORDER BY {sql_order_by}"
#
#                 cursor.execute(query, params)
#                 columns = [col[0] for col in cursor.description]
#                 results = [dict(zip(columns, row)) for row in cursor.fetchall()]
#
#                 departure_airport = Airport.objects.filter(airport_code=airport_code).first()
#
#                 if departure_airport and departure_airport.coordinates:
#                     try:
#                         dep_lon, dep_lat = ast.literal_eval(departure_airport.coordinates)
#                         dep_name = departure_airport.airport_name.get('en', '')
#                     except Exception as e:
#                         logger.error(f"Departure airport coordinates parsing error: {str(e)}")
#                         return Response({'message': "Manba aeroport koordinatalarini o‘qishda xatolik"}, status=400)
#
#                     for result in results:
#                         result['departure_airport'] = dep_name
#                         arrival_code = result.get('arrival_code')
#                         arrival_airport = Airport.objects.filter(airport_code=arrival_code).first()
#                         if arrival_airport and arrival_airport.coordinates:
#                             try:
#                                 arr_lon, arr_lat = ast.literal_eval(arrival_airport.coordinates)
#                                 distance = haversine(dep_lat, dep_lon, arr_lat, arr_lon)
#                                 result['distance_km'] = round(distance, 2)
#                             except Exception as e:
#                                 logger.warning(f"Arrival airport coordinates parsing error: {str(e)}")
#
#                 return Response(results, status=status.HTTP_200_OK)
#
#         except Exception as e:
#             logger.error(f"Airport statistics error: {str(e)}")
#             return Response(
#                 {'message': "Statistika olishda xatolik yuz berdi"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
