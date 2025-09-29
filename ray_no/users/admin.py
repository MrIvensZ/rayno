from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'username',
                    'sex',
                    'review_count',
                    'comment_count',)
    list_display_links = ('id', 'username')
    search_fields = ('username',)
    ordering = ['id',]

    @admin.display(description='Количество обзоров')
    def review_count(self, user: CustomUser):
        count = user.reviews.count()
        string = ''
        if count != 11 and (count % 10) == 1:
            string = 'обзор'
        elif (count % 10) in [2, 3, 4] and count not in [12, 13, 14]:
            string = 'обзора'
        else:
            string = 'обзоров'
        return f'{count} {string}'

    @admin.display(description='Количество комментариев')
    def comment_count(self, user: CustomUser):
        count = user.comments.count()
        string = ''
        if count != 11 and (count % 10) == 1:
            string = 'комментарий'
        elif (count % 10) in [2, 3, 4] and count not in [12, 13, 14]:
            string = 'комментария'
        else:
            string = 'комментариев'
        return f'{count} {string}'
