from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('airport.urls')),
    path('api/', include('booking.urls')),
    path('api/', include('flight.urls')),
    path('api/', include('ticket.urls')),
]

# Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="This is a sample server.  You can find out more about Swagger at "
                    "[http://swagger.io](http://swagger.io) or on [irc.freenode.net, #swagger](http://swagger.io/irc/). "
                    "For this sample, you can use the api key `special-key` to test the authorization filters.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="#", url="#",
                                name="#"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
