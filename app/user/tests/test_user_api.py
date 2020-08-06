from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient  # Test client to make request to API
from rest_framework import status  # use human readable codes


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Tets the public users API"""

    # Is this called before each test?
    def setUp(self):
        self.client = APIClient()  # one client for test suite

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

    def test_create_token_for_user(self):
        """Test that a token is created"""

        payload = {
            'email': 'test@email.com',
            'password': 'testPW'
        } 

        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)

        # As we are going to use the built in django token auth system
        # there is no need to test that the token works
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        valid_user_data = {
            'email': 'test@email.com',
            'password': 'testPW'
        }

        create_user(**valid_user_data)

        payload = {
            'email': 'test@email.com',
            'password': 'wrong'
        }

        response = self.client.post(TOKEN_URL, payload)

        # As we are going to use the built in django token auth system
        # there is no need to test that the token works
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        payload = {
            'email': 'test@email.com',
            'password': 'testPW'
        }

        response = self.client.post(TOKEN_URL, payload)

        # As we are going to use the built in django token auth system
        # there is no need to test that the token works
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_retrieve_user_unauth(self):
    #     """Test auth is required for users"""

    #     response = self.client.get(ME_URL)

    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_retrieve_user_unauthorized(self):
        """Test that authentication required for users"""
        
        res = self.client.get(ME_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUsersAPITest(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@email.com',
            password='testPW',
            name='test'
        )
        self.client = APIClient()
        # simulate authenticated requests
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""

        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'email': self.user.email,
            'name': self.user.name
        })

    def test_post_me_not_allowed(self):
        """Test tgar POST is not allowed on the me url"""

        response = self.client.post(ME_URL, {})

        self.assertEqual(response.status_code,
                        status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""

        payload = {'name': 'new name', 'password': 'newPW!'}

        response = self.client.patch(ME_URL, payload)

        # helper function to pull latest values
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
