from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Category, Tag
import requests


class TestAPICategory(APITestCase):

    def setUp(self) -> None:
        self.url = 'http://127.0.0.1:8000/api/v0/category/'
        User.objects.create_superuser(username='admin', password='admin12345')
        User.objects.create_user(username='baseuser', password='baseuser12345')
        self.data = {'name': 'TestInsertCategory'}
        Category.objects.create(name='TestCategoryBase')

    def test_api_category_anonymous_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_api_category_base_user(self):
        self.client.login(username='baseuser', password='baseuser12345')
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, 200)
        self.assertContains(response_get, 'TestCategoryBase')
        response_post = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response_post.status_code, 403)

    def test_api_category_admin(self):
        self.client.login(username='admin', password='admin12345')
        # GET
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, 200)
        self.assertContains(response_get, 'TestCategoryBase')
        # POST
        response_post = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response_post.status_code, 201)


class TestAPITag(APITestCase):

    def setUp(self) -> None:
        self.url = 'http://127.0.0.1:8000/api/v0/tag/'
        self.admin = User.objects.create_superuser(username='admin', password='admin12345')
        self.user = User.objects.create_user(username='baseuser', password='baseuser12345')
        self.data = {'name': 'TestInsertTag'}
        Tag.objects.create(name='TestTagBase')

    def test_api_tag_anonymous_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_api_tag_base_user(self):
        self.client.login(username='baseuser', password='baseuser12345')
        # GET
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, 200)

        # GET Token
        client = APIClient()
        token_base_user = Token.objects.create(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token_base_user.key)
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, 200)

        # POST
        response_post = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response_post.status_code, 403)

    def test_api_category_admin(self):
        self.client.login(username='admin', password='admin12345')
        # GET
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, 200)

        # GET Token
        client = APIClient()
        token_admin = Token.objects.create(user=self.admin)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token_admin.key)
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, 200)

        # POST
        response_post = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response_post.status_code, 201)


class TestAPITag(APITestCase):

    def setUp(self) -> None:
        self.url = 'http://127.0.0.1:8000/api/v0/tag/'
        self.admin = User.objects.create_superuser(username='admin', password='admin12345')
        self.user = User.objects.create_user(username='baseuser', password='baseuser12345')
        self.data = {'name': 'TestInsertTag'}
        Tag.objects.create(name='TestTagBase')

    def test_api_tag_anonymous_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_api_tag_base_user(self):
        self.client.login(username='baseuser', password='baseuser12345')
        # GET
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, 200)

        # GET Token
        client = APIClient()
        token_base_user = Token.objects.create(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token_base_user.key)
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, 200)

        # POST
        response_post = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response_post.status_code, 403)

    def test_api_tag_admin(self):
        self.client.login(username='admin', password='admin12345')
        # GET
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, 200)

        # GET Token
        client = APIClient()
        token_admin = Token.objects.create(user=self.admin)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token_admin.key)
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, 200)

        # POST
        response_post = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response_post.status_code, 201)


class TestAPIUsers(APITestCase):

    def setUp(self) -> None:
        self.url = 'http://127.0.0.1:8000/api/v0/users/'
        self.admin = User.objects.create_superuser(username='admin', password='admin12345')
        self.user = User.objects.create_user(username='baseuser', password='baseuser12345')

    def test_api_users_anonymous_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_api_users_base_user(self):
        self.client.login(username='baseuser', password='baseuser12345')
        # GET
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, 403)

        # GET Token
        client = APIClient()
        token_base_user = Token.objects.create(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token_base_user.key)
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, 403)

    def test_api_users_admin(self):
        self.client.login(username='admin', password='admin12345')
        # GET
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, 200)

        # GET Token
        client = APIClient()
        token_admin = Token.objects.create(user=self.admin)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token_admin.key)
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, 200)