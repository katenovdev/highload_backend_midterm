# market/serializers.py

from rest_framework import serializers
from .models import User, Category, Product

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        model = User
        fields = ['login', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password']) 
        user.save()
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category']
