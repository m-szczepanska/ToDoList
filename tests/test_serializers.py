import json

from rest_framework import status
from django.test import TestCase, Client

from todoapp.models import User, Item
from todoapp.serializers import (GetUserSerializer,
CreateUserSerializer, ItemSerializer, UpdateUserSerializer)

from tests.fixtures import gen_user, gen_item

client = Client()
BASE_URL='http://127.0.0.1:8000'


class TestUserDetailsViews(TestCase):

    def test_user_password_ok(self):
        payload = {
            'username': 'mrpostman',
            'first_name': 'Mr',
            'last_name': 'Postman',
            'email': 'postman@test.email.com',
            'password': 'postmanpassword8',
            'password_repeat': 'postmanpassword8'
        }
        response = client.post(
            f'{BASE_URL}/users/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_json = response.json()
        # import pdb; pdb.set_trace()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_user_lack_of_digit_fail(self):
        payload = {
            'username': 'mrpostman',
            'first_name': 'Mr',
            'last_name': 'Postman',
            'email': 'postman@test.email.com',
            'password': 'postmanpassword',
            'password_repeat': 'postmanpassword'
        }
        response = client.post(
            f'{BASE_URL}/users/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_json = response.json()
        expected = {
            'non_field_errors': ['Password must contain at least 1 digit']
        }
        self.assertEqual(resp_json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_password_too_short_fail(self):
        payload = {
            'username': 'mrpostman',
            'first_name': 'Mr',
            'last_name': 'Postman',
            'email': 'postman@test.email.com',
            'password': 'pass',
            'password_repeat': 'pass'
        }
        response = client.post(
            f'{BASE_URL}/users/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_json = response.json()
        expected = {
            'non_field_errors': ['Passwords must have at least 8 characters']
        }
        self.assertEqual(resp_json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_passwords_doesnt_match_fail(self):
        payload = {
            'username': 'mrpostman',
            'first_name': 'Mr',
            'last_name': 'Postman',
            'email': 'postman@test.email.com',
            'password': 'password',
            'password_repeat': 'pass'
        }
        response = client.post(
            f'{BASE_URL}/users/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_json = response.json()
        expected = {
            'non_field_errors': ['Passwords did not match.']
        }
        self.assertEqual(resp_json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)