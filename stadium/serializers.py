from datetime import timedelta
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import serializers

from .models import Stadium, StadiumImages


class StadiumImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StadiumImages
        fields = ["id", "image"]


class StadiumSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()
    available = serializers.SerializerMethodField()

    images = StadiumImagesSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    latitude = serializers.CharField(write_only=True)
    longitude = serializers.CharField(write_only=True)

    class Meta:
        model = Stadium
        fields = [
            "id",
            "title",
            "longitude",
            "latitude",
            "price_per_hour",
            "address",
            "images",
            "distance",
            "owner",
            "available"
        ]

    def get_distance(self, obj):
        return f"{round(obj.distance, 2)} km" if hasattr(obj, "distance") else None

    def get_available(self, obj):
        start_time_str = self.context.get("start_time")
        if not start_time_str:
            return True

        query_start = parse_datetime(start_time_str)
        if not query_start:
            return True

        if timezone.is_naive(query_start):
            query_start = timezone.make_aware(query_start, timezone.get_current_timezone())

        if query_start < timezone.now():
            return False

        for booking in obj.booked_times.all():
            booking_end = booking.start_time + timedelta(hours=booking.hours)
            if booking.start_time <= query_start < booking_end:
                return False
        return True



