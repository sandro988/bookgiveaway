import uuid
from django.contrib.auth import get_user_model
from django.db import models
from books.models import Book


class BookingRequest(models.Model):
    """
    Model for booking requests made by users who would like to request a book from the owner.

    Model Fields:
        book (ForeignKey): The book being requested.
        requester (ForeignKey): The user making the booking request.
        status (str): The current status of the booking request (either "Pending", "Approved", "Rejected" or "Canceled)."
        request_selected (bool): Indicates whether the request has been selected by the book owner (either True or False).
        additional_information (str): Additional information or like a comment to the owner provided by the requester when making the request.
        created_at (DateTimeField): The date and time when the booking request was created.
        updated_at (DateTimeField): The date and time when the booking request was last updated.

    Methods:
        __str__: Returns a string representation of the booking request, including the book title, requester's email and ID.
    """

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Canceled", "Canceled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    requester = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )
    request_selected = models.BooleanField(default=False)
    additional_information = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking request for {self.book.title} by {self.user} with the id {self.user.id}."
