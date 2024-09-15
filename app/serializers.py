from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import *

User = get_user_model()

# User
# ___________________________________________________________


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)  # Добавляем поле phone_number

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'phone_number']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['name'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', '')  # Устанавливаем значение phone_number
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Неверные данные для входа")
        return {'user': user}
# __________________________________________________________________________________


class ObjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objects
        fields = ['id', 'name']


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'product', 'kilogram', 'total_price', 'is_active']
        read_only_fields = ['total_price']
        # Метод для автоматической установки текущего пользователя как заказчика

    def create(self, validated_data):
        # Получаем пользователя из контекста запроса
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            validated_data['customer'] = request.user
        else:
            raise serializers.ValidationError("User is required")

        return super().create(validated_data)


class VarietySerializer(serializers.ModelSerializer):
    is_this = serializers.SerializerMethodField()

    class Meta:
        model = Variety
        fields = ['id', 'img', 'title', 'description', 'is_this', 'stock', 'price']

    def get_is_this(self, obj):
        # Используем сериализатор ObjectsSerializer для преобразования связанных объекта
        serializer = ObjectsSerializer(obj.is_this)
        return serializer.data['name']
