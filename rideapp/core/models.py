from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = (
        ('rider', 'Rider'),
        ('driver', 'Driver'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='rider')

    def __str__(self):
        return f"{self.username} ({self.role})"


class Ride(models.Model):
    rider = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='rides')
    driver = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='drives')
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('denied', 'Denied'),
    ], default='requested')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.rider.username} → {self.dropoff_location} ({self.status})"
