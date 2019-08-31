from django.contrib.auth.models import User
from django.test import Client, TestCase


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='francisc', password='a')

    def test_existent_user(self):
        response = self.client.login(username='francisc', password='a')
        self.assertEqual(response, True)
        self.client.logout()

    def test_nonexistent_user(self):
        response = self.client.login(username='bau', password='miau')
        self.assertEqual(response, False)
