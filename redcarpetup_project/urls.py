from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),
    
    # Auth URLs
    path('auth/', include('auth_app.urls')),
    
    # Core URLs
    path('api/', include('core_app.urls')),
]
