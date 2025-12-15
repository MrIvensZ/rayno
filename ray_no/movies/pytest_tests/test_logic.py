import pytest
from http import HTTPStatus

from django.urls import reverse
# from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
def test_unauthorized_user_cant_add_movie(unauthorized_user_client):
    url = reverse('movies:create')
    response = unauthorized_user_client.get(url)
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
def auth_user_can_add_movie(authorized_user_client, movie_form_data):
    url = reverse('movies:create')
    response = authorized_user_client.get(url)
    assert response.status_code == HTTPStatus.OK
    response = authorized_user_client.post(url, data=movie_form_data)
    assert response.status_code == HTTPStatus.FOUND
