from rest_framework import viewsets, filters, status, permissions
from rest_framework.response import Response

from .models import Stadium, StadiumImages
from .serializers import StadiumSerializer
from .pagination import StandardResultsSetPagination
from .permissions import IsAdminOrOwner, IsAdminOrStadiumOwner
from .utils import haversine


class StadiumViewSet(viewsets.ModelViewSet):
    queryset = Stadium.objects.filter(active=True)
    serializer_class = StadiumSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['title', 'address']
    ordering_fields = ['price_per_hour', 'title']

    def get_permissions(self):
        # For update and delete actions, require the user to be authenticated and pass IsAdminOrOwner check.
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]
        # For create, you might require authentication as well.
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, IsAdminOrStadiumOwner]
        else:
            # For list and retrieve, you can allow any access or adjust as needed.
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        user_lat = request.query_params.get('lat')
        user_lon = request.query_params.get('long')
        queryset = self.filter_queryset(self.get_queryset())

        if user_lat and user_lon:
            try:
                user_lat = float(user_lat)
                user_lon = float(user_lon)
            except ValueError:
                return Response({"error": "Kordinatalar no to'g'ri berilgan!"}, status=400)

            stadiums_with_distance = []
            for stadium in queryset:
                try:
                    stadium_lat = float(stadium.latitude)
                    stadium_lon = float(stadium.longitude)
                except (ValueError, TypeError):
                    continue

                stadium.distance = haversine(user_lon, user_lat, stadium_lon, stadium_lat)
                stadiums_with_distance.append(stadium)


            stadiums_with_distance.sort(key=lambda s: s.distance)
            page = self.paginate_queryset(stadiums_with_distance)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(stadiums_with_distance, many=True)
            return Response(serializer.data)

        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        images_data = request.data.pop('images', [])
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stadium = serializer.save(owner=request.user)

        for image in images_data:
            StadiumImages.objects.create(stadium=stadium, image=image)

        response_serializer = self.get_serializer(stadium)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

