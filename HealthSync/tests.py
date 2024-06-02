from django.test import TestCase
from django.test import TestCase
from django.contrib.auth.models import User


class AuthentificationTests(TestCase):
    def test_user_can_login(self):
        user = User.objects.create_user('testuser', 'test@example.com','testpasswd')
        response = self.client.post('HealthSync/login/',{'username' : 'testuser', 'password' :'testpassword'})
        self.assertEqual(response.status_code, 302)