from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='Введите ваше имя')
    email = forms.EmailField(label='Введите вашу почту')
    message = forms.CharField(label='Сообщение')