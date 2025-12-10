from rest_framework import viewsets
from django.contrib.auth import get_user_model

from movies.models import Genres, Directors, Movies, Reviews, Comments

from .mixins import StandartMixin
from .pagination import MovieAPIPagination
from .permissions import IsAuthorAuthenticatedOrReadOnly
from .serializers import (GenreSerializer,
                          DirectorSerializer,
                          MoviesSerializer,
                          ReviewsSerializer,
                          CommentsSerializer,
                          UserSerializer)


class GenreViewset(StandartMixin):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer


class DirectorsViewset(StandartMixin):
    queryset = Directors.objects.all()
    serializer_class = DirectorSerializer


class MoviesViewset(viewsets.ModelViewSet):
    queryset = Movies.objects.all()
    serializer_class = MoviesSerializer
    pagination_class = MovieAPIPagination


class ReviewsViewset(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthorAuthenticatedOrReadOnly, )


class CommentsViewset(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class UsersViewset(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
