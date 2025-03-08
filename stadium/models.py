from datetime import timedelta

from django.db import models
from django.core.exceptions import ValidationError

from authentication.models import User


class Stadium(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fields")
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    longitude = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class StadiumImages(models.Model):
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="stadium_images/")

    def __str__(self):
        return f"Image for {self.stadium.title}"


class StadiumBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    stadium = models.ForeignKey(Stadium, on_delete=models.PROTECT, related_name="booked_times")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["stadium", "start_time", "end_time"], name="unique_booking"),
        ]

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("Bron qilish yakunlanish vaqti boshlanish vaqtidan katta bo'lishi kerak !")
        
        if self.end_time - self.start_time <= timedelta(hours=1):
            raise ValidationError("Eng kamida 1 soat uchun bron qilishingiz kerak")

    def __str__(self):
        return f"{self.user.phone_number} booked {self.stadium.title} from {self.start_time} to {self.end_time}"

