from django.test import TestCase
from django.contrib.auth import get_user_model
# note that we can import the User Model directly, but if we ever change our
# user model then we would have to change it everywhere instead of just in the
# settings

from core import models


def sample_user(email='test@email.com', password='testPW'):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_success(self):
        """Test creating a new user with and email"""

        email = 'test@live.com'
        password = 'password'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normailse(self):
        """Test the email for a new user is normalised"""

        email = "test@UPPERcASE.Com"

        user = get_user_model().objects.create_user(
            email=email,
            password='password'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '123')

    def test_create_superuser(self):
        """Test creating new superuser"""

        user = get_user_model().objects.create_superuser(
            email='test@live.com',
            password='password'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """test tag string repr"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """test ingredient string repr"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="Cucumber"
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """test recipe string repr"""

        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Test Recipe',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)
