from django.test import TestCase, Client  # Client allows us to make requests
from django.contrib.auth import get_user_model
from django.urls import reverse  # allows for generation of urls


class AdminSiteTests(TestCase):
    # setup function that is ran before every test that is run
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="password"
        )
        # logins in superuser
        self.client.force_login(self.admin_user)
        # Create user for checks
        self.user = get_user_model().objects.create_user(
            email='user@test.com',
            password="password",
            name="Name"
        )

    def test_users_listed(self):
        """Test that users are listed on the user page"""

        # We want to generate the url. These are defined in the docs
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        # assertContains is a django assertion that checks if a response
        # contains a certain item, as well as checking the response is 200
        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""

        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_user_add_page(self):
        """Test that the create user page works"""

        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
