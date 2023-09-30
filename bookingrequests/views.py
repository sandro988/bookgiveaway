from rest_framework.generics import CreateAPIView
from .serializers import BookingRequestSerializer


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

    - `create`: Create a new booking request.

    **Fields:**

    - `book`: The book to request. You should provide the unique ID(UUID) of the book.
    - `additional_information`: Additional information such as comments for the booking request (optional).

    **Responses:**

    - Successful request creation will return a status code 201 (Created) with the booking request details
    and fields such as: **id**, **book**, **requester**, **status**, **request_selected**, **created_at**, **updated_at**.
    - Duplicate booking requests will return a status code 400 (Bad Request).
    - Unauthenticated users will receive a status code 401 (Unauthorized) and the booking request will not be created.
    - Invalid or incomplete data will result in a status code 400 (Bad Request).
    """

    serializer_class = BookingRequestSerializer

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)
