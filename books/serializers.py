from rest_framework import serializers
from .models import Genre, Book


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    """
    This serializer will NOT be used for PUT, PATCH requests
    """

    genre = serializers.SlugRelatedField(
        slug_field="genre_name",
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ["owner"]

    def to_internal_value(self, data):
        genre_names = data.get("genre")
        if genre_names:
            genres = []
            for genre_name in genre_names:
                genre_name = genre_name.capitalize()
                genre, _ = Genre.objects.get_or_create(genre_name=genre_name)
                genres.append(genre)

            data["genre"] = genres
        return super().to_internal_value(data)


class BookUpdateSerializer(serializers.ModelSerializer):
    """
    I could not figure out why but for some reason the PATCH request does not take partial updates when I send request from swagger.
    It was demanding to include fields such as: title, author, ISBN, location and genre in the request even though it should be able
    to take partial updates, so I created this separate serializer and in BookDetailView's 'get_serializer_class'
    method I am passing this serializer if the request.method is PATCH, otherwise I am passing BookSerializer.
    """

    genre = serializers.SlugRelatedField(
        slug_field="genre_name", queryset=Genre.objects.all(), many=True, required=False
    )

    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ["owner"]
        extra_kwargs = {
            "title": {"required": False},
            "author": {"required": False},
            "ISBN": {"required": False},
            "retrieval_location": {"required": False},
        }

    def to_internal_value(self, data):
        genre_names = data.get("genre")
        genre_names = list(genre_names)
        if genre_names:
            genres = []
            for genre_name in genre_names:
                genre_name = genre_name.capitalize()
                genre, _ = Genre.objects.get_or_create(genre_name=genre_name)
                genres.append(genre)

            data["genre"] = genres
        return super().to_internal_value(data)
