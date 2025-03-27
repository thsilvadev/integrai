from django.urls import path
from .views import register_user, check_user

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('check/', check_user, name='check_user'),
]
