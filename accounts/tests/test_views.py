from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status


User = get_user_model()


class SignUpAPITests(APITestCase):
    def setUp(self):
        self.signup_url = reverse("signup_api_view")
        self.correct_user_data = {
            "email": "test_user@email.com",
            "password": "test_pass",
        }
        self.incorrect_user_data = {
            "email": "test_user@email.com",
            "password": "",
        }

    def test_register_user(self):
        response = self.client.post(
            self.signup_url, self.correct_user_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, "test_user@email.com")

    def test_register_user_with_incorrect_data(self):
        response = self.client.post(
            self.signup_url, self.incorrect_user_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_register_user_with_duplicate_email(self):
        # Creating initial user.
        User.objects.create_user(
            email="initial_user@email.com",
            password="test_pass",
        )

        data = {
            "email": "initial_user@email.com",
            "password": "test_pass",
        }

        # Attempting to create second user with the same email address.
        response = self.client.post(self.signup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
