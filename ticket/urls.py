from django.urls import path

from ticket.views import TicketView, TicketFlightView

urlpatterns = [
    # Ticket API
    path('tickets/', TicketView.as_view(), name='ticket-list'),
    path('tickets/<str:ticket_no>/', TicketView.as_view(), name='ticket-detail'),
    path('ticket_flights/', TicketFlightView.as_view(), name='ticketflight-list'),
    path('ticket_flights/<int:id>/', TicketFlightView.as_view(), name='ticketflight-detail'),

]
