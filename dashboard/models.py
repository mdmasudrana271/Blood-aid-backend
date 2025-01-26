from django.db import models
from django.contrib.auth.models import User
from event.models import Event
# Create your models here.

STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('canceled', 'Canceled'),
        ('recieved', 'Recieved'),
    ]


class DonationHistory(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donor_history")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient_history")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="related_donations")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    accepted_at = models.DateTimeField(auto_now_add=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"Donation from {self.donor.username} to {self.recipient.username} - {self.status}"