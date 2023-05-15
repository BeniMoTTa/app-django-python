from django.shortcuts import render
from rest_framework.views import APIView, Response
from django.contrib.auth import authenticate
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .permissions import IsEmployeeOrNormalUser

class RegisterView(APIView):
    def post(self, req) -> Response:
        serializer = UserSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, 201)
class LoginView(APIView):
    def post(self, req) -> Response:
        serializers = TokenObtainPairSerializer(data=req.data)
        serializers.is_valid(raise_exception=True)

        return Response(serializers.validated_data, 200)

class UserDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrNormalUser]

    def get(self, req, user_id):
        user = User.objects.get(id=user_id)
        self.check_object_permissions(req, user)
        serializer = UserSerializer(user)

        return Response(serializer.data, 200)
    
    def patch(self, req, user_id):
        user = User.objects.get(id=user_id)
        serializers = UserSerializer(data=req.data, partial=True)
        serializers.is_valid(raise_exception=True)
        self.check_object_permissions(req, user)
        for key, value in serializers.validated_data.items():
            setattr(user, key, value)
        user.set_password(serializers.validated_data.get("password"))
        user.save()
        serializers = UserSerializer(user)
        return Response(serializers.data, 200)