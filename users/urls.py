from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('users/register', views.UserRegisterView.as_view()),
    path('users/login',obtain_auth_token),
    path('users/',views.AllUserView.as_view()),
    path('users/<int:id>/',views.UserView.as_view())
]