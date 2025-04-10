from django.urls import path
from .views import FlightView, FlightStatisticsView, FlightByAirportView, FlightStatistics, FlightStatisticsAPIView

urlpatterns = [
    # Parvozlar ro'yxatini olish va yangi parvoz yaratish
    path('flights/', FlightView.as_view(), name='flight-list'),
    path('flights/<int:flight_id>/', FlightView.as_view(), name='flight-detail'),

    path('flights/statistics/<str:airport_code>/', FlightStatistics.as_view(), name='flight-statistics'),
    path('flights/statistics/<str:airport_code>/filter/', FlightStatistics.as_view(), name='flight-statistics-filter'),
    path('flight-statistics/<str:airport_code>/', FlightStatisticsAPIView.as_view(), name='flight-statistics'),
    path('flight-statistics/<str:airport_code>/filter/', FlightStatisticsAPIView.as_view(),
         name='flight-statistics-filter'),
]
