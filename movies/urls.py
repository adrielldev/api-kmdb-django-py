from django.urls import path
from . import views





urlpatterns = [
   path('movies/',views.MovieView.as_view()),
   path('movies/<int:id>/',views.MovieIdView.as_view()),
   path('movies/<int:id>/reviews/',views.MovieReviews.as_view()),
   path('movies/<int:id_movie>/reviews/<int:id_review>/',views.MovieIdReviews.as_view())
]