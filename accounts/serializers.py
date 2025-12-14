from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('telegram_username', 'full_name', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            telegram_username=validated_data['telegram_username'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ''),
            email=validated_data.get('email', '')
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'telegram_username', 'full_name')
