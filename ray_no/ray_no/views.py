# from django.shortcuts import render
from django.views.generic import ListView

from movies.models import Movies


# def index(request):
#     template = 'includes/index.html'
#     return render(request, template)

class TopMoviesListView(ListView):
    model = Movies
    template_name = 'includes/index.html'
    extra_context = {
        'movies': Movies.objects.with_ratings(),
    }
