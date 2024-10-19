from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class UserSignupTests(APITestCase):
    def test_signup_success(self):
        url = reverse('user-signup')
        data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "securepassword123",
            "first_name": "Test",
            "last_name": "User"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['email'], data['email'])

    def test_signup_email_already_exists(self):
        url = reverse('user-signup')
        data = {
            "email": "existinguser@example.com",
            "username": "newuser",
            "password": "newpassword123",
        }
        # Create an existing user
        self.client.post(url, data, format='json')
        # Try to create another user with the same email
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
