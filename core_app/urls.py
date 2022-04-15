from django.urls import path
from .views import *

urlpatterns = [
    # Add User
    path('addUser/', AddUser.as_view(), name='addUser'),
    
    # View User
    path('viewUser/', ViewUser.as_view(), name='viewUser'),
    
    # Edit User
    path('editUser/', EditUser.as_view(), name='editUser'),

]
