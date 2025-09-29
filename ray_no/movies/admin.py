from django.contrib import admin

from .models import Movies, Rating, Directors, Genres, Reviews, Comments


@admin.register(Movies)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'director',
                    'release_date')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ['director',]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rate')
    list_display_links = ('rate',)


@admin.register(Directors)
class DirectorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'movie_count')
    list_display_links = ('full_name', )
    search_fields = ('full_name',)
    ordering = ['full_name',]

    @admin.display(description='Количество фильмов')
    def movie_count(self, director: Directors):
        count = director.movies.count()
        string = ''
        if count != 11 and (count % 10) == 1:
            string = 'фильм'
        elif (count % 10) in [2, 3, 4] and count not in [12, 13, 14]:
            string = 'фильма'
        else:
            string = 'фильмов'
        return f'{count} {string}'


@admin.register(Genres)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'genre')
    list_display_links = ('genre', )
    ordering = ['id',]


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'time_create')
    list_display_links = ('user', )
    ordering = ['time_create',]


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'time_create')
    list_display_links = ('user', )
    ordering = ['-time_create',]
