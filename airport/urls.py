from django.urls import path, include
from rest_framework.routers import DefaultRouter

from airport.views import AirportStatisticsViewSet, AirportDateStatisticsViewSet, AirportToDateStatisticsViewSet

router = DefaultRouter()

router.register(r'get-airports-by-code', AirportStatisticsViewSet, basename='activities')
router.register(r'get-airports-by-from-date', AirportDateStatisticsViewSet, basename='from_dates')
router.register(r'get-airports-by-to-date', AirportToDateStatisticsViewSet, basename='to_dates')

urlpatterns = [
    path('airports/v1/', include(router.urls)),
]
