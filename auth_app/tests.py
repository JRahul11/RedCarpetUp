from rest_framework import status
from rest_framework.test import APITestCase
from core_app.models import User



class SignUpTestCase(APITestCase):

    def test_taxpayer(self):                                                        # TaxPayer SignUp Test
        data = {
            "username": "taxpayer_username",
            "password": "taxpayer_password",
            "user_type": 1
        }
        response = self.client.post("/auth/signup/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_taxaccountant(self):                                                   # TaxAccountant SignUp Test
        data = {
            "username": "accountant_username",
            "password": "accountant_password",
            "user_type": 2
        }
        response = self.client.post("/auth/signup/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_superuser(self):                                                                   
        data = {
            "username": "superuser_username_exceeding_20_characters",               # Too long username for SuperUser/Admin
            "password": "superuser_password",
            "user_type": 3
        }
        response = self.client.post("/auth/signup/", data)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)



class LoginTestCase(APITestCase):

    def test_superuser(self):                                                       # SuperUser Login Test
        User.objects.create_user(
            username = 'superuser_username', 
            password = 'superuser_password', 
            user_type = 3
        )
        data = {
            "username": "superuser_username",
            "password": "superuser_password"
        }
        response = self.client.post("/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_taxpayer(self):                                                        # TaxPayer Wrong Credentials Test
        data = {
            "username": "taxpayer_username",
            "password": "taxpayer_password"
        }
        response = self.client.post("/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)