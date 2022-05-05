from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ContactForm(forms.Form):
    name = forms.CharField(label='Введите ваше имя',
                           widget=forms.TextInput(attrs={'placeholder': 'Имя',
                                                         'class': 'form-control'}))
    email = forms.EmailField(label='Введите вашу почту',
                             widget=forms.TextInput(attrs={'placeholder': 'test@email.com',
                                                           'class': 'form-control'})
                             )
    message = forms.CharField(label='Сообщение',
                              widget=forms.TextInput(attrs={'placeholder': 'сообщение',
                                                            'class': 'form-control'})
                              )


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')