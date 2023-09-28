from django.urls import path
from .views import BookListCreateView, BookDetailView


urlpatterns = [
    path("", BookListCreateView.as_view(), name="book_list_create_api_view"),
    path("<uuid:pk>/", BookDetailView.as_view(), name="book_detail_api_view"),
]
