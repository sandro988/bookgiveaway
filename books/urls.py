from .views import BookViewSet, GenreListAPIView, AuthorListAPIView
from rest_framework.routers import SimpleRouter
from django.urls import path

router = SimpleRouter()
router.register("", BookViewSet, basename="books")
urlpatterns = [
    path("genres/", GenreListAPIView.as_view(), name="genres-list"),
    path("authors/", AuthorListAPIView.as_view(), name="authors-list"),
] + router.urls
