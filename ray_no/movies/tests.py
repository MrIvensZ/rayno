from http import HTTPStatus

from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Directors, Genres, Movies
from .forms import MovieForm

User = get_user_model()


class TestMovies(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.authorized_user = User.objects.create(username='a_user')
        cls.not_authorized_user = User.objects.create(username='na_user')
        cls.director = Directors.objects.create(first_name='Name',
                                                last_name='LastName')
        cls.genre = Genres.objects.create(genre='test_genre')
        cls.movie = Movies.objects.create(
            title='TestMovie',
            release_date='2000-06-12',
            director=cls.director,
        )
        cls.movie.genre.set([cls.genre])

    def setUp(self):
        self.authorized_user_client = Client()
        self.not_authorized_user_client = Client()
        self.authorized_user_client.force_login(self.authorized_user)

    def test_add_movie_by_authorized_user(self):
        url = reverse('movies:create')
        response = self.authorized_user_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], MovieForm)

    def test_add_movie_by_not_authorized_user(self):
        url = reverse('movies:create')
        response = self.not_authorized_user_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
