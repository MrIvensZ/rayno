from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, CreateView

from .models import Movies, Rating, Reviews, Comments
from .forms import RatingForm, MovieForm, ReviewForm, CommentForm
from ray_no.settings import DEFAULT_MOVIE_IMAGE


class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movies
    form_class = MovieForm
    template_name = 'movies/movie_create.html'


class MovieListView(ListView):
    context_object_name = 'movies'  # имя объекта в шаблоне
    template_name = 'movies/movies.html'
    paginate_by = 10
    extra_context = {'default_poster': DEFAULT_MOVIE_IMAGE}

    def get_queryset(self):
        # поскольку у нас непростое получение объектов модели,
        # нужно отредактировать получение кварисета
        return Movies.objects.with_ratings().order_by('title')


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movies.objects.with_ratings()
                              .select_related('director')
                              .prefetch_related('genre'),
                              id=movie_id)
    your_score = None
    if request.user.is_authenticated:
        try:
            your_score = Rating.objects.get(
                user=request.user,
                movie=movie
                ).rate
        except Rating.DoesNotExist:
            pass
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                user=request.user,
                movie=movie,
                defaults={'rate': form.cleaned_data['rate']}
            )
    else:
        form = RatingForm()
    template = 'movies/movie_detail.html'
    context = {'movie': movie,
               'form': form,
               'your_score': your_score,
               'default_poster': DEFAULT_MOVIE_IMAGE}
    return render(request, template, context)


@login_required
def review_add(request, movie_id):
    movie = get_object_or_404(Movies, pk=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Reviews.objects.create(
                user=request.user,
                text=form.cleaned_data['text'],
                movie=movie
            )
            if review:
                return redirect(review.get_absolute_url())
    else:
        form = ReviewForm()
    template = 'movies/add_review.html'
    context = {'form': form, 'movie': movie, }
    return render(request, template, context)


def review_list(request, movie_id):
    movie = Movies.objects.get(pk=movie_id)
    reviews = movie.reviews.all()
    context = {'reviews': reviews, 'movie': movie}
    template = 'movies/reviews.html'
    return render(request, template, context)


def review_detail(request, movie_id, review_id):
    review = get_object_or_404(Reviews, pk=review_id)
    comments = review.comments.all().order_by('-time_create')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comments.objects.create(
                user=request.user,
                text=form.cleaned_data['text'],
                review=review
            )
            if comment:
                return redirect(review)
    else:
        form = CommentForm()
    context = {'review': review,
               'comments': comments,
               'form': form}
    template = 'movies/review_detail.html'
    return render(request, template, context)
