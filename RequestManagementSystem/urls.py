"""
URL configuration for RequestManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from users import views as users_view
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

import users.views

urlpatterns = [
    path('admin/', admin.site.urls),
    # The actual schema (the JSON/YAML file)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # The UI (Swagger)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Optional: Redoc UI (an alternative to Swagger)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('user/login', users_view.LoginView.as_view(), name='login'),
    path('user/register', users_view.RegisterView.as_view(), name='register'),
    path('advertisement/create', users_view.LoginView.as_view(), name='login'),
]
