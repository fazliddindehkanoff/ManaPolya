from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import StadiumBooking


class BookingSerializer(serializers.ModelSerializer):
    active = serializers.SerializerMethodField(read_only=True)
    stadium_title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StadiumBooking
        fields = ['id', 'stadium', "stadium_title", 'start_time', 'hours', 'active']
        read_only_fields = ['user']

    def get_stadium_title(self, obj):
        return obj.stadium.title

    def get_active(self, obj):
        now = timezone.now()
        return now < obj.start_time + timedelta(hours=obj.hours)

    def update(self, instance, validated_data):
        new_start_time = validated_data.get('start_time', None)
        if new_start_time:
            if timezone.now() > instance.start_time - timedelta(hours=4):
                raise serializers.ValidationError(
                    "Bron qilish vaqtini o'yin boshlanishidan 4 soat oldin o'zgartira olasiz holos"
                )
            instance.start_time = new_start_time
            instance.save()
        return instance
