from django.db import models
from hotel.models import Hotel
# Create your models here.
class Room(models.Model):
    ROOM_TYPES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Family Suite','Family Suite'),
        ('Suite', 'Suite'),
    ]
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms') 
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES)
    descirption=models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=255, blank=True, null=True)
    is_available = models.BooleanField(default=True)  

    def __str__(self):
        return f'{self.hotel.name} - {self.room_type}'