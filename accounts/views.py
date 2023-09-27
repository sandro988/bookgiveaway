from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from accounts.serializers import SignUpSerializer


class SignUpAPIView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [
        AllowAny,
    ]
