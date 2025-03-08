from django.db import models

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
