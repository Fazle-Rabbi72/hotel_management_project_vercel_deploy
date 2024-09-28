from decimal import Decimal
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer
from rooms.models import Room
from datetime import datetime
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from django.db import transaction

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication]
    

    def create(self, request, *args, **kwargs):
        user = request.user
        
        # Validate room existence check kora hocce
        try:
            room = Room.objects.get(id=request.data['room'])
        except Room.DoesNotExist:
            return Response({"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND)

        # convert  to Decimal price
        room_price_per_night = Decimal(room.price_per_night)

        # check-in and check-out dates
        check_in_date_str = request.data['check_in_date']
        check_out_date_str = request.data['check_out_date']
        check_in_date = datetime.strptime(check_in_date_str, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out_date_str, '%Y-%m-%d')

        # Validate check-in and check-out dates
        if check_out_date <= check_in_date:
            return Response({"error": "Check-out date must be after check-in date."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for existing bookings
        existing_booking = Booking.objects.filter(
            Q(check_in_date__lt=check_out_date) & Q(check_out_date__gt=check_in_date),
            room=room,
            status='Confirmed',
        )

        if existing_booking.exists():
            return Response({"error": "This room is already booked for the selected dates."}, status=status.HTTP_400_BAD_REQUEST)

        # total price calculate kora hocce!!
        num_nights = (check_out_date - check_in_date).days
        if num_nights <= 0:
            return Response({"error": "Invalid booking duration."}, status=status.HTTP_400_BAD_REQUEST)

        total_price = room_price_per_night * Decimal(num_nights)

        # for user valance check
        user_balance = Decimal(user.balance)
        if user_balance < total_price:
            return Response({"error": "Insufficient balance to make this booking."}, status=status.HTTP_400_BAD_REQUEST)

        # transection and boooking create kora hocce
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data) #valid data ki na check korbe
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user.save()

        return Response({"message": "Booking created successfully!", "booking": serializer.data}, status=status.HTTP_201_CREATED)
   
   
    def get_queryset(self):
        queryset = super().get_queryset()
        user_id= self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset