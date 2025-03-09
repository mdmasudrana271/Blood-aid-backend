from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()


router.register('list', views.UserDonationHistoryViewSet,basename='user-donation-history') 
urlpatterns = [
    path('', include(router.urls)),
    path('create/', views.CreateDonationHistoryAPIView.as_view(), name='create'),
    path('donor-donation-history/', views.DonorDonationHistory.as_view(), name='donor-donation-history'),
    
]