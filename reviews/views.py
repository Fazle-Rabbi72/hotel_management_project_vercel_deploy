from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Review
from .serializers import ReviewSerializer
from rest_framework.authentication import TokenAuthentication

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [TokenAuthentication]
    def get_queryset(self):
        queryset = super().get_queryset()
        room_id= self.request.query_params.get('room_id', None)
        if room_id is not None:
            queryset = queryset.filter(room_id=room_id)
        return queryset