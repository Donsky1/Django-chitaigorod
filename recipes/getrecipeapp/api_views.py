from .models import Dishes, Category, Tag, Complexity
from rest_framework import viewsets, permissions
from .serializers import CategorySerializer, TagSerializer, ComplexitySerializer, DishesSerializer, DishesActiveSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ComplexityViewSet(viewsets.ModelViewSet):
    queryset = Complexity.objects.all()
    serializer_class = ComplexitySerializer


class DishesViewSet(viewsets.ModelViewSet):
    queryset = Dishes.objects.all()
    serializer_class = DishesSerializer
    permission_classes = [permissions.IsAuthenticated]


class DishesActiveViewSet(viewsets.ModelViewSet):
    queryset = Dishes.active_objects.all()
    serializer_class = DishesActiveSerializer
    permission_classes = [permissions.IsAuthenticated]