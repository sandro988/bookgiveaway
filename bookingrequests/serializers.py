from rest_framework import serializers
from .models import BookingRequest


class BookingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRequest
        fields = "__all__"
        read_only_fields = [
            "owner",
            "requester",
            "status",
            "request_selected",
        ]
        extra_kwargs = {"request_selected": {"default": False}}

    def validate(self, data):
        """
        Custom validation to ensure the owner cannot request their own book.
        """
        book = data["book"]
        requester = self.context["request"].user

        existing_request = BookingRequest.objects.filter(
            book=book, requester=requester
        ).exists()

        if existing_request:
            raise serializers.ValidationError("You have already requested this book.")

        if book.owner == requester:
            raise serializers.ValidationError("You cannot request your own book.")

        return data
