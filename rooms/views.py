from django.utils.dateparse import parse_date
from rest_framework import viewsets, status,pagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rooms.models import Room
from bookings.models import Booking
from .serializers import RoomSerializer


class Roompagination(pagination.PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 10000

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    pagination_class=Roompagination

    @action(detail=False, methods=['post'])
    def check_availability(self, request):
        check_in_date_str = request.data.get('check_in_date')
        check_out_date_str = request.data.get('check_out_date')

        # Check if check_in_date and check_out_date are present
        if not check_in_date_str or not check_out_date_str:
            return Response({"error": "Check-in and check-out dates are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Try to parse the dates
        try:
            check_in_date = parse_date(check_in_date_str)
            check_out_date = parse_date(check_out_date_str)

            if not check_in_date or not check_out_date:
                raise ValueError("Invalid date format")
        except (ValueError, TypeError):
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # Get rooms that have bookings which overlap with the selected date range
        booked_rooms = Booking.objects.filter(
            status='Confirmed',
            check_in_date__lt=check_out_date,
            check_out_date__gt=check_in_date
        ).values_list('room_id', flat=True)

        # Exclude booked rooms and return available rooms
        available_rooms = Room.objects.exclude(id__in=booked_rooms).filter(is_available=True)
        serializer = self.get_serializer(available_rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
