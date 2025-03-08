from rest_framework import serializers
from .models import Stadium, StadiumImages


class StadiumImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StadiumImages
        fields = ["id", "image"]


class StadiumSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

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
            "owner"
        ]

    def get_distance(self, obj):
        return f"{round(obj.distance, 2)} km" if hasattr(obj, "distance") else None
