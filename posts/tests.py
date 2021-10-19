import json, jwt, datetime
from time import time

from django.test import TestCase, Client


from .models import Post
from users.models import User

from my_settings import SECRET_KEY, ALGORITHM

class PostViewtest(TestCase):
    def setUp(self):
        User.objects.bulk_create(
            [
                User(
                    id=1,
                    name="muk1",
                    email="fall031@gmail.com",
                    password="anranr12!"
                ),
                User(
                    id=2,
                    name="muk2",
                    email="fall0833@gmail.com",
                    password="anranr12!@"
                )
            ]
        )
        self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        Post.objects.bulk_create(
            [
                Post(
                    id=1,
                    user=User.objects.get(id=1),
                    title="1번 글", 
                    username=User.objects.get(id=1).name,
                    content="1번 글 내용입니다",
                ),
                Post(
                    id=2,
                    user=User.objects.get(id=1),
                    title="2번 글", 
                    username=User.objects.get(id=1).name,
                    content="2번 글 내용입니다",
                ),
                Post(
                    id=3,
                    user=User.objects.get(id=1),
                    title="3번 글", 
                    username=User.objects.get(id=1).name,
                    content="3번 글 내용입니다",
                ),
                Post(
                    id=4,
                    user=User.objects.get(id=1),
                    title="4번 글", 
                    username=User.objects.get(id=1).name,
                    content="4번 글 내용입니다",
                ),
                Post(
                    id=5,
                    user=User.objects.get(id=1),
                    title="5번 글", 
                    username=User.objects.get(id=1).name,
                    content="5번 글 내용입니다",
                ),
                Post(
                    id=6,
                    user=User.objects.get(id=2),
                    title="6번 글", 
                    username=User.objects.get(id=2).name,
                    content="6번 글 내용입니다",
                ),
                Post(
                    id=7,
                    user=User.objects.get(id=2),
                    title="7번 글", 
                    username=User.objects.get(id=2).name,
                    content="7번 글 내용입니다",
                ),
                Post(
                    id=8,
                    user=User.objects.get(id=2),
                    title="8번 글", 
                    username=User.objects.get(id=2).name,
                    content="8번 글 내용입니다",
                ),
                Post(
                    id=9,
                    user=User.objects.get(id=2),
                    title="9번 글", 
                    username=User.objects.get(id=2).name,
                    content="9번 글 내용입니다",
                ),
                Post(
                    id=10,
                    user=User.objects.get(id=2),
                    title="10번 글", 
                    username=User.objects.get(id=2).name,
                    content="10번 글 내용입니다",
                )
            ]
        )

    def tearDown(self):
        Post.objects.all().delete()
        User.objects.all().delete()

    def test_create_post_success(self):
        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm=ALGORITHM)
        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        post = {
            "title": "11번 글",
            "username": User.objects.get(id=1).name,
            "content": "11번 글 내용입니다.",
            "created_at": self.time
        }
        response = client.post(
            "/posts", json.dumps(post), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "CREATE", 
        "data": {
            "title": "11번 글",
            "username": "muk1",
            "content": "11번 글 내용입니다.",
            "created_at": self.time
            }
        }
        )

    def test_create_key_error(self):
        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm=ALGORITHM)
        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        post = {
            "titleeee": "12번 글",
            "username": User.objects.get(id=1).name,
            "content": "12번 글 내용입니다.",
            "created_at": self.time
        }
        response = client.post(
            "/posts", json.dumps(post), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "KEY_ERROR"})

    def test_getlist_success(self):
        client = Client()
        response = client.get("/posts/list")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "count": 3,
                "Result": [
                    {
                        "username": "muk1",
                        "title": "1번 글",
                        "content": "1번 글 내용입니다",
                        "created_at": Post.objects.get(id=1).created_at.strftime('%Y-%m-%d %H:%M:%S')
                    },
                    {
                        "username": "muk1",
                        "title": "2번 글",
                        "content": "2번 글 내용입니다",
                        "created_at": Post.objects.get(id=2).created_at.strftime('%Y-%m-%d %H:%M:%S')
                    },
                    {
                        "username": "muk1",
                        "title": "3번 글",
                        "content": "3번 글 내용입니다",
                        "created_at": Post.objects.get(id=3).created_at.strftime('%Y-%m-%d %H:%M:%S')
                    }
                ]
            }
        )


    def test_get_success(self):
        client = Client()
        response = client.get("/posts/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "Result": {
                    "username": "muk1",
                    "title": "1번 글",
                    "content": "1번 글 내용입니다",
                    "created_at": Post.objects.get(id=1).created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        )

    def test_post_does_not_exist(self):
        client = Client()
        response = client.get("/posts/24")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "DOES_NOT_EXIST"})

    def test_edit_not_matched_user(self):
        access_token = jwt.encode({"id": 2}, SECRET_KEY, algorithm=ALGORITHM)
        client = Client()

        header = {"HTTP_AUTHORIZATION": access_token}
        post = {
            "post": "수정 내용입니다",
        }
        response = client.patch(
            "/posts/1", json.dumps(post), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "NOT_MATCHED_USER"})

    def test_post_edit_success(self):
        access_token = jwt.encode({"id": 1}, SECRET_KEY, algorithm=ALGORITHM)
        client = Client()

        header = {"HTTP_AUTHORIZATION": access_token}
        post = {
            "content": "수정 내용입니다",
        }
        response = client.patch(
            "/posts/1", json.dumps(post), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "SUCCESS"})

    def test_post_edit_key_error(self):
        access_token = jwt.encode({"id": 1}, SECRET_KEY, algorithm=ALGORITHM)
        client = Client()

        header = {"HTTP_AUTHORIZATION": access_token}
        post = {
            "text": "수정 내용입니다",
        }
        response = client.patch(
            "/posts/1", json.dumps(post), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "KEY_ERROR"})

    def test_post_edit_does_not_exist(self):
        access_token = jwt.encode({"id": 1}, SECRET_KEY, algorithm=ALGORITHM)
        client = Client()

        header = {"HTTP_AUTHORIZATION": access_token}
        post = {
            "content": "수정 내용입니다",
        }
        response = client.patch(
            "/posts/111", json.dumps(post), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "DOES_NOT_EXIST"})

    def test_post_delete_not_authorization_user(self):
        access_token = jwt.encode({"id": 2}, SECRET_KEY, algorithm=ALGORITHM)
        client = Client()

        header = {"HTTP_AUTHORIZATION": access_token}
        response = client.delete("/posts/1", **header)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"MESSAGE": "NOT_MATCHED_USER"})

    def test_post_delete_success(self):
        access_token = jwt.encode({"id": 1}, SECRET_KEY, algorithm=ALGORITHM)
        client = Client()

        header = {"HTTP_AUTHORIZATION": access_token}
        response = client.delete("/posts/1", **header)

        self.assertEqual(response.status_code, 204)

    def test_post_delete_does_not_exist(self):
        access_token = jwt.encode({"id": 1}, SECRET_KEY, algorithm=ALGORITHM)
        client = Client()

        header = {"HTTP_AUTHORIZATION": access_token}
        response = client.delete("/posts/100", **header)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "DOES_NOT_EXIST"})