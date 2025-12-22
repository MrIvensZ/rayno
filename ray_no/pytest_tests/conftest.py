import datetime
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
def director():
    director = Directors.objects.create(first_name='d_first_name',
                                        last_name='d_last_name')
    return director


@pytest.fixture
def genre():
    genre = Genres.objects.create(genre='test_genre')
    return genre


@pytest.fixture
def movie(director, genre):
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


@pytest.fixture
def pk_for_movie(movie):
    return {'movie_id': movie.pk}


@pytest.fixture
def pk_for_movie_and_review(movie, review):
    return {'movie_id': movie.pk, 'review_id': review.pk}


@pytest.fixture
def movie_form_data(director, genre):
    return {
        'title': 'test_title2',
        'release_date': datetime.date(1998, 6, 23),
        'director': director.id,
        'genre': [genre.id,]
    }


@pytest.fixture
def rating_form_data(movie):
    return {
        'movie': movie.id,
        'rate': 5
    }


@pytest.fixture
def wrong_rating_form_data(movie):
    return {
        'movie': movie.id,
        'rate': 11
    }


@pytest.fixture
def review_form_data(movie):
    return {
        'movie': movie.id,
        'text': 'Test review text'
    }


@pytest.fixture
def comment_form_data(review):
    return {
        'review': review.id,
        'text': 'Test comment text'
    }
