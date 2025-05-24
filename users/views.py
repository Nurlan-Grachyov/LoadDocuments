from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase


class RegisterCreateAPIView(generics.CreateAPIView):
    """
    Класс регистрации пользователя
    """

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


class MyTokenObtainPairView(TokenObtainPairView, TokenViewBase):
    """
    Переопределение класса TokenObtainPairView с предоставлением доступа всем
    """

    permission_classes = [AllowAny]
