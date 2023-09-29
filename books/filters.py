import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            "author",
            "genre__genre_name",
            "condition",
            "available",
        }
