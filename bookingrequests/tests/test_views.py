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


class BookingRequestsDetailTestClass(APITestCase, UserTestsData):
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

        # Creating booking request.
        cls.booking_request = BookingRequest.objects.create(
            book=cls.book,
            additional_information="I would like to request your book.",
            requester=cls.requester_user,
        )

        # Data for updating booking requests.
        cls.another_book = Book.objects.create(
            title="Another Test Book",
            ISBN="0987654321",
            retrieval_location="Test Location",
            owner=cls.user,
        )
        cls.book.genre.add(cls.genre)
        cls.book.author.add(cls.author)

        cls.data_for_update = {
            "book": cls.another_book.id,
            "additional_information": "I want to request your book.",
        }

        # URLs that I will use in test cases.
        cls.booking_request_url = reverse(
            "booking-requests-detail", kwargs={"pk": cls.booking_request.id}
        )

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.requester_token.key}")

    def test_retrieve_booking_request(self):
        response = self.client.get(self.booking_request_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BookingRequest.objects.count(), 1)
        self.assertEqual(response.data["requester"], self.requester_user.id)
        self.assertEqual(response.data["book"], self.book.id)
        self.assertEqual(response.data["status"], "Pending")
        self.assertEqual(response.data["request_selected"], False)
        self.assertEqual(
            response.data["additional_information"],
            "I would like to request your book.",
        )

    def test_retrieve_nonexistant_booking_request(self):
        non_existing_pk = "00000000-0000-0000-0000-000000000000"
        response = self.client.get(
            reverse("booking-requests-detail", kwargs={"pk": non_existing_pk}),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_booking_request_with_unauthenticated_user(self):
        # Creating a new instance of the self.client without authentication credentials.
        client = self.client_class()
        response = client.get(self.booking_request_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_booking_request_with_nonauthor_user(self):
        # Creating completely new user and token.
        User = get_user_model()
        another_user = User.objects.create_user(
            email="another_requester@email.com", password="another_requester_pass"
        )
        token = Token.objects.create(user=another_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        # Trying to access booking request that does not belong to this user.
        response = self.client.get(self.booking_request_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_booking_request_with_book_owner(self):
        # 'user' is created in UserTestsData class that I am using as a parent for this test class.
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        # Trying to access booking request as a book owner.
        # Owner should be able to just retrive information about booking requests.
        response = self.client.get(self.booking_request_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["requester"], self.requester_user.id)
        self.assertEqual(response.data["book"], self.book.id)
        self.assertEqual(response.data["status"], "Pending")
        self.assertEqual(response.data["request_selected"], False)
        self.assertEqual(
            response.data["additional_information"],
            "I would like to request your book.",
        )

    def test_update_booking_request_with_PUT(self):
        response = self.client.put(self.booking_request_url, self.data_for_update)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Checking that no new book request was added.
        self.assertEqual(BookingRequest.objects.count(), 1)

        # Checking that requested book was changed to another_book.
        self.assertEqual(BookingRequest.objects.last().book, self.another_book)

        # Checking that both fields were updated.
        self.assertEqual(
            BookingRequest.objects.last().additional_information,
            "I want to request your book.",
        )

    def test_update_booking_request_with_PATCH(self):
        # Sending partial data by poping book from the dictionary and leaving only additional_information.
        self.data_for_update.pop("book")

        # Testing for PATCH request
        response = self.client.patch(self.booking_request_url, self.data_for_update)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Checking that no new book request was added.
        self.assertEqual(BookingRequest.objects.count(), 1)

        # Checking that requested book was not changed.
        self.assertEqual(BookingRequest.objects.last().book, self.book)

        # Checking that additional_information was changed.
        self.assertEqual(
            BookingRequest.objects.last().additional_information,
            "I want to request your book.",
        )

    def test_update_nonexistant_booking_request(self):
        non_existing_pk = "00000000-0000-0000-0000-000000000000"

        # Testing for PUT request
        response = self.client.put(
            reverse("booking-requests-detail", kwargs={"pk": non_existing_pk}),
            self.data_for_update,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Testing for PATCH request
        response = self.client.patch(
            reverse("booking-requests-detail", kwargs={"pk": non_existing_pk}),
            self.data_for_update,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_booking_request_with_unauthenticated_user(self):
        client = self.client_class()

        # Testing for PUT request
        response = client.put(
            self.booking_request_url, self.data_for_update, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        booking_request_obj = BookingRequest.objects.last()
        self.assertNotEqual(booking_request_obj.book, self.data_for_update["book"])
        self.assertNotEqual(
            booking_request_obj.additional_information,
            self.data_for_update["additional_information"],
        )

        # Testing for PATCH request
        self.data_for_update.pop("book")
        response = client.patch(
            self.booking_request_url, self.data_for_update, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        booking_request_obj = BookingRequest.objects.last()
        self.assertNotEqual(
            booking_request_obj.additional_information,
            self.data_for_update["additional_information"],
        )

    def test_update_booking_request_with_nonauthor_user(self):
        # Creating completely new user and token.
        User = get_user_model()
        another_user = User.objects.create_user(
            email="another_requester@email.com", password="another_requester_pass"
        )
        token = Token.objects.create(user=another_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        # Trying to change booking request that does not belong to this user with PUT request.
        response = self.client.put(
            self.booking_request_url, self.data_for_update, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        booking_request_obj = BookingRequest.objects.last()
        self.assertNotEqual(booking_request_obj.book, self.data_for_update["book"])
        self.assertNotEqual(
            booking_request_obj.additional_information,
            self.data_for_update["additional_information"],
        )

        # Trying to change booking request that does not belong to this user with PATCH request.
        self.data_for_update.pop("book")
        response = self.client.patch(
            self.booking_request_url, self.data_for_update, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        booking_request_obj = BookingRequest.objects.last()
        self.assertNotEqual(
            booking_request_obj.additional_information,
            self.data_for_update["additional_information"],
        )

    def test_update_booking_request_with_book_owner(self):
        # Book owner should not be able to update other users booking requests.
        # Book owner can only retrieve details about booking requests.

        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        # Trying to change booking request as a book owner.
        response = self.client.put(
            self.booking_request_url, self.data_for_update, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_booking_request(self):
        # Deleting booking request by the requester user
        response = self.client.delete(self.booking_request_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BookingRequest.objects.count(), 0)

    def tets_delete_booking_request_by_nonauthor_user(self):
        # Deleting booking request by some other user.
        User = get_user_model()
        another_user = User.objects.create_user(
            email="another_requester@email.com", password="another_requester_pass"
        )
        token = Token.objects.create(user=another_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        # This user should not have the permission to delete other users booking request.
        response = self.client.delete(self.booking_request_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(BookingRequest.objects.count(), 1)

    def test_delete_booking_request_by_unauthenticated_user(self):
        # Unauthenticated user should not have the permission to delete other users booking requests.
        client = self.client_class()
        response = client.delete(self.booking_request_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(BookingRequest.objects.count(), 1)

    def test_delete_booking_request_by_book_owner(self):
        # Book owners should not have the permission to delete the booking requests of other users.

        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.delete(self.booking_request_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(BookingRequest.objects.count(), 1)

    def test_delete_nonexisting_booking_request(self):
        non_existing_pk = "00000000-0000-0000-0000-000000000000"
        response = self.client.delete(
            reverse("booking-requests-detail", kwargs={"pk": non_existing_pk}),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
