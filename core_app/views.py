from django.contrib.auth.hashers import make_password
from auth_app.groups import CustomGroups
from auth_app.serializer import SignUpSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from core_app.models import User
from .serializer import *


class Welcome(APIView):
    def get(self, request):
        return Response('Welcome to RedCarpetUp APIs by Rahul Jadhav')



class AddUser(APIView):
    
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication


    # Create User Record if doesnt exist
    def createNewUser(self, username, password, user_type, name=None, state=None, income_from_salary=None, income_from_shares=None, tax_status=None):
        try:                                                                                # Check if user already exists
            User.objects.get(username=username)
            return 'User Exists', 500
        except:                                                                             # Create a new user if doesnt exist
            new_user = User.objects.create_user(username=username, password=make_password(password), user_type=user_type, name=name, state=state, income_from_salary=income_from_salary, income_from_shares=income_from_shares, tax_status=tax_status)
            CustomGroups.addUserToGroup(self, new_user, user_type)
            return 'User Added', 200


    def post(self, request):
        username = request.user
        user = User.objects.get(username=username)                                          # Get the user record
        
        if user.groups.filter(name='SuperUser'):                                            # Check if user is a SuperUser
            data = request.data  
            if request.data['user_type'] == 1:
                addUserSerializer = ValidateSerializer(data=data)
                if addUserSerializer.is_valid():
                    username = addUserSerializer.data['username']
                    password = addUserSerializer.data['password']
                    user_type = addUserSerializer.data['user_type']
                    name = addUserSerializer.data['name']
                    state = addUserSerializer.data['state']
                    income_from_salary = addUserSerializer.data['income_from_salary']
                    income_from_shares = addUserSerializer.data['income_from_shares']
                    tax_status = addUserSerializer.data['tax_status']
                    status, status_code = self.createNewUser(username, password, user_type, name, state, income_from_salary, income_from_shares, tax_status)
                    return Response(
                        {
                            'status': status,
                        },
                        status = status_code
                    )
                else:
                    return Response(                                                    # Error if user data is invalid
                        {
                            'status': 'Error',
                            'message': addUserSerializer.errors
                        },
                        status = 500
                    )
            else:
                addUserSerializer = SignUpSerializer(data=data)                                 # Data Validation using Serializer
                if addUserSerializer.is_valid():
                    username = addUserSerializer.data['username']
                    password = addUserSerializer.data['password']
                    user_type = addUserSerializer.data['user_type']
                    status, status_code = self.createNewUser(username, password, user_type)                  # Call createNewUser for new user check
                    return Response(
                        {
                            'status': status,
                        },
                        status = status_code
                    )

        elif user.groups.filter(name='TaxAccountant'):                                      # Check if user is a Teacher
            data = request.data                                                             # Get the data from the request
            if request.data['user_type'] == 1:
                addUserSerializer = ValidateSerializer(data=data)                                 # Data Validation using Serializer
                if addUserSerializer.is_valid():
                    username = addUserSerializer.data['username']
                    password = addUserSerializer.data['password']
                    user_type = addUserSerializer.data['user_type']
                    name = addUserSerializer.data['name']
                    state = addUserSerializer.data['state']
                    income_from_salary = addUserSerializer.data['income_from_salary']
                    income_from_shares = addUserSerializer.data['income_from_shares']
                    tax_status = addUserSerializer.data['tax_status']
                    status, status_code = self.createNewUser(username, password, user_type, name, state, income_from_salary, income_from_shares, tax_status)
                    return Response(
                        {
                            'status': status,
                        },
                        status = status_code
                    )
                else:
                    return Response(                                                    # Error if user data is invalid
                        {
                            'status': 'Error',
                            'message': addUserSerializer.errors
                        },
                        status = 500
                    )
            else:
                return Response(                                                        # Error if new user is SuperUser or TaxAccountant
                    {
                        'status': 'Error',
                        'message': 'Insufficient Permissions to perform the request'
                    },
                    status = 500
                )

        elif user.groups.filter(name='TaxPayer'):                                          # Check if user is a TaxPayer
            return Response(
                {                                                                           # Error because TaxPayer cannot add Users
                    'status': 'Error',
                    'message': 'Insufficient Permissions to perform the request'
                },
                status = 500
            )



# View User Class
class ViewUser(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication


    def createUserJSON(self, user):                                                               # Create a JSON for the user data
        if user.user_type == 1:
            user_type = 'Tax Payer'
            return {
                'id': user.id,
                'username': user.username,
                'user_type': user_type,
                'name': user.name,
                'state': user.state,
                'income_from_salary': user.income_from_salary,
                'income_from_shares': user.income_from_shares,
                'tax_status': user.tax_status,
            }
        elif user.user_type == 2:
            user_type = 'Tax Accountant'
            return {
                'id': user.id,
                'username': user.username,
                'user_type': user_type
            }
        elif user.user_type == 3:
            user_type = 'SuperUser'
            return {
                'id': user.id,
                'username': user.username,
                'user_type': user_type
            }


    # GET Request
    def get(self, request):
        response = []                                                                       # Create a list to store the user data
        username = request.user                                                             # Get the user from the request
        user = User.objects.get(username=username)                                          # Get the user record

        if user.groups.filter(name='SuperUser'):                                            # Check if user is a SuperUser
            users = User.objects.all()                                                      # SuperUser can view all the Users
            for user in users:
                response.append(self.createUserJSON(user))                                  # Append the user JSON to the list
            return Response(response)
        elif user.groups.filter(name='TaxAccountant'):                                      # Check if user is a TaxAccountant
            users = User.objects.filter(user_type=1)                                        # TaxAccountant can view all the TaxPayers
            for user in users:
                response.append(self.createUserJSON(user))                                  # Append the user JSON to the list
            return Response(response)
        elif user.groups.filter(name='TaxPayer'):                                           # Check if user is a TaxPayer
            response.append(self.createUserJSON(user))                                      # Append the user JSON to the list
            return Response(response)



class EditUser(APIView):
    
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def updateUser(self, username, password, user_type, name=None, state=None, income_from_salary=None, income_from_shares=None, tax_status=None):
        try:                                                                                # Check if user already exists and edit
            user = User.objects.get(username=username)
            user.groups.clear()
            user.password = make_password(password)
            user.user_type = user_type
            user.name = name
            user.state = state
            user.income_from_salary = income_from_salary
            user.income_from_shares = income_from_shares
            user.tax_status = tax_status
            user.save(update_fields=['password', 'user_type', 'name', 'state', 'income_from_salary', 'income_from_shares', 'tax_status'])
            CustomGroups.addUserToGroup(self, user, user_type)                              # Update User's Group
            return 'User Updated', 200
        except:                                                                             # Error if user doesnt exist
            return 'User Does Not Exists', 500

    def post(self, request):
        username = request.user
        user = User.objects.get(username=username)                                          # Get the user record
        
        if user.groups.filter(name='SuperUser'):                                            # Check if user is a SuperUser
            data = request.data  
            if request.data['user_type'] == 1:
                editUserSerializer = ValidateSerializer(data=data)
                if editUserSerializer.is_valid():
                    username = editUserSerializer.data['username']
                    password = editUserSerializer.data['password']
                    user_type = editUserSerializer.data['user_type']
                    name = editUserSerializer.data['name']
                    state = editUserSerializer.data['state']
                    income_from_salary = editUserSerializer.data['income_from_salary']
                    income_from_shares = editUserSerializer.data['income_from_shares']
                    tax_status = editUserSerializer.data['tax_status']
                    status, status_code = self.updateUser(username, password, user_type, name, state, income_from_salary, income_from_shares, tax_status)
                    return Response(
                        {
                            'status': status,
                        },
                        status = status_code
                    )
                else:
                    return Response(                                                    # Error if user data is invalid
                        {
                            'status': 'Error',
                            'message': editUserSerializer.errors
                        },
                        status = 500
                    )
            else:
                editUserSerializer = SignUpSerializer(data=data)                                 # Data Validation using Serializer
                if editUserSerializer.is_valid():
                    username = editUserSerializer.data['username']
                    password = editUserSerializer.data['password']
                    user_type = editUserSerializer.data['user_type']
                    status, status_code = self.updateUser(username, password, user_type)                  # Call createNewUser for new user check
                    return Response(
                        {
                            'status': status,
                        },
                        status = status_code
                    )

        elif user.groups.filter(name='TaxAccountant'):                                      # Check if user is a Teacher
            data = request.data                                                             # Get the data from the request
            if request.data['user_type'] == 1:
                editUserSerializer = ValidateSerializer(data=data)                                 # Data Validation using Serializer
                if editUserSerializer.is_valid():
                    username = editUserSerializer.data['username']
                    password = editUserSerializer.data['password']
                    user_type = editUserSerializer.data['user_type']
                    name = editUserSerializer.data['name']
                    state = editUserSerializer.data['state']
                    income_from_salary = editUserSerializer.data['income_from_salary']
                    income_from_shares = editUserSerializer.data['income_from_shares']
                    tax_status = editUserSerializer.data['tax_status']
                    status, status_code = self.updateUser(username, password, user_type, name, state, income_from_salary, income_from_shares, tax_status)
                    return Response(
                        {
                            'status': status,
                        },
                        status = status_code
                    )
                else:
                    return Response(                                                    # Error if user data is invalid
                        {
                            'status': 'Error',
                            'message': editUserSerializer.errors
                        },
                        status = 500
                    )
            else:
                return Response(                                                        # Error if new user is SuperUser or TaxAccountant
                    {
                        'status': 'Error',
                        'message': 'Insufficient Permissions to perform the request'
                    },
                    status = 500
                )

        elif user.groups.filter(name='TaxPayer'):                                          # Check if user is a TaxPayer
            return Response(
                {                                                                           # Error because TaxPayer cannot add Users
                    'status': 'Error',
                    'message': 'Insufficient Permissions to perform the request'
                },
                status = 500
            )
