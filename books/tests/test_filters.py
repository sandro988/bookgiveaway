from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from books.models import Book, Genre
from .test_views import UserTestsData


class BookFilterTestClass(TestCase, UserTestsData):
    @classmethod
    def setUpTestData(cls):
        UserTestsData.setUpTestData()

        # First Creating genres
        cls.genre1 = Genre.objects.create(genre_name="History")
        cls.genre2 = Genre.objects.create(genre_name="Fiction")

        # Creating books
        cls.book1 = Book.objects.create(
            title="Book 1",
            author="Author 1",
            condition="Brand New",
            available=True,
            ISBN="1",
            retrieval_location="Tbilisi",
            owner=cls.user,
        )
        cls.book2 = Book.objects.create(
            title="Book 2",
            author="Author 2",
            condition="Used",
            available=False,
            ISBN="2",
            retrieval_location="Tbilisi",
            owner=cls.user,
        )
        cls.book3 = Book.objects.create(
            title="Book 3",
            author="Author 2",
            condition="Brand New",
            available=True,
            ISBN="3",
            retrieval_location="Tbilisi",
            owner=cls.user,
        )

        # Assigning genres to books
        cls.book1.genre.add(cls.genre1)
        cls.book2.genre.add(cls.genre2)
        cls.book3.genre.add(cls.genre2)

        cls.book_list_url = reverse("books-list")

    def test_filter_by_author(self):
        response = self.client.get(
            self.book_list_url, {"author": "Author 1"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book 1")

        response = self.client.get(
            self.book_list_url, {"author": "Author 2"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Only second and third books had Author with the name: "Author 2"
        self.assertEqual(response.data[0]["title"], "Book 2")
        self.assertEqual(response.data[1]["title"], "Book 3")

    def test_filter_by_condition(self):
        response = self.client.get(self.book_list_url, {"condition": "Brand New"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Only first and third books had the condition of "Brnad New"
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, ["Book 1", "Book 3"])

    def test_filter_by_available(self):
        response = self.client.get(self.book_list_url, {"available": "true"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Only first and third books were available for retrieval.
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, ["Book 1", "Book 3"])

    def test_filter_by_genre(self):
        response = self.client.get(self.book_list_url, {"genre__genre_name": "Fiction"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Only second and third books had genre of "Fiction"
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, ["Book 2", "Book 3"])
