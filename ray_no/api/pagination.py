from rest_framework import pagination


class MovieAPIPagination(pagination.PageNumberPagination):
    # количество записей на одной страницу
    page_size = 2
    # имя параметра в адресной строке, чтобы пользователь мог сам задать количество записей:
    # http://127.0.0.1:8000/api/v1/movies/?page_size=1
    page_size_query_param = 'page_size'
    max_page_size = 10
