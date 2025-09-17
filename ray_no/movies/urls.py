from django.urls import path

from . import views

app_name = 'movies'


urlpatterns = [
    path('', views.movie_list, name='list'),
    path('create', views.movie_create, name='create'),
    path('<int:movie_id>', views.movie_detail, name='detail')
]
