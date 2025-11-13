from django.urls import path

from . import views

app_name = 'movies'


urlpatterns = [
    path('', views.MovieListView.as_view(), name='movie_list'),
    path('create', views.MovieCreateView.as_view(), name='create'),
    path('<int:movie_id>', views.movie_detail, name='movie_detail'),
    path('<int:movie_id>/add_review', views.review_add, name='add_review'),
    path('<int:movie_id>/reviews', views.review_list, name='reviews_list'),
    path('<int:movie_id>/reviews/<int:review_id>',
         views.review_detail,
         name='review_detail'),
]
