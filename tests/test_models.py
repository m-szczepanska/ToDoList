from sys import exit
from django.contrib.auth.hashers import make_password
from django.test import TestCase

from todoapp.models import User


class TestUserModel(TestCase):

    def setUp(self):
        username = "Jdoe",
        first_name="Jon",
        last_name="Doe",
        email="email.email@false.com",
        password="P@ssw0rd!"

        self.user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        self.user.set_password(password)


    def test_check_password_correct_password(self):
        result = self.user.check_password("P@ssw0rd!")

        self.assertTrue(result)


    def test_check_password_wrong_password(self):
        result = self.user.check_password("password")

        self.assertFalse(result)


    def test_set_password(self):
        self.user.set_password("new_pass")
        result = self.user.check_password("new_pass")

        self.assertTrue(result)