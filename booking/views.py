from rest_framework import mixins, viewsets

from stadium.pagination import StandardResultsSetPagination
from .models import StadiumBooking
from .serializers import BookingSerializer

class BookingViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    
    pagination_class = StandardResultsSetPagination
    serializer_class = BookingSerializer

    def get_queryset(self):
        return StadiumBooking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
