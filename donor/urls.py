from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()


router.register('list', views.DonorViewset) 
urlpatterns = [
    path('', include(router.urls)),
    path('update/', views.DonorProfileUpdateView.as_view(), name='update'),
    path('available_donor/', views.DonorListAPIView.as_view(), name='available_donor'),
    path('register/', views.UserRegistrationApiView.as_view(), name='register'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
]