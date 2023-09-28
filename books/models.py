import uuid
from django.contrib.auth import get_user_model
from django.db import models


class Book(models.Model):
    def book_cover_filename(self, filename):
        """
        Used for assigning names to book covers so that they are more manageable and unique.
        """
        return f"book_covers/{self.id}-{filename}"

    GENRE_CHOICES = [
        ("Fiction", "Fiction"),
        ("Non-Fiction", "Non-Fiction"),
        ("Mystery", "Mystery"),
        ("Romance", "Romance"),
        ("Science Fiction", "Science Fiction"),
        ("Fantasy", "Fantasy"),
        ("Thriller", "Thriller"),
        ("Horror", "Horror"),
        ("Biography", "Biography"),
        ("Autobiography", "Autobiography"),
        ("History", "History"),
        ("Philosophy", "Philosophy"),
        ("Drama", "Drama"),
        ("Business", "Business"),
        ("Psychology", "Psychology"),
        ("Detective", "Detective"),
        ("Comics", "Comics"),
    ]

    CONDITION_CHOICES = [
        ("Brand New", "Brand New"),
        ("Used", "Used"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    ISBN = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True)
    condition = models.CharField(
        max_length=10, choices=CONDITION_CHOICES, default="Brand New"
    )
    book_cover = models.ImageField(upload_to=book_cover_filename, blank=True)
    available = models.BooleanField(default=True)
    location = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
