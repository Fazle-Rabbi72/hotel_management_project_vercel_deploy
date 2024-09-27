from django.db import models
from user.models import User
from rooms.models import Room

STER_CHOICE = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  
    rating = models.CharField(choices=STER_CHOICE, max_length=100)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Review by {self.user.username} for {self.room.hotel.name}'  # Change 'hotel.name' to 'room.hotel.name'
