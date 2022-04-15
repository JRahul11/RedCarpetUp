from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from core_app.views import Welcome

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),

    # Base URL
    path('', Welcome.as_view()),

    # Auth URLs
    path('auth/', include('auth_app.urls')),

    # Core URLs
    path('api/', include('core_app.urls')),
]
