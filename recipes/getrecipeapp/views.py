from django.shortcuts import redirect, get_list_or_404
from django.urls import reverse_lazy, reverse
from .models import Dishes, Tag
from .forms import ContactForm, RegistrationForm
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q


class DishesView(ListView):
    model = Dishes
    paginate_by = 6
    template_name = 'getrecipeapp/index.html'
    context_object_name = 'dishes'
    ordering = '-id'
    queryset = Dishes.active_objects. \
        select_related('complexity'). \
        prefetch_related('tags').all()
    extra_context = {'title': 'Главная страница'}


class DishesViewCategory(ListView):
    model = Dishes
    paginate_by = 6
    template_name = 'getrecipeapp/index_for_category.html'
    ordering = '-id'
    context_object_name = 'dishes'
    extra_context = {'title': 'Категории'}

    def get_queryset(self):
        tag = self.kwargs['tag']
        result = Dishes.active_objects.\
            select_related('complexity').\
            prefetch_related('tags').filter(tags__name__icontains=tag)
        return result


class DishesViewSearch(ListView):
    model = Dishes
    paginate_by = 6
    template_name = 'getrecipeapp/search.html'
    ordering = '-id'
    context_object_name = 'dishes'
    extra_context = {'title': 'Поиск'}
    allow_empty = False

    def get_queryset(self):
        result = Dishes.active_objects.all()
        q = self.request.GET['q']
        if q:
            result = Dishes.active_objects.select_related('complexity'). \
                prefetch_related('tags').filter(Q(title__icontains=q) |
                                                Q(tags__name__icontains=q) |
                                                Q(description__icontains=q) |
                                                Q(description_full__icontains=q))
        return result


class About(TemplateView):
    template_name = 'getrecipeapp/about.html'
    extra_context = {'title': 'О нас'}


class DishesDetailView(DetailView):
    model = Dishes
    template_name = 'getrecipeapp/post.html'
    extra_context = {'title': 'Рецепт: '}


class Contact(FormView):
    form_class = ContactForm
    template_name = 'getrecipeapp/contact.html'
    success_url = reverse_lazy('dishes:index')
    extra_context = {'title': 'Форма обратной связи'}

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
    extra_context = {'title': 'Добавить\Обновить рецепт'}


class DishesUpdate(LoginRequiredMixin, UpdateView):
    model = Dishes
    fields = '__all__'
    template_name = 'getrecipeapp/create-dishes.html'
    extra_context = {'title': 'Добавить\Обновить рецепт'}

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("dishes:post", kwargs={"pk": pk})


class DishesDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Dishes
    success_url = reverse_lazy('dishes:index')
    template_name = 'getrecipeapp/delete_dishes_confirm.html'
    extra_context = {'title': 'Удалить рецепт'}

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('dishes:access_denied')


class UserLoginView(LoginView):
    template_name = 'getrecipeapp/login.html'
    extra_context = {'title': 'Логин'}


class UserRegistrationView(CreateView):
    template_name = 'getrecipeapp/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('dishes:login')
    extra_context = {'title': 'Регистрация'}


class AccessDenied(TemplateView):
    template_name = 'getrecipeapp/accesdenied.html'
    extra_context = {'title': 'Доступ запрещен'}
