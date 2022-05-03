from django import forms


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
