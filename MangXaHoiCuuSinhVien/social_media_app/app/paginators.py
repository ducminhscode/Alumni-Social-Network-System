from rest_framework import pagination


class AlumniPagination(pagination.PageNumberPagination):
    page_size = 10