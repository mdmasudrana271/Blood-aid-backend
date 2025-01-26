from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import DonationHistory
from event.models import Event
from .serializers import DonationHistorySerializer
from django.contrib.auth.models import User
from . import serializers



class UserDonationHistoryViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user

        # Fetch donations where the user is a donor
        donated_history = DonationHistory.objects.filter(donor=user).order_by("-accepted_at")
        # Fetch donations where the user is a recipient
        received_history = DonationHistory.objects.filter(recipient=user).order_by("-accepted_at")

        # Serialize the data
        donated_serializer = DonationHistorySerializer(donated_history, many=True)
        received_serializer = DonationHistorySerializer(received_history, many=True)

        # Combine both histories in one response
        combined_history = donated_serializer.data + received_serializer.data

        # Sort by 'accepted_at' to show them chronologically in a single table
        combined_history.sort(key=lambda x: x.get("accepted_at"), reverse=True)

        return Response(combined_history)

class CreateDonationHistoryAPIView(APIView):
    serializer_class = serializers.DonationHistorySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data)
        donor = self.request.user
        event_id = request.data.get('event_id')
        recipient_id = request.data.get('recipient_id')

        if not event_id or not recipient_id:
            return Response({"error": "Event ID and Recipient ID are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            return Response({"error": "Recipient not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create the donation history entry
        donation_history = DonationHistory.objects.create(
            donor=donor,
            recipient=recipient,
            event=event,
            status="accepted",
            blood_group=event.blood_group,
        )
        event.status = "accepted"  # Or use another field to mark it as unavailable
        event.save()

        serializer = DonationHistorySerializer(donation_history)
        return Response({"message": "Request accepted successfully.", "data": serializer.data}, status=200)
        
