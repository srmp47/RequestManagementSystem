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

from comments.views import CommentListCreateView, CommentRetrieveUpdateDestroyView
from tickets.views import TicketRetrieveUpdateDestroyView, TicketListCreateView
from users import views as users_view
from advertisements import views as advertisements_view
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

import users.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('user/login', users_view.LoginView.as_view(), name='login'),
    path('user/register', users_view.RegisterView.as_view(), name='register'),
    path('user/profile/', users_view.UserProfileView.as_view(), name='user-profile'),
    path('advertisement/', advertisements_view.RequestListCreateView.as_view(), name='ad-list-create'),

    path('advertisement/<int:pk>/', advertisements_view.RequestRetrieveUpdateDeleteView.as_view(), name='ad-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),

    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-detail'),
    path('tickets/', TicketListCreateView.as_view(), name='ticket-list-create'),

    path('tickets/<int:pk>/', TicketRetrieveUpdateDestroyView.as_view(), name='ticket-detail'),
]
