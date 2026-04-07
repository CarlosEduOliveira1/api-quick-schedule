from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Service(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8,decimal_places=2)
    duration = models.DurationField()
    is_active = models.BooleanField(default=True)

class ProviderAvailability(models.Model):
    WEEK_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    week_day = models.IntegerField(
        choices=WEEK_CHOICES
    )
    hour_beginning = models.TimeField()
    hour_ending = models.TimeField()