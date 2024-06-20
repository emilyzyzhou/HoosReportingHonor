from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

class GoogleLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.login_url = reverse('account_login')  

    def test_valid_google_login(self):
        response = self.client.post(self.login_url, {
            'login': 'testuser',
            'password': 'testpassword123'
        }, follow=True)

        # Check that the response is the home page (login succeeded)
        self.assertEqual(response.request['PATH_INFO'], reverse('shared:home'))

    def test_invalid_google_login(self):
        response = self.client.post(self.login_url, {
            'login': 'testuser',
            'password': 'wrongpassword'
        }, follow=False)

        # Check that the response is the login page (login failed)
        self.assertEqual(response.request['PATH_INFO'], self.login_url)


