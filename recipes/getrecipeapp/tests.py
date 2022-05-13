import io
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
                                image_full=os.path.abspath(self.path_to_tmp_img))

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
        User.objects.create_user(username='Carl', password='Carl1234567', email='carl@example.com')
        self.client.login(username='Carl', password='Carl1234567')
        response = self.client.get('/')
        self.assertTrue('post-meta article' in str(response.content.decode()))

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