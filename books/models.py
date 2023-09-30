import uuid
from django.contrib.auth import get_user_model
from django.db import models


class Genre(models.Model):
    """
    model for book genres.

    Attributes:
        genre_name (str): The name of the genre (for example: "Thriller").
    """

    genre_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.genre_name


class Author(models.Model):
    """
    Model for book authors.

    model fields:
        author_name (str): The name of the author (for example: "Stephen King").
    """

    author_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.author_name


class Book(models.Model):
    """
    Model for a book with various details.

    Model fields:
        owner (ForeignKey): The owner of the book.
        author (ManyToManyField): The authors of the book.
        genre (ManyToManyField): The genres associated with the book.
        title (str): The title of the book.
        ISBN (str): The ISBN (International Standard Book Number) of the book.
        description (str): A brief description of the book.
        condition (str): The condition of the book (either "Brand New" or "Used").
        book_cover (ImageField): An image representing the book cover.
        available (bool): Indicates whether the book is available or not(either True or False).
        retrieval_location (str): The location from where the book can be retrieved.
        created (DateTimeField): The date and time when the book record was created.
        updated (DateTimeField): The date and time when the book record was last updated.
    """

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
    author = models.ManyToManyField(Author)
    genre = models.ManyToManyField(Genre)
    title = models.CharField(max_length=255, unique=True)
    ISBN = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True, default="No description")
    condition = models.CharField(
        max_length=10, choices=CONDITION_CHOICES, default="Brand New"
    )
    book_cover = models.ImageField(upload_to=book_cover_filename, blank=True, null=True)
    available = models.BooleanField(default=True)
    retrieval_location = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
