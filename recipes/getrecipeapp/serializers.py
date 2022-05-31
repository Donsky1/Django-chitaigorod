from .models import Dishes, Category, Tag, Complexity
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ComplexitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Complexity
        fields = '__all__'


class DishesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dishes
        fields = ('title', 'category', 'tags')


class DishesActiveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dishes
        fields = ('title', 'category', 'rating', 'description', 'description_full', 'link')