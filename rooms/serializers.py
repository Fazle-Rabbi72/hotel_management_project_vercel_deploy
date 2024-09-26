from rest_framework import serializers
from .models import Room
from hotel.models import Hotel
from hotel.serializers import HotelSerializer

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'hotel','descirption', 'room_type', 'price_per_night', 'image']

    def create(self, validated_data):
        hotel = validated_data.pop('hotel')  # Get the hotel instance from the validated data
        room = Room.objects.create(hotel=hotel, **validated_data)
        return room

