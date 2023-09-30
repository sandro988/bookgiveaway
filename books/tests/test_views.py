from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from books.models import Book, Genre, Author


class UserTestsData:
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="test_user@email.com", password="test_pass"
        )


class BookListCreateViewTests(APITestCase, UserTestsData):
    @classmethod
    def setUpTestData(cls):
        UserTestsData.setUpTestData()

        cls.token = Token.objects.create(user=cls.user)
        cls.book_data = {
            "title": "Test Book",
            "author": ["Charles Dickens", "Stephen King"],
            "genre": ["History", "Fiction"],
            "ISBN": "1234567890",
            "description": "This is a test book.",
            "condition": "Brand New",
            "available": True,
            "retrieval_location": "Test Location",
            # Owner field will be set to request.user because of the perform_create method that I overrode in BookListCreateView.
        }

        cls.book_list_url = reverse("books-list")

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_create_and_list_functionality(self):
        response_for_create = self.client.post(
            self.book_list_url, self.book_data, format="json"
        )

        # Checking that new book was created successfully.
        self.assertEqual(response_for_create.status_code, status.HTTP_201_CREATED)
        book = Book.objects.last()
        genres = [genre.genre_name for genre in book.genre.all()]
        authors = [author.author_name for author in book.author.all()]

        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(authors, ["Charles Dickens", "Stephen King"])
        self.assertEqual(genres, ["History", "Fiction"])
        self.assertEqual(book.condition, "Brand New")
        self.assertEqual(book.available, True)
        self.assertEqual(book.owner, self.user)

        # Checking that book is listed out when users access api/books/ endpoint with GET request.
        response_for_list = self.client.get(self.book_list_url)
        self.assertEqual(response_for_list.status_code, status.HTTP_200_OK)

    def test_create_with_duplicate_data(self):
        # Creating new book
        first_create_response = self.client.post(
            self.book_list_url, self.book_data, format="json"
        )
        self.assertEqual(first_create_response.status_code, status.HTTP_201_CREATED)

        # Trying to create the exact same book I created previouisly.
        second_create_response = self.client.post(
            self.book_list_url, self.book_data, format="json"
        )
        self.assertEqual(
            second_create_response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_create_with_empty_fields(self):
        self.book_data["title"] = ""
        response = self.client.post(self.book_list_url, self.book_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_unauthenticated_user(self):
        # I am creating a new instance of the self.client without authentication credentials.
        client = self.client_class()
        response = client.post(self.book_list_url, self.book_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 0)

    def test_book_listing_with_unauthenticated_user(self):
        # First I create a book
        create_book_response = self.client.post(
            self.book_list_url, self.book_data, format="json"
        )

        # Just like in the previoius test I am creating a new instance of the
        # self.client without authentication credentials.
        client = self.client_class()
        list_book_response = client.get(self.book_list_url)

        self.assertEqual(list_book_response.status_code, status.HTTP_200_OK)


class BookRetrieveUpdateDeleteViewTests(APITestCase, UserTestsData):
    @classmethod
    def setUpTestData(cls):
        UserTestsData.setUpTestData()
        cls.token = Token.objects.create(user=cls.user)

        # Creating genre, author and book
        cls.fiction_genre = Genre.objects.create(genre_name="Fiction")
        cls.fiction_author = Author.objects.create(author_name="Stephen King")
        cls.book = Book.objects.create(
            title="Test Book",
            ISBN="1234567890",
            description="This is a test book.",
            condition="Brand New",
            retrieval_location="Test Location",
            owner=cls.user,
        )

        # Setting genre and author to book
        cls.book.genre.add(cls.fiction_genre)
        cls.book.author.add(cls.fiction_author)

        cls.data_for_update = {
            "title": "Updated Title",
            "author": ["Stan Lee", "Charles Dickens"],
            "genre": ["Comics", "History"],
            "ISBN": "11111111",
            "retrieval_location": "Updated Location",
            "description": "Updated description",
        }

        cls.book_detail_url = reverse("books-detail", kwargs={"pk": cls.book.pk})

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_book_detail(self):
        response = self.client.get(self.book_detail_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), self.book.title)
        self.assertEqual(
            response.data.get("genre"),
            [genre.genre_name for genre in self.book.genre.all()],
        )

    def test_detail_for_nonexisting_book(self):
        non_existing_pk = "00000000-0000-0000-0000-000000000000"
        response = self.client.get(
            reverse("books-detail", kwargs={"pk": non_existing_pk}),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_with_unauthenticated_user(self):
        """
        In books/permissions.py I created IsAuthorOrReadOnly permission
        class where I am allowing unauthenticated users to have a read-only.
        this test will test that users do not get 404 when simply accessing
        individual books to just view them.
        """

        client = self.client_class()
        response = client.get(self.book_detail_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_with_PUT(self):
        response = self.client.put(
            self.book_detail_url,
            self.data_for_update,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")
        self.assertEqual(self.book.description, "Updated description")
        self.assertEqual(
            [genre.genre_name for genre in self.book.genre.all()], ["Comics", "History"]
        )

    def test_update_with_PATCH(self):
        # Sending only partial data
        self.data_for_update = {
            "title": "Yet again updated title",
            "genre": ["Comics", "History", "Thriller"],
            "author": ["Stan Lee", "Charles Dickens", "Stephen King"],
        }
        response = self.client.patch(
            self.book_detail_url,
            self.data_for_update,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Yet again updated title")
        self.assertEqual(
            [genre.genre_name for genre in self.book.genre.all()],
            ["Comics", "History", "Thriller"],
        )
        # Using sorted function because the ordering of both of these lists was different.
        self.assertEqual(
            sorted([author.author_name for author in self.book.author.all()]),
            sorted(["Stan Lee", "Charles Dickens", "Stephen King"]),
        )

    def test_update_with_unauthenticated_user(self):
        client = self.client_class()
        # Testing for PUT request
        response_for_PUT = client.put(
            self.book_detail_url,
            self.data_for_update,
            format="json",
        )
        self.assertEqual(response_for_PUT.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(Book.objects.last().author, self.data_for_update["author"])

        # Testing for PATCH request
        self.data_for_update = {"title": "Yet again updated title"}
        response_for_PATCH = client.patch(
            self.book_detail_url,
            self.data_for_update,
            format="json",
        )
        self.assertEqual(response_for_PATCH.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(Book.objects.last().title, self.data_for_update["title"])

    def test_update_with_nonauthor_user(self):
        non_author_user = get_user_model().objects.create_user(
            email="non_author_user@email.com", password="non_author_test_pass"
        )
        non_author_user_token = Token.objects.create(user=non_author_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {non_author_user_token.key}")

        # Testing for PUT request
        response_for_PUT = self.client.put(
            self.book_detail_url,
            self.data_for_update,
            format="json",
        )

        self.assertEqual(response_for_PUT.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Book.objects.last().title, self.data_for_update["title"])

        # Testing for PATCH request
        self.data_for_update = {"title": "Yet again updated title"}
        response_for_PATCH = self.client.patch(
            self.book_detail_url,
            self.data_for_update,
            format="json",
        )
        self.assertEqual(response_for_PATCH.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Book.objects.last().title, self.data_for_update["title"])

    def test_update_with_invalid_data(self):
        # Testing for PUT request
        self.data_for_update["title"] = ""
        response_for_PUT = self.client.put(
            self.book_detail_url,
            self.data_for_update,
            format="json",
        )

        self.assertEqual(response_for_PUT.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(Book.objects.last().title, "")

        # Testing for PATCH request
        self.data_for_update = {"title": ""}
        response_for_PUT = self.client.patch(
            self.book_detail_url,
            self.data_for_update,
            format="json",
        )

        self.assertEqual(response_for_PUT.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(Book.objects.last().title, "")

    def test_update_with_nonexisting_book(self):
        non_existing_pk = "00000000-0000-0000-0000-000000000000"
        response_for_PUT = self.client.put(
            reverse("books-detail", kwargs={"pk": non_existing_pk}),
            self.data_for_update,
            format="json",
        )

        self.assertEqual(response_for_PUT.status_code, status.HTTP_404_NOT_FOUND)

        self.data_for_update = {"title": "Yet again updated title"}
        response_for_PATCH = self.client.patch(
            reverse("books-detail", kwargs={"pk": non_existing_pk}),
            self.data_for_update,
            format="json",
        )
        self.assertEqual(response_for_PATCH.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_book(self):
        response = self.client.delete(self.book_detail_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_nonexisting_book(self):
        non_existing_pk = "00000000-0000-0000-0000-000000000000"
        response = self.client.delete(
            reverse("books-detail", kwargs={"pk": non_existing_pk}),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_with_unauthenticated_user(self):
        # new instance of the self.client without credentials.
        client = self.client_class()
        response = client.delete(
            self.book_detail_url,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_with_nonauthor_user(self):
        non_author_user = get_user_model().objects.create_user(
            email="non_author_user@email.com", password="non_author_test_pass"
        )
        non_author_user_token = Token.objects.create(user=non_author_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {non_author_user_token.key}")

        response = self.client.delete(
            self.book_detail_url,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 1)


class GenreListViewTests(APITestCase, UserTestsData):
    @classmethod
    def setUpTestData(cls):
        UserTestsData.setUpTestData()
        cls.token = Token.objects.create(user=cls.user)

        # Creating genres
        for num in range(1, 11):
            Genre.objects.create(genre_name=f"Genre {num}")
        cls.genre_list_url = reverse("genres-list")

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_genre_listing(self):
        response = self.client.get(self.genre_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_genre_list_with_unauthenticated_user(self):
        client = self.client_class()
        response = client.get(self.genre_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)


class AuthorListViewTests(APITestCase, UserTestsData):
    @classmethod
    def setUpTestData(cls):
        UserTestsData.setUpTestData()
        cls.token = Token.objects.create(user=cls.user)

        # Creating Authors
        for num in range(1, 11):
            Author.objects.create(author_name=f"author {num}")
        cls.author_list_url = reverse("authors-list")

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_author_listing(self):
        response = self.client.get(self.author_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_author_list_with_unauthenticated_user(self):
        client = self.client_class()
        response = client.get(self.author_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)
