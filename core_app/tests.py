from .models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from auth_app.groups import CustomGroups



class AddUserTestCase(APITestCase):
    
    def setUp(self):
        CustomGroups.createAdminGroup(self)
        CustomGroups.createTaxAccountantGroup(self)
        CustomGroups.createTaxPayerGroup(self)

    def test_addTaxAccountantAsSuperuser(self):                                                                           # Admin can add a Tax Accountant
        self.setUp()
        user=User.objects.create_user(username='SuperUser', password='SuperUser', user_type=3)                      
        CustomGroups.addUserToGroup(self, user, 3)
        access=str(RefreshToken.for_user(user).access_token)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        data={
            "username": "taxpayer_username",
            "password": "taxpayer_password",
            "user_type": 2
        }
        response=self.client.post("/api/addUser/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_addSuperuserAsTaxPayer(self):                                                                                # Tax Payer cannot add a SuperUser
        self.setUp()
        user=User.objects.create_user(username='TaxPayer', password='TaxPayer', user_type=1)
        CustomGroups.addUserToGroup(self, user, 1)
        access=str(RefreshToken.for_user(user).access_token)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        data={
            "username": "admin_username",
            "password": "admin_password",
            "user_type": 3
        }
        response=self.client.post("/api/addUser/", data)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)



class ViewUserTestCase(APITestCase):
    
    def setUp(self):
        CustomGroups.createAdminGroup(self)
        CustomGroups.createTaxAccountantGroup(self)
        CustomGroups.createTaxPayerGroup(self)

    def test_viewAsTaxAccountant(self):                                                                           # Tax Accountant can view all Tax Payers
        self.setUp()
        user=User.objects.create_user(username='TaxAccountant', password='TaxAccountant', user_type=2)                      
        CustomGroups.addUserToGroup(self, user, 2)
        access=str(RefreshToken.for_user(user).access_token)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response=self.client.get("/api/viewUser/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class EditUserTestCase(APITestCase):
    
    def setUp(self):
        CustomGroups.createAdminGroup(self)
        CustomGroups.createTaxAccountantGroup(self)
        CustomGroups.createTaxPayerGroup(self)
    
    def test_editTaxAccountantAsTaxPayer(self):                                                                   # Tax Payer cannot edit a Tax Accountant
        self.setUp()
        user = User.objects.create_user(username='TaxPayer', password='TaxPayerPass', user_type=1)
        CustomGroups.addUserToGroup(self, user, 1)
        access=str(RefreshToken.for_user(user).access_token)
        taxAccountant=User.objects.create_user(username='TaxAccountant', password='TaxAccountantPass', user_type=2)
        CustomGroups.addUserToGroup(self, taxAccountant, 2)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        data={
            "username": "TaxAccountant",
            "password": "TaxAccountantPass",
            "user_type": 3,
        }
        response=self.client.post("/api/editUser/", data)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)