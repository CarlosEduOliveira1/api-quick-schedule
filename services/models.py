from django.db import models
from ..users.models import User

# Create your models here.
class Service(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(...)
    duration = models.IntegerField()
    is_active = models.BooleanField(default=True)