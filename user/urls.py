from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserRegistrationView,UserLoginApiView,active,LogoutAPIview,DepositView

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)

# Make sure to register the custom URL before the router
urlpatterns = [
    path('', include(router.urls)),  # Include router after
    path('register/', UserRegistrationView.as_view(), name='register'),  # Register URL first
    path('login/',UserLoginApiView.as_view(), name='login'),
    path('logout/',LogoutAPIview.as_view(), name='logout'),
    path('register/active/<uidb64>/<token>/',active,name='activet'),
    path('deposit/',DepositView.as_view(), name='deposit'),
]
