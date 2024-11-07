from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from webcourse.models import User
from .models import MyUser
from .serializers import UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            user = serializer.save()
            user.isBasicUser = True
            user.save()
            User(uid=user.id, name=user.username).save()
            return Response({
                'message': 'Register successful!'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'error_message': 'This email has already exist!',
                'errors_code': 400,
            }, status=status.HTTP_400_BAD_REQUEST)

class RegisterDataAdmin(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        if user.isAccountAdmin:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
                user = serializer.save()
                user.isDataAdmin = True
                user.save()
                User(uid=user.id, name=user.username).save()
                return Response({
                    'message': 'Register successful!'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error_message': 'This email has already exist!',
                    'errors_code': 400,
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You do not have right to use this function",status=status.HTTP_401_UNAUTHORIZED)

class RegisterAccountAdmin(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        if user.isAccountAdmin:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
                user = serializer.save()
                user.isAccountAdmin = True
                user.save()
                User(uid=user.id, name=user.username).save()
                return Response({
                    'message': 'Register successful!'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error_message': 'This email has already exist!',
                    'errors_code': 400,
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You do not have right to use this function",status=status.HTTP_401_UNAUTHORIZED)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_id'] = user.id
        token['is_basicuser'] = user.isBasicUser
        token['is_dataadmin'] = user.isDataAdmin
        token['is_accountadmin'] = user.isAccountAdmin
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer