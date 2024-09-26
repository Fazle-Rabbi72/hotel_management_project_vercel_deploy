from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)  # Custom field to differentiate between admin and regular users
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-generated timestamp for account creation
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return self.username