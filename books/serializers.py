from rest_framework import serializers
from .models import Genre, Book


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
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
        """
        This method is used to get the genres, capitalize them so that
        no duplicate genres are created and create them if they do not already
        exist in the Genre model.

        For example if user inputs genre in all uppercase it will be capitalized
        and checked if already exists in the Genre model. Thus no duplicate of Genre
        will be created.

        Parameters:
            data (dict): The input data to be transformed.

        Returns:
            dict: The transformed data with 'genre' field converted to a list of Genre objects.
        """

        genre_names = data.get("genre")
        if genre_names:
            genres = []
            for genre_name in genre_names:
                genre_name = genre_name.capitalize()
                genre, _ = Genre.objects.get_or_create(genre_name=genre_name)
                genres.append(genre)

            data["genre"] = genres
        return super().to_internal_value(data)
