from django.db import models
from django.contrib.auth.models import User

# Create your models here.


BLOOD_GROUP_CHOICES = [
        ('O+', 'O+'), ('O-', 'O-'),
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('canceled', 'Canceled'),
        ('recieved', 'Recieved'),
    ]

class Event(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_events")
    title = models.CharField(max_length=255)
    description = models.TextField()
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    address = models.CharField(max_length=500,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.title} by {self.creator.username}"