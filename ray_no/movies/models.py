from django.db import models
# GeneratedField импортируется только так
from django.db.models.fields.generated import GeneratedField
from django.db.models.functions import Concat, Coalesce
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

User = get_user_model()


class MovieQuerySet(models.QuerySet):
    """Изменение мэнеджера для получения рейтингов и количества оценок"""

    def with_ratings(self):
        return self.annotate(
            avg_rating=Coalesce(models.Avg('ratings__rate'),
                                models.Value(0.0)),
            rating_count=models.Count('ratings')
        )


class Genres(models.Model):
    """Модель жанров"""

    genre = models.CharField(max_length=128,
                             verbose_name='Жанр')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.genre


class Directors(models.Model):
    """Модель режиссёров"""

    first_name = models.CharField(max_length=128,
                                  verbose_name='Имя режиссёра')
    last_name = models.CharField(max_length=128,
                                 verbose_name='Фамилия режиссёра')
    full_name = GeneratedField(
        # само выражение
        expression=Concat('first_name', models.Value(' '), 'last_name'),
        # какое поле должно быть
        output_field=models.CharField(max_length=128),
        db_persist=True
    )

    class Meta:
        verbose_name = 'Режиссёр'
        verbose_name_plural = 'Режиссёры'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Movies(models.Model):
    """Модель фильмов"""

    title = models.CharField(max_length=100,
                             verbose_name='Название фильма',
                             help_text='Введите название фильма')
    release_date = models.DateField(null=True,
                                    verbose_name='Дата выхода')
    director = models.ForeignKey(Directors,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='movies',
                                 verbose_name='Режиссёр фильма')
    genre = models.ManyToManyField(Genres,
                                   related_name='movies',
                                   verbose_name='Жанры')

    poster = models.ImageField(upload_to='movie_posters',
                               blank=True,
                               null=True,
                               verbose_name='Постер фильма')

    objects = MovieQuerySet.as_manager()

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movies:movie_detail', kwargs={'movie_id': self.pk})


class Rating(models.Model):
    """Модель рейтингов фильмов"""

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='ratings',
                             verbose_name='Пользователь')
    movie = models.ForeignKey('Movies',
                              on_delete=models.CASCADE,
                              related_name='ratings',
                              verbose_name='Фильм')
    rate = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Оценка',
        help_text='Оценка от 1 до 10')

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}: {self.rate}'

    class Meta:
        verbose_name = 'Оценка пользователя'
        verbose_name_plural = 'Оценки пользователя'
        unique_together = ['user', 'movie']


class Reviews(models.Model):
    """Модель обзоров фильмов"""

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='reviews',
                             verbose_name='Пользователь')
    text = models.TextField(max_length=1000,
                            verbose_name='Текст обзора')
    movie = models.ForeignKey(Movies,
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='Фильм')
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Обзор пользователя {self.user} на фильм {self.movie}.'

    class Meta:
        verbose_name = 'Обзор пользователя'
        verbose_name_plural = 'Обзоры пользователя'
        unique_together = ['user', 'movie']

    def get_absolute_url(self):
        return reverse('movies:review_detail', kwargs={
            'review_id': self.pk,
            'movie_id': self.movie.pk})


class Comments(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Пользователь')
    text = models.TextField(max_length=500,
                            verbose_name='Текст комментария')
    review = models.ForeignKey(Reviews,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Обзор')
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Коментарий {self.id}'

    class Meta:
        verbose_name = 'Комментарий пользователя'
        verbose_name_plural = 'Комментарии пользователя'
