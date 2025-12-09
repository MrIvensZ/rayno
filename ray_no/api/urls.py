from django.urls import include, path

from rest_framework import routers

from . import views

app_name = 'api'


router = routers.DefaultRouter()

router.register('genres', views.GenreViewset, basename='genre')
router.register('directors', views.DirectorsViewset, basename='director')
router.register('movies', views.MoviesViewset, basename='movie')
router.register('reviews', views.ReviewsViewset, basename='review')
router.register('comments', views.CommentsViewset, basename='comment')
router.register('users', views.UsersViewset, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
