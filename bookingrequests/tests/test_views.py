from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from books.tests.test_views import UserTestsData
from bookingrequests.models import BookingRequest
from books.models import Book, Genre, Author


class CreateBookingRequestsTestClass(APITestCase, UserTestsData):
    @classmethod
    def setUpTestData(cls):
        UserTestsData.setUpTestData()

        # This user will request the book after we create it.
        requester_user = get_user_model()
        cls.requester_user = requester_user.objects.create_user(
            email="requester_test_user@email.com", password="requester_test_pass"
        )
        cls.requester_token = Token.objects.create(user=cls.requester_user)

        # Creating genre, author and book.
        cls.genre = Genre.objects.create(genre_name="Fiction")
        cls.author = Author.objects.create(author_name="Stephen King")
        cls.book = Book.objects.create(
            title="Test Book",
            ISBN="1234567890",
            description="This is a test book.",
            condition="Brand New",
            retrieval_location="Test Location",
            owner=cls.user,
        )

        # Setting genre and author to book.
        cls.book.genre.add(cls.genre)
        cls.book.author.add(cls.author)

        # Data that I will use when creating booking request.
        cls.booking_request_data = {
            "book": cls.book.id,
            "additional_information": "I would like to request your book.",
        }

        cls.booking_request_create_url = reverse("booking-requests-create")

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.requester_token.key}")

    def test_create_booking_request(self):
        response = self.client.post(
            self.booking_request_create_url,
            self.booking_request_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookingRequest.objects.count(), 1)
        booking_request = BookingRequest.objects.last()
        self.assertEqual(booking_request.requester, self.requester_user)
        self.assertEqual(booking_request.book, self.book)
        self.assertEqual(booking_request.status, "Pending")
        self.assertEqual(booking_request.request_selected, False)
        self.assertEqual(
            booking_request.additional_information, "I would like to request your book."
        )

    def test_create_duplicate_booking_request(self):
        # Initial request.
        response = self.client.post(
            self.booking_request_create_url,
            self.booking_request_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookingRequest.objects.count(), 1)

        # Second request trying to create the same request.
        response = self.client.post(
            self.booking_request_create_url,
            self.booking_request_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BookingRequest.objects.count(), 1)

    def test_create_booking_request_with_unauthenticated_user(self):
        # I am creating a new instance of the self.client without authentication credentials.
        client = self.client_class()
        response = client.post(
            self.booking_request_create_url, self.booking_request_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(BookingRequest.objects.count(), 0)

    def test_create_booking_with_empty_fields(self):
        self.booking_request_data["book"] = ""
        self.booking_request_data["book_description"] = ""
        response = self.client.post(
            self.booking_request_create_url,
            self.booking_request_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BookingRequest.objects.count(), 0)

    def test_book_owner_can_not_request_book(self):
        # Creating token and signing in the user that created the book.
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        # Trying to request booking for the book by the owner of the book.
        response = self.client.post(
            self.booking_request_create_url,
            self.booking_request_data,
            format="json",
        )

        # Owner of the book should not be able to create booking of his own book.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BookingRequest.objects.count(), 0)
