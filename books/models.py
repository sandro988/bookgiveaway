import uuid
from django.contrib.auth import get_user_model
from django.db import models


class Genre(models.Model):
    genre_name = models.CharField(max_length=100, unique=True)
    genre_description = models.TextField(blank=True)

    def __str__(self):
        return self.genre_name


class Book(models.Model):
    def book_cover_filename(self, filename):
        """
        Used for assigning names to book covers so that they are more manageable and unique.
        """
        return f"book_covers/{self.id}-{filename}"

    CONDITION_CHOICES = [
        ("Brand New", "Brand New"),
        ("Used", "Used"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    ISBN = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True, default="No description")
    condition = models.CharField(
        max_length=10, choices=CONDITION_CHOICES, default="Brand New"
    )
    book_cover = models.ImageField(upload_to=book_cover_filename, blank=True, null=True)
    available = models.BooleanField(default=True)
    location = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
