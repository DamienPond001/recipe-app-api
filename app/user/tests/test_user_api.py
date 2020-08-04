from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient  # Test client to make request to API
from rest_framework import status  # use human readable codes


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Tets the public users API"""

    def setUp(self):
        self.client = APIClient()  # one lcient for test suite

    def test_create_valid_user_success(self):
        """Test user with valid payload"""
        payload = {
            'email': 'test@email.com',
            'password': 'testPW',
            'name': 'Test name'
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """Test that user exists"""
        payload = {
            'email': 'test@email.com',
            'password': 'testPW',
            'name': 'Test name'
        }

        create_user(**payload)

        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pw_too_short(self):
        """pw must more than 5 characters"""

        payload = {
            'email': 'test@email.com',
            'password': 'test',
            'name': 'Test name'
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)
