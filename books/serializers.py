from rest_framework import serializers
from .models import Genre, Book, Author


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

    owner_email = serializers.EmailField(source="owner.email", read_only=True)

    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ["owner", "owner_email"]

    def to_internal_value(self, data):
        genre_names = data.get("genre", [])
        data["genre"] = [
            Genre.objects.get_or_create(genre_name=genre.capitalize())[0]
            for genre in genre_names
        ]

        author_names = data.get("author", [])
        data["author"] = [
            Author.objects.get_or_create(author_name=author.title())[0]
            for author in author_names
        ]

        return super().to_internal_value(data)
