from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserAPITestCase(APITestCase):
    def test_register(self):
        url = reverse("users:register")
        data = {
            "email": "test@example.com",
            "password": "testpass123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())
        user = User.objects.get(email="test@example.com")
        self.assertTrue(user.check_password("testpass123"))

    def test_login(self):
        User.objects.create_user(email="login@example.com", password="testpass123")
        url = reverse("users:login")
        data = {"email": "login@example.com", "password": "testpass123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
