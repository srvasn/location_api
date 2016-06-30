from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from gis_api.serializers import UserSerializer


# __author__ = 'Sourav Banerjee'
# __email__ = ' srvasn@gmail.com'

class AccountTests(APITestCase):
    """
    Test if we can successfully create a user
    """

    def setUp(self):
        # self.superuser = User.objects.create_superuser("derek", "derek@wind.com", "testpassword")
        # self.client.login(username="derek", password="testpassword")
        self.data = {"username": "john", "password": "testpassword", "name": "Express Communications", "lang": "ENG",
                     "curr": "GBP", "email": "express@gmail.com", "phone": "9132452321"}

    def test_can_create_user(self):
        response = self.client.post(reverse("vendors-list"), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReadUserTest(APITestCase):
    """
    Test if we can successfully read user list and user detail
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.create(username="mike")

    def test_can_read_user_list(self):
        response = self.client.get(reverse('vendors-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_user_detail(self):
        response = self.client.get(reverse('vendors-list'), args=[self.user.id])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateUserTest(APITestCase):
    """
    Test if we can update an existing user using PUT
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.create_user(username="mike", password="testpassword", email="mike@tyson.com")
        self.data = UserSerializer(self.user).data
        self.data.update(
            {'name': 'Mike Tyson', 'password': 'testpassword', 'phone': '213233555', 'lang': 'ENG', 'curr': 'USD',
             'email': 'changed@changed.com'})

    def test_can_update_user(self):
        response = self.client.put(reverse("vendors-detail", args=[self.user.id]), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteUserTest(APITestCase):
    """
    Test if we can delete a user
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.create(username="mikey")

    def test_can_delete_user(self):
        response = self.client.delete(reverse('vendors-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
