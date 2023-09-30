from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .serializers import BookSerializer, GenreSerializer, AuthorSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import BookFilter
from .models import Book, Genre, Author


class BookViewSet(ModelViewSet):
    """
    **Book Management API Endpoint**

    This viewset provides various operations for managing books, including creating, retrieving, updating, and deleting book records.

    **Authentication:**
    - Creating, updating, or deleting books requires authentication. Only authenticated users can
    perform these actions and they must be the owners of the books.
    - Viewing the list of available books and retrieving book details is accessible to all users.

    **Supported Operations:**

    - `list`: Get a list of all available books.
    - `create`: Create a new book record.
    - `retrieve`: Retrieve the details of a specific book by its unique ID.
    - `update`: Update the details of a specific book by its unique ID.
    - `partial_update`: Partially update the details of a specific book by its unique ID.
    - `destroy`: Delete a specific book by its unique ID.

    **Filtering Options:**

    - `author__author_name`: Filter books by author.
    - `genre__genre_name`: Filter books by genre.
    - `condition`: Filter books by condition (options: **'Brand New'** or **'Used'**).
    - `available`: Filter books by availability status (options: **'true'** or **'false'**).

    **Genre Field, Author Field (ManyToMany):**

    The `genre` and `author` fields in the JSON response are represented as a list of genre/author names as strings.

    **Genre and Author fields example (JSON):**

    `{"genre": ["Classic", "Fiction"], "author": ["F. Scott Fitzgerald", "Stephen King"], ...}`
    """

    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filterset_class = BookFilter
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GenreListAPIView(ListAPIView):
    """
    **Genre List API Endpoint**

    This view provides users with a list of available genres. With this view users can retrieve all the
    genres present in the database.

    **Authentication:**
    - No authentication is required to access this view.

    **Supported Operations:**

    - `list`: Gets a list of all available genres.

    **Genre Field (JSON Response):**

    - The genres are represented as a list of dictionaries, each containing the `id` and `genre_name` fields.

    **Genre field example (JSON):**

    `[{"id": 1, "genre_name": "Horror"}, {"id": 2, "genre_name": "Thriller"}, ...]`
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]


class AuthorListAPIView(ListAPIView):
    """
    **Author List API Endpoint**

    This view provides users with a list of available authors. With this view users can retrieve all the
    authors present in the database.

    **Authentication:**
    - No authentication is required to access this view.

    **Supported Operations:**

    - `list`: Gets a list of all available authors.

    **Author Field (JSON Response):**

    The authors are represented as a list of dictionaries, each containing the `id` and `author_name` fields.

    **Author field example (JSON):**

    `[{"id": 1, "author_name": "F. Scott Fitzgerald"}, {"id": 2, "author_name": "Stephen King"}, ...]`
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]
