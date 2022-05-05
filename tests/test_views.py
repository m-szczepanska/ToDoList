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

    def setUp(self):
        self.users = [
            gen_user(),
            gen_user(
                username="JKowalski",
                first_name="Jan",
                last_name="Kowalski",
                email="j@bkowalski.test.com",
                password="P@ssw0rd1"
            )
        ]

    def test_user_ok(self):
        response = client.get(
            f'{BASE_URL}/users/{self.users[0].id}')
        expected = GetUserSerializer(self.users[0]).data

        self.assertEqual(response.json(), expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_404(self):
        response = client.get(f'{BASE_URL}/users/299')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_delete_ok(self):
        response = client.delete(
            f'{BASE_URL}/users/{self.users[0].id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_put_ok(self):
        payload = {
            'first_name': 'Nowe',
            'last_name': 'Imie',
            'email': "nowe.imie@email.com"
        }
        response = client.put(
            f'{BASE_URL}/users/{self.users[1].id}',
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_json = response.json()

        self.assertEqual(resp_json['first_name'], payload['first_name'])
        self.assertEqual(resp_json['last_name'], payload['last_name'])
        self.assertEqual(resp_json['email'], payload['email'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_put_400_for_empy_field(self):
        payload = {
            'first_name': '',
            'last_name': 'Imie',
            'email': "nowe.imie@email.com"
        }
        response = client.put(
            f'{BASE_URL}/users/{self.users[1].id}',
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_json = response.json()
        with self.assertRaises(AssertionError):
            self.assertEqual(resp_json['first_name'], payload['first_name'])

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUserListViews(TestCase):

    def setUp(self):
        self.users = [
            gen_user(),
            gen_user(
                username="JKowalski",
                first_name="Jan",
                last_name="Kowalski",
                email="j@bkowalski.test.com",
                password="P@ssw0rd1"
            )
        ]


    def test_users_list_ok(self):
        response = client.get(f'{BASE_URL}/users/')
        expected = GetUserSerializer(self.users, many=True).data

        self.assertEqual(response.json(), expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_users_post_ok(self):
        payload = {
            'username': 'Mrpostman',
            'first_name': 'Mr',
            'last_name': 'Postman',
            'email': 'postman@test.email.com',
            'password': 'postmanpassword1',
            'password_repeat': 'postmanpassword1'
        }
        response = client.post(
            f'{BASE_URL}/users/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_json = response.json()

        self.assertEqual(resp_json['username'], payload['username'])
        self.assertEqual(resp_json['first_name'], payload['first_name'])
        self.assertEqual(resp_json['last_name'], payload['last_name'])
        self.assertEqual(resp_json['email'], payload['email'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_users_post_empty_field(self):
        payload = {
            'username': '',
            'first_name': 'Mr',
            'last_name': 'Postman',
            'email': 'postman@test.email.com',
            'password': 'postmanpassword1',
            'password_repeat': 'postmanpassword1'
        }
        response = client.post(
            f'{BASE_URL}/users/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_json = response.json()

        expected = {
            'username': ['This field may not be blank.']}
        self.assertEqual(response.json(), expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_post_duplicate_email(self):
        user_dicts = [
            {
                'username': 'Mrpostman',
                'first_name': 'Mr',
                'last_name': 'Postman',
                'email': 'thesame@email.test.com',
                'password': 'postmanpassword1',
                'password_repeat': 'postmanpassword1'
            },
            {
                'username': 'Jsmith',
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'thesame@email.test.com',
                'password': 'postmanpassword1',
                'password_repeat': 'postmanpassword1'
            }
        ]
        for elem in user_dicts:
            response = client.post(
                f'{BASE_URL}/users/',
                data=json.dumps(elem),
                content_type='application/json')
        expected = {
            'non_field_errors': ['User with this email already exists.']}

        self.assertEqual(response.json(), expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_post_duplicate_username(self):
        user_dicts = [
            {
                'username': 'thesameusername',
                'first_name': 'Mr',
                'last_name': 'Postman',
                'email': 'thesame@email.test.com',
                'password': 'postmanpassword1',
                'password_repeat': 'postmanpassword1'
            },
            {
                'username': 'thesameusername',
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'other@email.test.com',
                'password': 'postmanpassword1',
                'password_repeat': 'postmanpassword1'
            }
        ]
        for elem in user_dicts:
            response = client.post(
                f'{BASE_URL}/users/',
                data=json.dumps(elem),
                content_type='application/json')
        expected = {
            'non_field_errors': ['User with this username already exists.']}

        self.assertEqual(response.json(), expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestItemDetailsViews(TestCase):

    def setUp(self):
        self.users = [
            gen_user(),
            gen_user(
                username="JKowalski",
                first_name="Jan",
                last_name="Kowalski",
                email="j@bkowalski.test.com",
                password="P@ssw0rd1"
            )
        ]
        self.items = [
            gen_item(),
            gen_item(
                title="remove bug from endpoint",
                text="create root cause analysis and remove bug from endpoint",
                status="in progress",
                category="bug",
                due_date="2022-05-08T00:00:00Z",
                owner_id=2,
                creator_id=1
            )
        ]


    def test_item_ok(self):
        response = client.get(
            f'{BASE_URL}/items/{self.items[0].id}')
        expected = ItemSerializer(self.items[0]).data

        self.assertEqual(response.json(), expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_item_404(self):
        response = client.get(f'{BASE_URL}/items/299')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_item_delete_ok(self):
        response = client.delete(
            f'{BASE_URL}/items/{self.items[0].id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_item_put_ok(self):
        payload = {
            "title": "create new endpoint",
            "text": "add new endpoint to the app",
            "status": "in progress",
            "category": "task",
            "due_date": "2022-05-06T00:00:00Z",
            "owner_id": 1,
            "creator_id": 1
        }
        response = client.put(
            f'{BASE_URL}/item_update/{self.items[0].id}/{self.users[0].id}',
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_json = response.json()

        self.assertEqual(resp_json['title'], payload['title'])
        self.assertEqual(resp_json['text'], payload['text'])
        self.assertEqual(resp_json['status'], payload['status'])
        self.assertEqual(resp_json['category'], payload['category'])
        self.assertEqual(resp_json['due_date'], payload['due_date'])
        self.assertEqual(resp_json['owner_id'], payload['owner_id'])
        self.assertEqual(resp_json['creator_id'], payload['creator_id'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_item_put_400_for_empy_field(self):
        payload = {
            "title": "create new endpoint",
            "text": "add new endpoint to the app",
            "status": "",
            "category": "task",
            "due_date": "2022-05-06T00:00:00Z",
            "owner_id": 1,
            "creator_id": 1
        }
        response = client.put(
            f'{BASE_URL}/item_update/{self.items[0].id}/{self.users[0].id}',
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_json = response.json()
        with self.assertRaises(AssertionError):
            self.assertEqual(resp_json["status"], payload["status"])

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestItemListViews(TestCase):

    def setUp(self):
        self.users = [
            gen_user(),
            gen_user(
                username="JKowalski",
                first_name="Jan",
                last_name="Kowalski",
                email="j@bkowalski.test.com",
                password="P@ssw0rd1"
            )
        ]
        self.items = [
            gen_item(),
            gen_item(
                title="remove bug from endpoint",
                text="create root cause analysis and remove bug from endpoint",
                status="in progress",
                category="bug",
                due_date="2022-05-08T00:00:00Z",
                owner_id=2,
                creator_id=1
            )
        ]


    def test_items_list_ok(self):
        response = client.get(f'{BASE_URL}/items/')
        expected = ItemSerializer(self.items, many=True).data

        self.assertEqual(response.json(), expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_items_post_ok(self):
        payload = {
            'title': 'new task',
            'text': 'description',
            'status': 'blocked',
            'category': 'new feature',
            'due_date': '2022-05-08T00:00:00Z',
        }
        # import pdb; pdb.set_trace()
        response = client.post(
            f'{BASE_URL}/item_create/2',
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_json = response.json()
        self.assertEqual(resp_json['title'], payload['title'])
        self.assertEqual(resp_json['text'], payload['text'])
        self.assertEqual(resp_json['status'], payload['status'])
        self.assertEqual(resp_json['category'], payload['category'])
        self.assertEqual(resp_json['due_date'], payload['due_date'])
        self.assertEqual(resp_json['creator_id'], 2)
        self.assertEqual(resp_json['owner_id'], 2)


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_items_post_empty_field(self):
        payload = {
            'title': '',
            'text': 'description',
            'status': 'blocked',
            'category': 'new feature',
            'due_date': '2022-05-08T00:00:00Z',
        }
        response = client.post(
            f'{BASE_URL}/item_create/1',
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_json = response.json()

        expected = {
            'title': ['This field may not be blank.']}
        self.assertEqual(response.json(), expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
