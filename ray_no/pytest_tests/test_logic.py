import pytest

from pytest_django.asserts import assertRedirects
from django.urls import reverse

from movies.models import Movies, Rating, Reviews, Comments


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


@pytest.mark.django_db
def test_auth_user_can_rate_movie(
    pk_for_movie,
    authorized_user_client,
    rating_form_data,
    authorized_user
):
    url = reverse('movies:movie_detail', kwargs=pk_for_movie)
    response = authorized_user_client.post(url, data=rating_form_data)
    assert Rating.objects.count() == 1
    new_rate = Rating.objects.get()
    assert new_rate.user.id == authorized_user.id
    assert new_rate.movie.id == rating_form_data['movie']
    assert new_rate.rate == rating_form_data['rate']
    assertRedirects(response, reverse('movies:movie_detail',
                                      kwargs=pk_for_movie))


@pytest.mark.django_db
def test_auth_user_cant_rate_movie_with_wrong_data(
    pk_for_movie,
    authorized_user_client,
    wrong_rating_form_data
):
    url = reverse('movies:movie_detail', kwargs=pk_for_movie)
    authorized_user_client.post(url, data=wrong_rating_form_data)
    assert Rating.objects.count() == 0


@pytest.mark.django_db
def test_not_auth_user_cant_rate_movie(
    pk_for_movie,
    client,
    rating_form_data
):
    url = reverse('movies:movie_detail', kwargs=pk_for_movie)
    client.post(url, data=rating_form_data)
    assert Rating.objects.count() == 0


@pytest.mark.django_db
def test_auth_user_can_add_review(
    pk_for_movie,
    authorized_user_client,
    review_form_data,
    authorized_user
):
    url = reverse('movies:add_review', kwargs=pk_for_movie)
    response = authorized_user_client.post(url, data=review_form_data)
    assert Reviews.objects.count() == 1
    new_review = Reviews.objects.get()
    assert new_review.user.id == authorized_user.id
    assert new_review.movie.id == review_form_data['movie']
    assert new_review.text == review_form_data['text']
    assertRedirects(response, reverse(
        'movies:review_detail',
        kwargs={
            'movie_id': review_form_data['movie'],
            'review_id': new_review.pk
            }))


@pytest.mark.django_db
def test_not_auth_user_cant_add_review(
    pk_for_movie,
    client,
    review_form_data,
):
    url = reverse('movies:add_review', kwargs=pk_for_movie)
    client.post(url, data=review_form_data)
    assert Reviews.objects.count() == 0


@pytest.mark.django_db
def test_auth_user_can_add_comment(pk_for_movie_and_review,
                                   authorized_user_client,
                                   comment_form_data,
                                   authorized_user):
    url = reverse('movies:review_detail', kwargs=pk_for_movie_and_review)
    response = authorized_user_client.post(url, data=comment_form_data)
    assert Comments.objects.count() == 1
    new_comment = Comments.objects.get()
    assert new_comment.review.id == comment_form_data['review']
    assert new_comment.user.id == authorized_user.id
    assert new_comment.text == comment_form_data['text']
    assertRedirects(response, reverse('movies:review_detail',
                                      kwargs=pk_for_movie_and_review))


@pytest.mark.django_db
def test_not_auth_user_cant_add_comment(pk_for_movie_and_review,
                                        client,
                                        comment_form_data):
    url = reverse('movies:review_detail', kwargs=pk_for_movie_and_review)
    client.post(url, data=comment_form_data)
    assert Comments.objects.count() == 0
