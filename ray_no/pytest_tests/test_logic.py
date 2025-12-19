import pytest

from pytest_django.asserts import assertRedirects
from django.urls import reverse

from movies.models import Movies


def test_auth_user_can_add_movie(authorized_user_client, movie_form_data):
    url = reverse('movies:create')
    response = authorized_user_client.post(url, data=movie_form_data)
    assert Movies.objects.count() == 1
    new_movie = Movies.objects.get()
    assert new_movie.title == movie_form_data['title']
    assert new_movie.release_date == movie_form_data['release_date']
    assert new_movie.director.id == movie_form_data['director']
    assert new_movie.genre.get().id == movie_form_data['genre'][0]
    assertRedirects(response, reverse('movies:movie_detail',
                                      kwargs={'movie_id': new_movie.pk}))


@pytest.mark.django_db
def test_not_auth_user_cant_add_movie(client, movie_form_data):
    url = reverse('movies:create')
    response = client.post(url, data=movie_form_data)
    assert Movies.objects.count() == 0
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
