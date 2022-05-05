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

from django.urls import path
from getrecipeapp import views
from django.contrib.auth.views import LogoutView

app_name = 'getrecipeapp'

urlpatterns = [
    path('', views.DishesView.as_view(), name='index'),
    path('about/', views.About.as_view(), name='about'),
    path('post/article/<int:pk>', views.DishesDetailView.as_view(), name='post'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('create-dishes/', views.DishesCreate.as_view(), name='create-dishes'),
    path('update-dishes/<int:pk>', views.DishesUpdate.as_view(), name='update-dishes'),
    path('delete-dishes/<int:pk>', views.DishesDelete.as_view(), name='delete-dishes'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('access_denied/', views.AccessDenied.as_view(), name='access_denied'),
]