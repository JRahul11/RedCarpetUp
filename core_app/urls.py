from django.urls import path
from .views import *

urlpatterns = [
    # Add User
    path('addUser/', AddUser.as_view()),
    
    # View User
    path('viewUser/', ViewUser.as_view()),
    
    # Edit User
    path('editUser/', EditUser.as_view()),

]
