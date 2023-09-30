from rest_framework import serializers
from .models import Genre, Book, Author
from .utils import transform_genres_and_authors


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="genre_name",
        queryset=Genre.objects.all(),
        many=True,
    )
    author = serializers.SlugRelatedField(
        slug_field="author_name",
        queryset=Author.objects.all(),
        many=True,
    )

    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ["owner"]

    def to_internal_value(self, data):
        data = transform_genres_and_authors(data, "genre", Genre)
        data = transform_genres_and_authors(data, "author", Author)
        return super().to_internal_value(data)
