

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import EventViewset,EventCreateAPIView

router = DefaultRouter()
router.register('list', EventViewset)  # Register only viewsets with the router

urlpatterns = [
    path('', include(router.urls)),  # Includes the router URLs
    path('create/', EventCreateAPIView.as_view(), name='create'),  # Add APIView directly
]
