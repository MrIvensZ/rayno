from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from .models import Movies, Rating, Reviews, Comments
from .forms import RatingForm, MovieForm, ReviewForm, CommentForm


def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            messages.success(request, f'Фильм "{movie.title}" добавлен!')
            return redirect('movies:detail', movie_id=movie.id)
    else:
        form = MovieForm()
    template = 'movies/movie_create.html'
    context = {'form': form}
    return render(request, template, context)


def movie_list(request):
    movies = Movies.objects.with_ratings()
    template = 'movies/movies.html'
    context = {'movies': movies}
    return render(request, template, context)


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movies.objects.with_ratings()
                              .select_related('director')
                              .prefetch_related('genre'),
                              id=movie_id)
    your_score = None
    try:
        your_score = Rating.objects.get(user=request.user, movie=movie).rate
    except Rating.DoesNotExist:
        pass
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                movie=movie,
                defaults={'rate': form.cleaned_data['rate']}
            )
            if created:
                messages.success(request, 'Оценка добавлена!')
            else:
                messages.success(request, 'Оценка обновлена!')
    else:
        form = RatingForm()
    template = 'movies/movie_detail.html'
    context = {'movie': movie,
               'form': form,
               'your_score': your_score}
    return render(request, template, context)


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
                messages.success(request, 'Обзор добавлен!')
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
    comments = review.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comments.objects.create(
                user=request.user,
                text=form.cleaned_data['text'],
                review=review
            )
            if comment:
                messages.success(request, 'Комментарий добавлен!')
                return redirect(review)
    else:
        form = ReviewForm()
    context = {'review': review,
               'comments': comments,
               'form': form}
    template = 'movies/review_detail.html'
    return render(request, template, context)
