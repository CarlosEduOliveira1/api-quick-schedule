from django.db import models
from django.contrib.auth.hashers import make_password

class UserType(models.TextChoices):
    CUSTOMER = 'C', 'Customer'
    PROVIDER = 'P', 'Provider'

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    user_type = models.CharField(
        max_length=1,
        choices=UserType.choices,
        default=UserType.CUSTOMER
    )
    create_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)