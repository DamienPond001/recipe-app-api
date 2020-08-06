from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsAPITests(TestCase):
    """Test the publically avaliable ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required"""

        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITests(TestCase):
    """Test ingredients can be retrieved by authed user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email="test@email.com",
            password="testPW"
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieveing a list of ingredients"""

        Ingredient.objects.create(user=self.user, name="Cucumber")
        Ingredient.objects.create(user=self.user, name="Lemon")

        response = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients for the authed user are returned"""

        user_2 = get_user_model().objects.create(
            email="testother@email.com",
            password="testPWother"
        )

        Ingredient.objects.create(user=user_2, name="Potato")
        Ingredient.objects.create(user=user_2, name="Tomato")

        ingredient = Ingredient.objects.create(user=self.user, name='Potato')

        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], ingredient.name)

    def test_ingredient_success(self):
        """Test successful creation of ingredient"""
        payload = {'name': 'Lettuce'}

        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_ingredient_invalid(self):
        """test for invalid payload"""

        payload = {'name': ''}
        response = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
