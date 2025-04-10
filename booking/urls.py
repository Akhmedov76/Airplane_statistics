from django.urls import path
from .views import BookingView, SeatsView

urlpatterns = [
    path('bookings/', BookingView.as_view(), name='booking-list'),
    path('bookings/<str:book_ref>/', BookingView.as_view(), name='booking-detail'),
    path('seats/', SeatsView.as_view(), name='seats-list-create'),
    path('seats/<int:seat_id>/', SeatsView.as_view(), name='seats-detail'),
]
