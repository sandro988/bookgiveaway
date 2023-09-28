from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import BookSerializer
from .permissions import IsAuthorOrReadOnly
from .models import Book


class BookListCreateView(ListCreateAPIView):
    """
    View used for listing exsiting books or creating new ones.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookDetailView(RetrieveUpdateDestroyAPIView):
    """
    View used for retrieving individual books, updating and deleteing them.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthorOrReadOnly,)
