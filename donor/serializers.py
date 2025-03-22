from rest_framework import serializers
from .models import Donor
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'username': {'read_only': True},  # Make username non-editable
        }

class DonorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Donor
        fields = '__all__'


    def update(self, instance, validated_data):
        # Extract the nested user data
        user_data = validated_data.pop('user', {})
        
        # Update the related User instance
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update the Donor instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance



class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
    
    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        
        if password != confirm_password:
            raise serializers.ValidationError({'error' : "Password Doesn't Mactched"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error' : "Email Already exists"})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error' : "Username Already exists"})
        account = User(username = username, email=email, first_name = first_name, last_name = last_name)
        print(account)
        account.set_password(password)
        account.is_active = False
        account.save()
        return account


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)



