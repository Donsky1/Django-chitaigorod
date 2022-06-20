"""recipes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from getrecipeapp import views
from django.contrib.auth.views import LogoutView
from rest_framework import routers
from getrecipeapp.api_views import CategoryViewSet, TagViewSet, ComplexityViewSet, DishesActiveViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('category', CategoryViewSet)
router.register('tag', TagViewSet)
router.register('complexity', ComplexityViewSet)
router.register('dish_active', DishesActiveViewSet)
router.register('users', UserViewSet)

app_name = 'getrecipeapp'

urlpatterns = [
    path('', views.DishesView.as_view(), name='index'),
    path('category/<str:tag>', views.DishesViewCategory.as_view(), name='index-category'),
    path('search/', views.DishesViewSearch.as_view(), name='search'),
    path('about/', views.About.as_view(), name='about'),
    path('post/<int:pk>', views.DishesDetailView.as_view(), name='post'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('create-dishes/', views.DishesCreate.as_view(), name='create-dishes'),
    path('update-dishes/<int:pk>', views.DishesUpdate.as_view(), name='update-dishes'),
    path('delete-dishes/<int:pk>', views.DishesDelete.as_view(), name='delete-dishes'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('access_denied/', views.AccessDenied.as_view(), name='access_denied'),
    path('profile/<int:pk>', views.DetailUser.as_view(), name='user-profile'),
    path('generate-token/', views.generate_token, name='generate_token'),
    path('api/v0/', include(router.urls)),
]
