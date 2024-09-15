from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework import generics, mixins
from .serializers import UserRegistrationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserLoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Variety
from .serializers import VarietySerializer
from .filters import VarietyFilter
from django.db import connections


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            print(f"Authenticated user: {user}")  # Отладка
            return Response({
                'username': user.username,
                'message': 'Вход успешен'
            }, status=status.HTTP_200_OK)
        print(f"Validation errors: {serializer.errors}")  # Отладка
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObjectsListView(generics.ListAPIView):
    queryset = Objects.objects.all()
    serializer_class = ObjectsSerializer


class VarietyView(APIView):
    def get(self, request):
        # Получение данных из модели Variety
        varieties = Variety.objects.all()
        serializer = VarietySerializer(varieties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrdersSerializer(data=request.data, context={'request': request})  # Передаем контекст
        if serializer.is_valid():
            order = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
