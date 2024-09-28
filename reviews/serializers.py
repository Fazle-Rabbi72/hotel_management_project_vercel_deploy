from rest_framework import serializers
from .models import Review
from bookings.models import Booking

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)  #for getting user name

    class Meta:
        model = Review
        fields = ['id', 'user_name', 'room', 'rating', 'comment', 'created_at']  

    def get_user_name(self, obj):
        # first name and last name Concatenate korteci
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        room = validated_data['room']

        # kono room bookig ace ki na seta check kora hocce
        if not Booking.objects.filter(user=user, room=room, status='Confirmed').exists():
            raise serializers.ValidationError("You can only leave a review after a confirmed booking.")

        review = Review.objects.create(
            room=room,
            user=user,
            rating=validated_data['rating'],
            comment=validated_data['comment'],
        )
        return review