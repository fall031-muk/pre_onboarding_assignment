import json
from unittest.mock import MagicMock, patch

from django.test import TestCase, Client

from .models import User


class SignUpTest(TestCase):
    def test_signup_success(self):
        client = Client()
        user = {
            "name": "muk5",
            "email": "fall035@gmail.com",
            "password": "anranr12!",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "SUCCESS"})

    def test_signupview_invalid_email(self):
        client = Client()
        user = {
            "name": "muk1",
            "email": "fall031gmail.com",
            "password": "anranr12!",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "EMAIL_VALIDATION_ERROR"})

    def test_signupview_invalid_password(self):
        client = Client()
        user = {
            "name": "muk3",
            "email": "fall033@gmail.com",
            "password": "anranr12",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "PASSWORD_VALIDATION_ERROR"})

    def setUp(self):
        User.objects.bulk_create(
            [
                User(
                    id=1,
                    name="muk1",
                    email="fall031@gmail.com",
                    password="anranr12!",
                ),
                User(
                    id=2,
                    name="muk2",
                    email="fall0833@gmail.com",
                    password="anranr12!@"
                )
            ]
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signupview_duplication(self):
        client = Client()
        user = {
            "name": "muk1",
            "email": "fall031@gmail.com",
            "password": "anranr12!",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "DUPLICATION_ERROR"})


class LoginTest(TestCase):
    def setUp(self):
        User.objects.bulk_create(
            [
                User(
                    id=1,
                    name="muk1",
                    email="fall031@gmail.com",
                    password="$2b$12$CprmtyKq69jdx0.U2kRMfuH71NLeSB.KCwRIvKlzMIVN52w/Rmttm",
                ),

            ]
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch("requests.post")
    def test_login_success(self, mocked_requests):
        user = {
            "email": "fall031@gmail.com",
            "password": "anranr12!",
        }
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "MESSAGE": "SUCCESS",
                    "ACCESS_TOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.fPMiZfFe-_HeHaOUWvBUgsKJQVWvmFyOA2LCi1VJFz8"
                }

        mocked_requests.post = MagicMock(return_value=MockedResponse())
        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        
    def test_logninview_not_exist_user(self):
        client = Client()
        user = {
            "email": "fall033@gmail.com",
            "password": "anranr12!@#",
        }
        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"MESSAGE": "DOES_NOT_EXIST"})

    def test_logninview_invalid_password(self):
        client = Client()
        user = {
            "email": "fall031@gmail.com",
            "password": "anranr12@@",
        }
        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"MESSAGE": "INVALID_PASSWORD"})