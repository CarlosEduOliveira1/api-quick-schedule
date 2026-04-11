from django.db import models
from django.conf import settings
from services.models import Service

# Create your models here.
class Scheduling(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_scheduling',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='scheduling',
    )
    hour_beginning = models.DateTimeField()
    hour_ending = models.DateTimeField(editable=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.hour_ending = self.hour_beginning + self.service.duration
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.customer} -> {self.service} em {self.hour_beginning}"