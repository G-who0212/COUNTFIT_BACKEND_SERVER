from django.test import TestCase
from account.models import User, Record

class TestUserModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            nickname="testuser",
            gender="male",
            age=25
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertTrue(self.user.check_password("password123"))

    def test_user_str(self):
        self.assertEqual(str(self.user), "testuser")

class TestRecordModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            nickname="testuser"
        )
        self.record = Record.objects.create(
            sport_type="running",
            aim_count=10,
            done_count=7,
            done_at="2023-01-01 00:00:00",
            user=self.user
        )

    def test_record_creation(self):
        self.assertEqual(self.record.sport_type, "running")
        self.assertEqual(self.record.user, self.user)
