from .models import Genre


class ToInternalValueMixin:
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
