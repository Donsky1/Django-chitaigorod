from .models import Dishes, Category, Tag, Complexity
from django.contrib.auth.models import User

from rest_framework import viewsets, permissions
from .serializers import CategorySerializer, TagSerializer, ComplexitySerializer, DishesActiveSerializer, \
    UsersSerializer
from .permissions import ReadOnly
from rest_framework import authentication


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser | ReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser | ReadOnly]
    authentication_classes = [authentication.BasicAuthentication,
                              authentication.SessionAuthentication,
                              authentication.TokenAuthentication]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ComplexityViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser | ReadOnly]
    authentication_classes = [authentication.BasicAuthentication,
                              authentication.SessionAuthentication,
                              authentication.TokenAuthentication]
    queryset = Complexity.objects.all()
    serializer_class = ComplexitySerializer


class DishesActiveViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser | ReadOnly]
    authentication_classes = [authentication.BasicAuthentication,
                              authentication.SessionAuthentication,
                              authentication.TokenAuthentication]
    queryset = Dishes.active_objects.all()
    serializer_class = DishesActiveSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [authentication.SessionAuthentication,
                              authentication.TokenAuthentication]
    queryset = User.objects.all()
    serializer_class = UsersSerializer
