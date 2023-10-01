from rest_framework import serializers
from .models import BookingRequest, Notification


class BookingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRequest
        fields = "__all__"
        read_only_fields = [
            "owner",
            "requester",
            "status",
        ]

    def validate(self, data):
        """
        Custom validation to ensure that:
        - Users can not create duplicate booking requests.
        - The book owner cannot request their own book.
        - Users can not create booking requests for books with `available` field set to False.

        """
        book = data["book"]
        requester = self.context["request"].user
        available = book.available

        if BookingRequest.objects.filter(book=book, requester=requester).exists():
            raise serializers.ValidationError("You have already requested this book.")

        if book.owner == requester:
            raise serializers.ValidationError("You cannot request your own book.")

        if not available:
            raise serializers.ValidationError(
                "This book is not available at this moment."
            )

        return data


class RetrieveUpdateDeleteBookingRequestSerializer(serializers.ModelSerializer):
    book_owner_id = serializers.ReadOnlyField(source="book.owner.id")
    book_owner_email = serializers.ReadOnlyField(source="book.owner.email")
    book_title = serializers.ReadOnlyField(source="book.title")

    class Meta:
        model = BookingRequest
        fields = "__all__"
        read_only_fields = [
            "requester",
            "status",
        ]


class ManageBookingRequestSerializer(serializers.Serializer):
    approve = serializers.BooleanField(required=True)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
