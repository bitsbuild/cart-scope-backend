from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
class UserTesting(APITestCase):
    def setUp(self):
        pass
    def test_create_user_success(self):
        data = {
            "username":"bitsbuild",
            "password":"password",
            "email":"email@email.com",
            "confirm_password":"password"
        }
        response = self.client.post(reverse('create'),data)
        self.assertEqual(response.status_code,HTTP_200_OK)
    def test_create_user_failure_passwords_not_matching(self):
        pass
    def test_create_user_failure_username_exists(self):
        pass
    def test_create_user_failure_account_with_email_exists(self):
        pass
    def test_create_user_failure_invalid_email_format(self):
        pass
    def test_get_token_success(self):
        pass
    def test_get_token_failure(self):
        pass
    def test_delete_user_success(self):
        pass
    def test_delete_user_failure(self):
        pass