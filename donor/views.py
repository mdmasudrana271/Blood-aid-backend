from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import status


from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect


class DonorViewset(viewsets.ModelViewSet):
    queryset = models.Donor.objects.all()
    serializer_class = serializers.DonorSerializer

    

class DonorListAPIView(APIView):
    def get(self, request):
        blood_group = request.query_params.get('blood_group', None)

        donors = models.Donor.objects.filter(is_available_for_donation=True)

        
        if blood_group:
            blood_group = blood_group.strip()  # Remove extra spaces
            donors = donors.filter(blood_group__iexact=blood_group)

        
        serializer = serializers.DonorSerializer(donors, many=True)
        return Response(serializer.data)

    




class DonorProfileUpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request):
        try:
            # Try to get the donor profile for the logged-in user
            donor, created = models.Donor.objects.get_or_create(user=request.user)
            
            # Use the serializer to validate and update the donor's profile
            serializer = serializers.DonorSerializer(donor, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Profile updated successfully.", "data": serializer.data}, status=200)
            
            return Response({"errors": serializer.errors}, status=400)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)





class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            print("token ", token)
            models.Donor.objects.create(user=user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid ", uid)
            confirm_link = f"https://blood-aid-backend.vercel.app/account/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response({'data':"Check your mail for confirmation"})
        return Response(serializer.errors)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('https://blood-aid-client.vercel.app/login')
    else:
        return redirect('https://blood-aid-client.vercel.app/signup')
    

class UserLoginApiView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username= username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request, user)
                # donor = models.Donor.objects.get(user=user);
                try:
                    donor = models.Donor.objects.get(user=user)
                except models.Donor.DoesNotExist:
                    donor = None
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'donor_id':donor.id,
                    'username': user.username,
                    'first_name':user.first_name,
                    'last_name':user.last_name,
                },status=status.HTTP_200_OK)
            else:
                return Response({'error' : "Invalid Credential"},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors)



class UserLogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            request.user.auth_token.delete()
            logout(request)
            return Response({"message": "Logged out successfully."}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)