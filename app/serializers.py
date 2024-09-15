from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


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
            username=validated_data['username'],
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

