from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  HotelViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
