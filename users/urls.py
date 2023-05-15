from django.urls import path
from users.views import *
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("users/", views.RegisterView.as_view()),
    path("users/login/", TokenObtainPairView.as_view()),
    path("token/refresh/",TokenRefreshView.as_view()),
    path("users/<int:user_id>/", UserDetailsView.as_view())
]