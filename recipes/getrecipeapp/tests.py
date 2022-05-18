from django.test import TestCase, Client
from getrecipeapp.models import Dishes, Tag, Category, Complexity, validate_image
from mixer.backend.django import mixer
import os
from django.core.files.images import get_image_dimensions
import numpy as np
from PIL import Image
from django.urls import reverse, reverse_lazy
from faker import Faker
from tqdm import tqdm
from django.contrib.auth.models import User


# Create your tests here.
class CategoryTestCase(TestCase):

    def test_str(self):
        category = mixer.blend(Category)
        self.assertEqual(str(category), category.name)


class TagTestCase(TestCase):

    def test_str(self):
        tag = mixer.blend(Tag)
        self.assertEqual(str(tag), tag.name)


class ComplexityTestCase(TestCase):

    def test_str(self):
        complexity = mixer.blend(Complexity)
        self.assertEqual(str(complexity), complexity.name)


class DishesTestCase(TestCase):

    def setUp(self) -> None:
        imarray = np.random.randint(0, 255, size=(1000, 1000, 3))
        im = Image.fromarray(imarray.astype('uint8')).convert('RGBA')
        self.path_to_tmp_img = os.path.join('media', 'images_full', 'result_image.png')
        im.save(self.path_to_tmp_img)
        self.dish = mixer.blend(Dishes,
                                tags__name=mixer.FAKE,
                                image=os.path.abspath(self.path_to_tmp_img),
                                image_full=os.path.abspath(self.path_to_tmp_img))

    def test_display_tags(self):
        tag = self.dish.tags.first()
        self.assertEqual(self.dish.display_tags(), str(tag))

    def test_resize_image(self):
        self.assertEqual(get_image_dimensions(self.dish.image), (150, 150))

    def test_active_manager(self):
        self.assertEqual(Dishes.objects.count(), 1)
        self.assertEqual(self.dish.is_active, False)
        self.dish.is_active = True
        self.dish.save()
        self.assertEqual(Dishes.objects.count(), 1)
        self.assertEqual(Dishes.active_objects.count(), 1)
        self.assertEqual(self.dish.is_active, True)


class TestOpenView(TestCase):

    def setUp(self) -> None:
        self.fake = Faker()
        self.client = Client()
        self.open_pages = ['about', 'index', 'contact', 'login', 'register', 'access_denied', 'post']
        self.close_pages = ['create-dishes', 'logout', 'update-dishes', 'delete-dishes']
        self.index_page = ['post', 'update-dishes', 'delete-dishes']
        self.path_to_tmp_img = os.path.join('media', 'images_full', 'result_image.png')
        self.dish = mixer.blend(Dishes,
                                tags__name=mixer.FAKE,
                                image=os.path.abspath(self.path_to_tmp_img),
                                image_full=os.path.abspath(self.path_to_tmp_img),
                                is_active=True)

    def test_status_code_open_page(self):
        for page in tqdm(self.open_pages, 'Проверка доступа на открытые страницы'):
            if page not in self.index_page:
                response = self.client.get(reverse(f'dishes:{page}'))
                self.assertEqual(response.status_code, 200)
            else:
                response = self.client.get(reverse(f'dishes:{page}', kwargs={"pk": 1}))
                self.assertEqual(response.status_code, 200)

    def test_status_code_close_page(self):
        for page in tqdm(self.close_pages, 'Проверка доступа на закрытые страницы'):
            if page not in self.index_page:
                response = self.client.get(reverse(f'dishes:{page}'))
                self.assertEqual(response.status_code, 302)
            else:
                response = self.client.get(reverse(f'dishes:{page}', kwargs={"pk": 1}))
                self.assertEqual(response.status_code, 302)

    def test_post_contact(self):
        for page in tqdm(['contact'], 'Отправка контактной формы'):
            response = self.client.post(reverse(f'dishes:{page}'), {'name': self.fake.name(),
                                                                    'email': self.fake.email(),
                                                                    'message': self.fake.text()})
            self.assertEqual(response.status_code, 302)

    def test_get_404(self):
        for page in tqdm([f'{self.fake.name().split()[-1]}'], 'Проверка несуществующей страницы'):
            response = self.client.get(f'{page}/')
            self.assertEqual(response.status_code, 404)

    def test_hidden_element(self):
        response = self.client.get('/')
        self.assertTrue('post-meta article' not in str(response.content.decode()))

    def test_login_required(self):
        User.objects.create_user(username='Carl', password='Carl1234567', email='carl@example.com')
        response = self.client.login(username='Carl', password='Carl1234567')
        self.assertEqual(response, True)
        response = self.client.get(reverse_lazy('dishes:logout'))
        self.assertEqual(response.status_code, 302)

    def test_register_required(self):
        response = self.client.post(reverse('dishes:register'), {'username': 'Carl',
                                                                 'password1': 'Grandtour123456',
                                                                 'password2': 'Grandtour123456',
                                                                 'email': 'carl@example.com'})
        self.assertEqual(response.status_code, 302)

    def test_search_field(self):
        fragment = Dishes.objects.last().title.split()[-1]
        url = '{url}?{filter}={value}'.format(
            url=reverse_lazy('dishes:search'),
            filter='q', value=f'{fragment}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        url = '{url}?{filter}={value}'.format(
            url=reverse_lazy('dishes:search'),
            filter='q', value=f'sdfsdfas')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_content_category(self):
        url = reverse_lazy('dishes:index-category', kwargs={'tag': str(Dishes.objects.last().category.name)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)



class TestTemplateView(TestCase):

    def setUp(self) -> None:
        self.fake = Faker()
        self.client = Client()
        self.path_to_tmp_img = os.path.join('media', 'images_full', 'result_image.png')
        mixer.cycle(5).blend(Dishes,
                             tags__name=mixer.FAKE,
                             image=os.path.abspath(self.path_to_tmp_img),
                             image_full=os.path.abspath(self.path_to_tmp_img),
                             is_active=True)

    def test_DishesViewTemplate(self):
        url = reverse_lazy('dishes:index')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'getrecipeapp/index.html')

    def test_DishesViewCategoryTemplate(self):
        url = reverse_lazy('dishes:index-category', kwargs={'tag': str(Dishes.objects.last().category.name)})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'getrecipeapp/index_for_category.html')

    def test_DishesViewSearchTemplate(self):
        fragment = Dishes.objects.last().title.split()[-1]
        url = '{url}?{filter}={value}'.format(
            url=reverse_lazy('dishes:search'),
            filter='q', value=f'{fragment}')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'getrecipeapp/search.html')

    def test_DishesDetailViewTemplate(self):
        url = reverse_lazy("dishes:post", kwargs={"pk": Dishes.objects.last().category.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'getrecipeapp/post.html')

    def test_AboutTemplate(self):
        url = reverse_lazy('dishes:about')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'getrecipeapp/about.html')

    def test_ContactTemplate(self):
        url = reverse_lazy('dishes:contact')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'getrecipeapp/contact.html')

    def test_DishesCreateTemplate(self):
        User.objects.create_user(username='Carl', password='Carl1234567', email='carl@example.com')
        self.client.login(username='Carl', password='Carl1234567')
        url = reverse_lazy('dishes:create-dishes')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'getrecipeapp/create-dishes.html')

    def test_UserLoginViewTemplate(self):
        url = reverse_lazy('dishes:login')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'getrecipeapp/login.html')

    def test_UserRegistrationViewTemplate(self):
        url = reverse_lazy('dishes:register')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'getrecipeapp/register.html')

    def test_AccessDeniedTemplate(self):
        url = reverse_lazy('dishes:access_denied')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'getrecipeapp/accesdenied.html')

    def test_DishesUpdateTemplate(self):
        User.objects.create_user(username='Carl', password='Carl1234567', email='carl@example.com')
        self.client.login(username='Carl', password='Carl1234567')
        url = reverse_lazy('dishes:update-dishes', kwargs={"pk": Dishes.objects.last().category.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'getrecipeapp/create-dishes.html')

    def test_DishesDeleteTemplate(self):
        User.objects.create_user(username='Carl', password='Carl1234567', email='carl@example.com', is_superuser=True)
        self.client.login(username='Carl', password='Carl1234567')
        url = reverse_lazy('dishes:delete-dishes', kwargs={"pk": Dishes.objects.last().id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'getrecipeapp/delete_dishes_confirm.html')