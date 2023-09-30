from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import BookingRequestSerializer, RetrieveUpdateDeleteBookingRequestSerializer
from .permissions import IsRequesterOrOwnerRetrieveOnly
from .models import BookingRequest


class BookingRequestCreateView(CreateAPIView):
    """
    **Booking Request Creation API Endpoint**

    This view allows users to create booking requests for specific books. Users can request a book
    from the owner by providing details such as the book to request and optional additional information.
    This information can be for example a comment to the owner of the book.

    **Authentication:**
    - Authentication is required for creating booking requests. **ONLY** authenticated users can make requests.
    - The requesting user is automatically set in **perform_create()** method.

    **Supported Operations:**

    - `create`: Create a new booking request. Owner of a book can not create a booking request to their own books.

    **Fields:**

    - `book`: The book to request. You should provide the unique ID(UUID) of the book.
    - `additional_information`: Additional information such as comments for the booking request (optional).

    **Responses:**

    - Successful request creation will return a status code **201 (Created)** with the booking request details
    and fields such as: **id**, **book**, **requester**, **status**, **request_selected**, **created_at**, **updated_at**.
    - Duplicate booking requests will return a status code **400 (Bad Request)**.
    - Unauthenticated users will receive a status code **401 (Unauthorized)** and the booking request will not be created.
    - Invalid or incomplete data will result in a status code **400 (Bad Request)**.
    """

    serializer_class = BookingRequestSerializer

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)


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
