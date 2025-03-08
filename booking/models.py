from django.db import models

from authentication.models import User
from stadium.models import Stadium


class StadiumBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    stadium = models.ForeignKey(Stadium, on_delete=models.PROTECT, related_name="booked_times")
    start_time = models.DateTimeField()
    hours = models.IntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["stadium", "start_time"], name="unique_booking"),
        ]

    def __str__(self):
        return f"{self.user.phone_number} booked {self.stadium.title} from {self.start_time} to {self.end_time}"

