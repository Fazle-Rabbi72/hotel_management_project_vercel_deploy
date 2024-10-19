
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.response import Response


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),           
    path('', include('hotel.urls')),          
    path('', include('rooms.urls')),           
    path('', include('bookings.urls')),      
    path('', include('reviews.urls')),        
    path('', include('contact_us.urls')),
    path('api/auth/',include('rest_framework.urls')),        
 
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

