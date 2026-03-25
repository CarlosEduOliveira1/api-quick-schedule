from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    USER_TYPE = (
        ('C', 'Customer'),
        ('P', 'Provider')
    )

    username = None
    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=1,
        choices=USER_TYPE,
        default='C'
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []