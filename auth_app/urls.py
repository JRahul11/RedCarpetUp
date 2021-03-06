from django.urls import path

# Import JWT Inbuilt Classes
from rest_framework_simplejwt.views import (TokenRefreshView)
from .views import *

urlpatterns = [
    
    # Authentication URLs
    path('login/', LoginView.as_view(), name='login'),                            # Login API
    path('signup/', SignUpView.as_view(), name='signup'),                          # SignUp API
    
    # JWT URLs
    path('tokenRefresh/', TokenRefreshView.as_view()),             # Refresh JWT Token  
]
