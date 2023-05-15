from django.urls import path
from movies.views import *

urlpatterns = [
    path("movies/", MovieRegisterView.as_view()),
    path("movies/<int:movie_id>/", MovieDetailView.as_view()),
    path("movies/<int:movie_id>/orders/", MovieOrderView.as_view())
]