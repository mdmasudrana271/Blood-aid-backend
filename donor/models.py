from django.db import models
from django.contrib.auth.models import User

# Create your models here.

BLOOD_GROUP_CHOICES = [
        ('O+', 'O+'), ('O-', 'O-'),
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="donor_profile")
    age = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    last_donation_date = models.DateField(null=True, blank=True)
    is_available_for_donation = models.BooleanField(default=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES,blank=True,null=True)


    def __str__(self):
        return self.user.username