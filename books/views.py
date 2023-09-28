from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import BookSerializer, BookUpdateSerializer
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
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        return (
            BookUpdateSerializer if self.request.method == "PATCH" else BookSerializer
        )

    def patch(self, request, *args, **kwargs):
        # For some reason that I could not figure out whenever I tried to update JUST the genre of a book I was getting:
        # 'AttributeError: This QueryDict instance is immutable' and a status code of '500 - Internal Server Error'.
        # The only way I came up with to kind of solve that problem was the one down below. I know that it is not the best
        # and there might be a better solution for this particular problem but this is the only solution that I came up with.

        request.POST._mutable = True
        return super().patch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        request.POST._mutable = True
        return super().patch(request, *args, **kwargs)
