from rest_framework import permissions


class IsRequesterOrOwnerRetrieveOnly(permissions.BasePermission):
    """
    Custom Permission for BookingRequestDetailView

    This permission class makes sure that only authenticated users can have permission to access the BookingRequestDetailView.
    Also only the requesters of booking requests can update and delete their booking requests. Owners of the books can just retrieve
    booking requests and view them but they can not delete or update them.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method == "GET" and obj.book.owner == user:
            return True

        return obj.requester == user


class IsBookOwner(permissions.BasePermission):
    """
    Custom permission to check if the user making a request is the owner of the book associated with the booking request.
    This permission class ensures that only owner of a book can manage booking requests.
    """

    def has_object_permission(self, request, view, obj):
        return obj.book.owner == request.user


class NotificationBelongsToUser(permissions.BasePermission):
    """
    Custom permission to check if the user making a request is the owner/receiver of the notication.
    This permission class ensures that only this user can manage notifications.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
