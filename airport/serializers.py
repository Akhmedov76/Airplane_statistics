from rest_framework import serializers


class AirportStatisticsSerializer(serializers.Serializer):
    airport_code = serializers.CharField(required=True)
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)
    order_by = serializers.ChoiceField(
        choices=['flights_count', 'passengers_count', 'flight_time'],
        required=False,
        default='flight_time'
    )

class AirportDateStatisticsSerializer(serializers.Serializer):
    from_date = serializers.DateField(required=True)

class AirportToDateStatisticsSerializer(serializers.Serializer):
    to_date = serializers.DateField(required=True)