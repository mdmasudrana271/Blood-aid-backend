from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    creator_id = serializers.IntegerField(source='creator.id', read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'blood_group', 'created_at', 'status', 'creator_id', 'creator']
