from .models import BookingRequest


def process_booking_request(instance: BookingRequest, approve: bool) -> None:
    """
    Process a booking request based on approval status.

    This function updates the status of a booking request and, if approved,
    assigns the book to the requester, marks it as unavailable, and deletes
    all other pending booking requests for the same book.
    If rejected(user passes False as a value), the booking request will be deleted.

    Args:
        instance (BookingRequest): The booking request to process.
        approve (bool): A boolean indicating whether to approve or reject
        the booking request. True for approval, False for rejection.

    Returns:
        None: This function does not return a value. it just modifies the database
        and objects in place.
    """

    if approve:
        instance.book.owner = instance.requester
        instance.book.available = False
        instance.book.save()
        every_book_request = BookingRequest.objects.filter(
            book=instance.book,
        )
        every_book_request.delete()
    else:
        instance.delete()
