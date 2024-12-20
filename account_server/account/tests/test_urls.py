from django.test import SimpleTestCase
from django.urls import reverse, resolve
from account.views import UserRegisterAPIView, UserLoginAPIView, UserAPIView, RecordAPIView

class TestUrls(SimpleTestCase):
    def test_signup_url_is_resolved(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func.view_class, UserRegisterAPIView)

    def test_signin_url_is_resolved(self):
        url = reverse('signin')
        self.assertEqual(resolve(url).func.view_class, UserLoginAPIView)

    def test_userinfo_url_is_resolved(self):
        url = reverse('userinfo')
        self.assertEqual(resolve(url).func.view_class, UserAPIView)

    def test_record_url_is_resolved(self):
        url = reverse('record')
        self.assertEqual(resolve(url).func.view_class, RecordAPIView)
