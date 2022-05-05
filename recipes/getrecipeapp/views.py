from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from .models import Dishes
from .forms import ContactForm, RegistrationForm
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class DishesView(ListView):
    model = Dishes
    paginate_by = 6
    template_name = 'getrecipeapp/index.html'
    context_object_name = 'dishes'


class About(TemplateView):
    template_name = 'getrecipeapp/about.html'


class DishesDetailView(DetailView):
    model = Dishes
    template_name = 'getrecipeapp/post.html'


class Contact(FormView):
    form_class = ContactForm
    template_name = 'getrecipeapp/contact.html'
    success_url = reverse_lazy('dishes:index')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        send_mail(f'Contact message from {name}',
                  f'Here is the {message}.',
                  'from@example.com',
                  [email],
                  fail_silently=True,
                  )

        return super().form_valid(form)


class DishesCreate(LoginRequiredMixin, CreateView):
    model = Dishes
    fields = '__all__'
    success_url = reverse_lazy('dishes:index')
    template_name = 'getrecipeapp/create-dishes.html'


class DishesUpdate(LoginRequiredMixin, UpdateView):
    model = Dishes
    fields = '__all__'
    template_name = 'getrecipeapp/create-dishes.html'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("dishes:post", kwargs={"pk": pk})


class DishesDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Dishes
    success_url = reverse_lazy('dishes:index')
    template_name = 'getrecipeapp/delete_dishes_confirm.html'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('dishes:access_denied')


class UserLoginView(LoginView):
    template_name = 'getrecipeapp/login.html'


class UserRegistrationView(CreateView):
    template_name = 'getrecipeapp/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('dishes:login')


class AccessDenied(TemplateView):
    template_name = 'getrecipeapp/accesdenied.html'