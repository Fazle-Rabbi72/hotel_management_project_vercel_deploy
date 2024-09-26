from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  RoomViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    ]