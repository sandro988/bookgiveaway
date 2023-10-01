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
        additional_information (str): Additional information or like a comment to the owner provided by the requester when making the request.
        created_at (DateTimeField): The date and time when the booking request was created.
        updated_at (DateTimeField): The date and time when the booking request was last updated.

    Methods:
        __str__: Returns a string representation of the booking request, including the book title, requester's email and ID.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    requester = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    additional_information = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking request for {self.book.title} by {self.requester.email} with the id {self.requester.id}."


class Notification(models.Model):
    """
    Model for Notifications that users receive when book owner either approves their booking request or rejects.

    Attributes:
        user (ForeignKey): The user to whom the notification is addressed.
        book (str): The title of the book.
        approved (bool): Indicates whether the booking request was approved (True) or rejected (False).
        retrieval_location (str, optional): The location from which the user can retrieve the book (if approved).
        created_at (DateTimeField): The date and time when the notification was created.

    Methods:
        __str__(): Returns a human-readable representation of the notification.

    Example:
        "Notification for sandro_nadiradze@example.com: Request Approved"
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)
    retrieval_location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email}: Request {'Approved' if self.approved else 'Rejected'}"
