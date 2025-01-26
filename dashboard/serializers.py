from rest_framework import serializers
from .models import DonationHistory
from event.models import Event
from donor.models import Donor

class DonationHistorySerializer(serializers.ModelSerializer):
    donor = serializers.StringRelatedField(read_only=True)  
    recipient = serializers.StringRelatedField(read_only=True)  
    event = serializers.StringRelatedField(read_only=True)  

    class Meta:
        model = DonationHistory
        fields = '__all__'
