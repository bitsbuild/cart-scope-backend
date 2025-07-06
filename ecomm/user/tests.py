from django.urls import reverse
from rest_framework.test import APITestCase
class UserTesting(APITestCase):
    def setUp(self):
        pass
    def test_create_user_success(self):
        pass
    def test_create_user_failure_passwords_not_matching(self):
        pass
    def test_create_user_failure_username_exists(self):
        pass
    def test_create_user_failure_account_with_email_exists(self):
        pass
    def test_get_token_success(self):
        pass
    def test_get_token_failure(self):
        pass
    def delete_user_success(self):
        pass
    def delete_user_failure(self):
        pass