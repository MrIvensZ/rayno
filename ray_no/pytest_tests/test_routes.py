import pytest

from http import HTTPStatus

from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, kwargs',
    [('index', {}),
     ('users:registration', {}),
     ('users:login', {}),
     ('movies:movie_list', {}),]
)
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
