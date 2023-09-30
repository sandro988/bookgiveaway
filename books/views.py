from .serializers import BookSerializer
from .permissions import IsAuthorOrReadOnly
from .filters import BookFilter
from .models import Book
from rest_framework.viewsets import ModelViewSet


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
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
