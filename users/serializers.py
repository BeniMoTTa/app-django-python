from rest_framework import serializers
from .models import User



class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=127)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(allow_null=True, default=None)
    is_employee = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(read_only=True)
    

    def create(self, validated_data:dict) -> User:
        employee = validated_data["is_employee"]
        if employee:
            return User.objects.create_superuser(**validated_data)
        else:
            return User.objects.create_user(**validated_data)

    def validate_email(self, email):
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise serializers.ValidationError(detail="email already registered.")
        return email

    def validate_username(self, username):
        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError(detail="username already taken.")
        return username

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 20)
    password = serializers.CharField(max_length=130, write_only=True)
    is_superuser = serializers.BooleanField(read_only = True)