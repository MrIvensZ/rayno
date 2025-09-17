from django.contrib import admin

from .models import Movies, Rating, Directors, Genres


@admin.register(Movies)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rate')


@admin.register(Directors)
class DirectorAdmin(admin.ModelAdmin):
    pass


@admin.register(Genres)
class GenreAdmin(admin.ModelAdmin):
    pass
