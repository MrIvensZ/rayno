from csv import DictReader

from django.core.management.base import BaseCommand
from movies.models import Genres

PATH = 'data/'


class Command(BaseCommand):

    def handle(self, *args, **options):
        for row in DictReader(open(f'{PATH}genres.csv', encoding='utf8')):
            genre = Genres(genre=row['genre'])
            genre.save()
