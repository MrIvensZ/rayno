# ray_no/movies/pytest_tests/conftest.py
import os
import sys
import django

# Добавляем путь к корню проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# Настраиваем Django ДО импорта моделей
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ray_no.settings')

django.setup()

import pytest
from django.test.client import Client

from django.conf import settings

from movies.models import Directors, Genres


@pytest.fixture
def authorized_user(django_user_model):
    return django_user_model.objects.create(username='auth_user')


@pytest.fixture
def authorized_user_client(authorized_user):
    client = Client()
    client.force_login(authorized_user)
    return client


@pytest.fixture
def unauthorized_user_client():
    client = Client()
    return client


@pytest.fixture
def genre():
    genre = Genres.objects.create(genre='test_genre')
    return genre


@pytest.fixture
def director():
    director = Directors.objects.create(first_name='Name',
                                        last_name='LastName')
    return director


@pytest.fixture
def movie_form_data(director, genre):
    form_data = {'title': 'TestMovie',
                 'release_date': '2000-06-12',
                 'director': director, }
    return form_data
