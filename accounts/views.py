from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from accounts.serializers import SignUpSerializer


class SignUpAPIView(CreateAPIView):
    """
    **User Registration API Endpoint**

    This endpoint allows users to register by providing their email and password. After a successful registration, a new user account is created.

    **Authentication:** No authentication is required to access this endpoint.

    **Request Parameters:**

    - `email`: The email address of the user.
    - `password`: The password for the user account.

    **Response:**
    - A successful registration will result in an HTTP response with status code 201 (Created).
    - The response will include a message indicating successful registration, along with the user's unique identifier (user_id).
    """

    serializer_class = SignUpSerializer
    permission_classes = [
        AllowAny,
    ]
