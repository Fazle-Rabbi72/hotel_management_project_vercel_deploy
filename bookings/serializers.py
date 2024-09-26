from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True) 
    class Meta:
        model = Booking
        fields = ['id', 'user', 'room','image','status', 'check_in_date', 'check_out_date', 'guest_number', 'total_price', 'status', 'created_at']
        

    def get_image(self, obj):
        # Return the full URL for the room's image
        request = self.context.get('request')  # Get the request object to construct full URL
        image_url = obj.room.image.url if obj.room.image else None
        if image_url and request:
            return request.build_absolute_uri(image_url)
        return None
    
    def validate(self, data):
        # Calculate the total price based on the number of nights before validation
        room = data['room']
        check_in_date = data['check_in_date']
        check_out_date = data['check_out_date']
        num_nights = (check_out_date - check_in_date).days
        total_price = room.price_per_night * num_nights

        # Check if the user has enough balance
        user = data['user']
        if user.balance < total_price:
            raise serializers.ValidationError("Insufficient balance to complete the booking.")

        return data

    def create(self, validated_data):
        # Automatically calculate the total price before saving
        room = validated_data['room']
        check_in_date = validated_data['check_in_date']
        check_out_date = validated_data['check_out_date']
        num_nights = (check_out_date - check_in_date).days
        total_price = room.price_per_night * num_nights

        # Assign total price to the booking object
        validated_data['total_price'] = total_price

        # Create the booking object
        booking = Booking.objects.create(**validated_data)

        return booking
    
