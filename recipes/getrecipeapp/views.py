from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from .models import Dishes
from .forms import ContactForm
from django.core.mail import send_mail


# Create your views here.
def index_page(request):
    dishes = Dishes.objects.all()
    return render(request, 'getrecipeapp/index.html', context={'dishes': dishes[:6]})


def about(request):
    return render(request, 'getrecipeapp/about.html')


def post(request, id):
    post = get_object_or_404(Dishes, id=id)
    return render(request, 'getrecipeapp/post.html', context={'post': post})


def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(
                f'Contact message from {name}',
                f'Here is the {message}.',
                'from@example.com',
                [email],
                fail_silently=True,
            )

            return HttpResponseRedirect(reverse('dishes:index'))
        else:
            return render(request, 'getrecipeapp/contact.html', context={'form': form})
    else:
        form = ContactForm()
        return render(request, 'getrecipeapp/contact.html', context={'form': form})
