from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    BookingRequestSerializer,
    RetrieveUpdateDeleteBookingRequestSerializer,
    ManageBookingRequestSerializer,
)
from .permissions import IsRequesterOrOwnerRetrieveOnly, IsBookOwner
from .models import BookingRequest
from .utils import process_booking_request
from .models import Notification


class BookingRequestListCreateView(ListCreateAPIView):
    """
    **Booking Request List and Creation API Endpoint**

    This view allows users to create booking requests for specific books and retrieve a list
    of their existing booking requests. Users can request a book from the owner by providing details
    such as the book to request and optional additional information, which can be a comment to the owner of the book.

    **Authentication:**

    - Authentication is required for creating booking requests.
    - **ONLY** authenticated users can make requests.
    - The requesting user is automatically set in the **perform_create()** method and thus when a user creates a booking
    request they do not need to enter their id, email, or any other identifying field.

    **Supported Operations:**

    - `create`: Create a new booking request. Owners of a book cannot create a booking request for their own books.
    - `list`: Retrieve a list of booking requests for books owned by the user.

    **Fields:**

    - `book`: The book to request. You should provide the unique ID(UUID) of the book.
    - `additional_information`: Additional information such as comments for the booking request (optional).

    **Create Responses:**

    - Successful request creation will return a status code **201 (Created)** with the booking request details
    and fields such as: **id**, **book**, **requester**, **status**, **request_selected**, **created_at**, **updated_at**.
    - Duplicate booking requests will return a status code **400 (Bad Request)**.
    - Unauthenticated users will receive a status code **401 (Unauthorized)** and the booking request will not be created.
    - Invalid or incomplete data will result in a status code **400 (Bad Request)**.

    **List Response:**

    - If a user who accesses this endpoint does not have any booking requests for their books, a status code of **204 (No Content)**
    is returned, indicating that no booking requests exist.
    - If users have one or more booking requests, a status code of **200 (OK)** is returned, along with a list of booking requests
    in the response body.
    """

    serializer_class = BookingRequestSerializer

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return BookingRequest.objects.filter(book__owner=user)

        return BookingRequest.objects.none()

    def list(self, request, *args, **kwargs):
        """
        If a user who accesses this endpoint does not have any booking requests for their books,
        I am returning a status code of 204 (No Content).

        Alternatively, If users have one or more booking requests, a status code of 200 (OK) is returned
        with a list of booking requests in the response body.
        """
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingRequestDetailView(RetrieveUpdateDestroyAPIView):
    """
    **API Endpoint for Retrieving, Updating and Deleting Booking Requests.**

    This view allows users to retrieve, update, or delete specific booking requests. Users can only
    retrieve their own booking requests or booking requests associated with books they own.
    Owners of the books can retrieve booking requests for their books BUT cannot update or delete them.

    **Authentication:**

    - Authentication is required for all type of requests.
    - Owners of the books can only retrieve booking requests associated with **ONLY** their books,
    meaning that they can not retrieve and view other book owners booking requests.

    **Supported Operations:**

    - `retrieve`: Retrieve details of a specific booking request.
    - `update`: Update the details of a specific booking request. Only the requester can update their booking requests.
    - `partial_update`: Partially update the details of a specific booking request. Only the requester can update their booking requests.
    - `destroy`: Delete a specific booking request. Only the requester can delete their booking requests.

    **Request Body:**

    - Retrieve (GET) does not require a request body.
    - Update (PUT) or Partial Update (PATCH) requires the following fields:
        - `book_id`: The unique ID of the book associated with the booking request. This field is required in PUT request but optional in PATCH.
        - `additional_information`: Additional information or comments for the booking request. This field is optional.
    - Delete (DELETE) does not require a request body.

    **Response Body:**

    - `book_id`: The unique ID of the book associated with the booking request.
    - `book_owner_id`: The unique ID of the owner of the associated book. (read-only).
    - `book_owner_email`: The email address of the owner of the associated book (read-only).
    - `book_title`: The title of the associated book (read-only).
    - `requester`: The user who made the booking request (read-only).
    - `status`: The status of the booking request.
    - `request_selected`: Indicates if the booking request is selected by the book owner.
    - `additional_information`: Additional information or comments for the booking request.
    - `created_at`: Information about date and time when booking request was created.
    - `updated_at`: Information about data and time when booking request was last updated.

    **Responses:**

    - Successful retrieve operation will return status code **200 (OK)**.
    - Successful update operation will return status code **200 (OK)**.
    - Successful delete operation will return status code **204 (No Content)**.
    - Unauthenticated users will receive a status code **401 (Unauthorized)**.
    - If users try to delete other users booking requests they will receive a status code **403 (Bad Request)**
    """

    serializer_class = RetrieveUpdateDeleteBookingRequestSerializer
    permission_classes = (IsRequesterOrOwnerRetrieveOnly,)
    queryset = BookingRequest.objects.all()


class ManageBookingRequestView(UpdateAPIView):
    """
    **API Endpoint for Managing Booking Requests.**

    This view allows owners of books to manage booking requests for their books. Owners can approve or reject booking
    requests, which affects the book's status and potentially deletes other pending requests for the same book.

    If the book owner approves a request:
    - The user who made the booking request becomes the new owner of the book.
    - The book's availability is set to False.
    - All other pending booking requests for the same book are deleted.

    If the book owner rejects a request:
    - the request is simply deleted.

    **Authentication:**

    - Authentication is required for making a request.
    - Only owners of the books associated with the booking requests can perform management actions.

    **Supported Operations:**

    - `update (PUT)`: Allows book owners to approve or reject booking requests from users.

    **Request Body:**

    - Update (PUT) requires the following fields:
        - `approve` (boolean): Indicates whether to approve (True) or reject (False) the booking request.

    **Responses:**

    - Successful management actions will return status code 200 (OK).
    - Unauthenticated users will receive a status code 401 (Unauthorized).
    - Users who are not owners of the associated book will receive a status code 403 (Forbidden).
    - If the user does not pass a boolean value in the request, they will receive a status code 400 (Bad Request).
    - Notifications are created to inform the user whose booking request was approved or rejected.

    Notifications:
    - If the booking request is approved, a notification is created with details about the book's retrieval location, title and etc.
    - If the booking request is rejected, a notification is created to inform the user about the rejection, in this case,
    retrieval location will not be included in the notification.
    """

    # Only one required value is being passed, so there is no need for partial updates.
    http_method_names = ["put"]
    queryset = BookingRequest.objects.all()
    serializer_class = ManageBookingRequestSerializer
    permission_classes = [IsBookOwner]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            approve = serializer.validated_data.get("approve")
            if approve:
                Notification.objects.create(
                    user=instance.requester,
                    book=instance.book,
                    approved=True,
                    retrieval_location=instance.book.retrieval_location,
                )
            else:
                Notification.objects.create(
                    user=instance.requester,
                    book=instance.book,
                    approved=False,
                )
            process_booking_request(instance, approve)

            instance.book.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
