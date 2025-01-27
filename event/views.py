from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class EventViewset(viewsets.ModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer


class EventListAPIView(APIView):
    def get(self, request):
        blood_group = request.query_params.get('blood_group', None)

        event = models.Event.objects.all()

        
        if blood_group:
            blood_group = blood_group.strip()  # Remove extra spaces
            event = event.filter(blood_group__iexact=blood_group)

        
        serializer = serializers.EventSerializer(event, many=True)
        return Response(serializer.data)



class EventCreateAPIView(APIView):
    serializer_class = serializers.EventSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            # Assign the creator to the currently authenticated user
            event = serializer.save(creator=request.user)
            print(event)
            return Response({"message":"Successfully created your event for blood requests"})
        return Response({"errors": serializer.errors}, status=400)



