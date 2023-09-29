from rest_framework import serializers
from .models import Genre, Book
from .mixins import ToInternalValueMixin


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class BookSerializer(
    ToInternalValueMixin,
    serializers.ModelSerializer,
):
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


class BookUpdateSerializer(
    ToInternalValueMixin,
    serializers.ModelSerializer,
):
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
