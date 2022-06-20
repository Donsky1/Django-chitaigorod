from .models import Dishes, Category, Tag, Complexity
from rest_framework import serializers
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ComplexitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Complexity
        fields = '__all__'


class DishesActiveSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    category = serializers.StringRelatedField()

    class Meta:
        model = Dishes
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'