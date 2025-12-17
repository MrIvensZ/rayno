import pytest

from pytest_lazy_fixtures import lf

from http import HTTPStatus

from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, kwargs',
    [('index', None),
     ('users:registration', None),
     ('users:login', None),
     ('movies:movie_list', None),
     ('movies:movie_detail', lf('pk_for_movie')),
     ('movies:reviews_list', lf('pk_for_movie')),
     ('movies:review_detail', lf('pk_for_movie_and_review'))])
def test_pages_for_anonymous_user(client, name, kwargs):
    url = reverse(name, kwargs=kwargs)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('users:profile',
     'users:edit',
     'users:password_change',
     'movies:create',)
)
def test_pages_availability_for_auth_user(authorized_user_client, name):
    url = reverse(name)
    response = authorized_user_client.get(url)
    assert response.status_code == HTTPStatus.OK
