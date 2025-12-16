import pytest

from django.test.client import Client

from movies.models import Directors, Genres, Movies, Reviews


@pytest.fixture
def authorized_user(django_user_model):
    return django_user_model.objects.create(username='test_user')


@pytest.fixture
def authorized_user_client(authorized_user):
    client = Client()
    client.force_login(authorized_user)
    return client


@pytest.fixture
def movie():
    director = Directors.objects.create(first_name='d_first_name',
                                        last_name='d_last_name')
    genre = Genres.objects.create(genre='test_genre')
    movie = Movies.objects.create(title='test_title',
                                  release_date='2025-12-12',
                                  director=director)
    movie.genre.set([genre])
    return movie


@pytest.fixture
def review(admin_user, movie):
    return Reviews.objects.create(user=admin_user,
                                  text='review_text',
                                  movie=movie)
