import pytest

from django.urls import reverse
from http import HTTPStatus
from pytest_django.asserts import assertRedirects
from pytest_lazy_fixtures import lf


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, kwargs',
    [('index', None),
     ('users:registration', None),
     ('users:login', None),
     ('movies:movie_list', None),
     ('movies:movie_detail', lf('pk_for_movie')),
     ('movies:reviews_list', lf('pk_for_movie')),
     ('movies:review_detail', lf('pk_for_movie_and_review'))]
     )
def test_pages_for_anonymous_user(client, name, kwargs):
    url = reverse(name, kwargs=kwargs)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, kwargs',
    [
        ('users:profile', None),
        ('users:edit', None),
        ('users:password_change', None),
        ('movies:create', None),
        ('movies:add_review', lf('pk_for_movie'))
        ]
)
def test_pages_availability_for_auth_user(authorized_user_client,
                                          name,
                                          kwargs):
    url = reverse(name, kwargs=kwargs)
    response = authorized_user_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
   'name, kwargs',
   [
       ('users:profile', None),
       ('users:edit', None),
       ('users:password_change', None),
       ('movies:create', None),
       ('movies:add_review', lf('pk_for_movie'))
       ]
)
def test_pages_availability_for_not_auth_user(client, name, kwargs):
    login_url = reverse('users:login')
    url = reverse(name, kwargs=kwargs)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
