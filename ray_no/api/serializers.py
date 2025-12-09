from rest_framework import serializers

from django.contrib.auth import get_user_model

from movies.models import Genres, Directors, Movies, Rating, Reviews, Comments


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('id', 'genre')


class DirectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Directors
        fields = ('id', 'first_name', 'last_name')
        read_only_fields = ('full_name',)


class MoviesSerializer(serializers.ModelSerializer):

    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Movies
        fields = ('id',
                  'title',
                  'director',
                  'release_date',
                  'genre',
                  'poster',
                  'url')


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('user', 'movie', 'rate')


class ReviewsSerializer(serializers.ModelSerializer):

    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Reviews
        fields = ('id', 'user', 'text', 'movie', 'time_create', 'url')


class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ('id', 'user', 'text', 'review', 'time_create')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'date_joined',
                  'about_user',
                  'sex',
                  'avatar')
