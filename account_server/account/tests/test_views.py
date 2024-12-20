from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from account.models import Record

User = get_user_model()

class TestUserRegisterAPIView(APITestCase):
    def test_register_user(self):
        data = {
            "email": "testuser@example.com",
            "password": "password123",
            "password2": "password123",
            "nickname": "testuser",
            "gender": "male",
            "age": 25
        }
        response = self.client.post('/account/signup/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

class TestUserLoginAPIView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            nickname="testuser"
        )

    def test_login_user(self):
        data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = self.client.post('/account/signin/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

class TestUserAPIView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            nickname="testuser"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_user_info(self):
        response = self.client.get('/account/userinfo/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nickname"], "testuser")

    def test_update_user_info(self):
        data = {"nickname": "updateduser"}
        response = self.client.post('/account/userinfo/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nickname"], "updateduser")

    def test_delete_user(self):
        response = self.client.delete('/account/userinfo/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

class TestRecordAPIView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            nickname="testuser"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_record(self):
        data = {
            "sport_type": "running",
            "aim_count": 10,
            "done_count": 7
        }
        response = self.client.post('/account/record/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Record.objects.count(), 1)

    def test_create_record_missing_data(self):
        data = {
            "sport_type": "running",
            "aim_count": 10
        }
        response = self.client.post('/account/record/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
