import pytest

from django.urls import reverse
from pytest_lazy_fixtures import lf

from movies.forms import MovieForm, RatingForm, ReviewForm, CommentForm


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, context_list_name, kwargs, object_name, context_object_name',
    [
        (
            'index',
            'movies',
            None,
            lf('movie'),
            None
            ),
        (
            'movies:movie_list',
            'movies',
            None,
            lf('movie'),
            None
            ),
        (
            'movies:movie_detail',
            None,
            lf('pk_for_movie'),
            lf('movie'),
            'movie'
            ),
        (
            'movies:reviews_list',
            'reviews',
            lf('pk_for_movie'),
            lf('review'),
            None
            ),
        (
            'movies:review_detail',
            None,
            lf('pk_for_movie_and_review'),
            lf('review'),
            'review'
            )
     ]
)
def test_objects_in_list_for_anonymus(
    name,
    context_list_name,
    kwargs,
    client,
    object_name,
    context_object_name
):
    url = reverse(name, kwargs=kwargs)
    response = client.get(url)
    if context_list_name:
        assert object_name in response.context[context_list_name]
    else:
        assert object_name == response.context[context_object_name]


def test_profile_content(authorized_user_client, authorized_user):
    url = reverse('users:profile')
    response = authorized_user_client.get(url)
    assert authorized_user == response.context['user']


@pytest.mark.parametrize(
    'name, kwargs, model_form',
    [
        (
            'movies:create',
            None,
            MovieForm
            ),
        (
            'movies:movie_detail',
            lf('pk_for_movie'),
            RatingForm
            ),
        (
            'movies:add_review',
            lf('pk_for_movie'),
            ReviewForm
            ),
        (
            'movies:review_detail',
            lf('pk_for_movie_and_review'),
            CommentForm
            ),
     ]
)
def test_auth_user_contains_form(authorized_user_client,
                                 name,
                                 kwargs,
                                 model_form):
    url = reverse(name, kwargs=kwargs)
    response = authorized_user_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], model_form)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, kwargs, model_form',
    [
        (
            'movies:movie_detail',
            lf('pk_for_movie'),
            RatingForm
            ),
        (
            'movies:review_detail',
            lf('pk_for_movie_and_review'),
            CommentForm
            ),
     ]
)
def test_not_auth_user_contains_form(client,
                                     name,
                                     kwargs,
                                     model_form):
    # нужно переписать логику вьюсетов, чтобы форма вообще не передавалась в контекст неавторизованного пользователя
    url = reverse(name, kwargs=kwargs)
    response = client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], model_form)
