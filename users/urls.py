from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from users.views import RegisterUserView, UserView

urlpatterns = [
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('register/', RegisterUserView.as_view(), name='auth_register'),
    path('', UserView.as_view(), name='User'),
]