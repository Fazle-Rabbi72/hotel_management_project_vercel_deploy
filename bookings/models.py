from django.db import models
from user.models import User
from rooms.models import Room

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    guest_number = models.PositiveIntegerField(default=None)  # New field for number of guests
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking by {self.user.username} for {self.room.hotel.name}'

    def save(self, *args, **kwargs):
        # Calculate total price based on the number of nights and room price
        num_nights = (self.check_out_date - self.check_in_date).days
        self.total_price = self.room.price_per_night * num_nights
        super().save(*args, **kwargs)

    @staticmethod
    def is_room_available(room, check_in_date, check_out_date):
        existing_bookings = Booking.objects.filter(
            room=room,
            status='Confirmed',
            check_in_date__lt=check_out_date,
            check_out_date__gt=check_in_date,
        )
        return not existing_bookings.exists()
