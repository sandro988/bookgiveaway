from django.urls import path
from .views import (
    BookingRequestListCreateView,
    BookingRequestDetailView,
    ManageBookingRequestView,
    NotificationListView,
    NotificationDetailView,
)

urlpatterns = [
    path(
        "",
        BookingRequestListCreateView.as_view(),
        name="booking-requests-list-create",
    ),
    path(
        "<uuid:pk>/",
        BookingRequestDetailView.as_view(),
        name="booking-requests-detail",
    ),
    path(
        "manage/<uuid:pk>/",
        ManageBookingRequestView.as_view(),
        name="manage-booking-request",
    ),
    path(
        "notifications/",
        NotificationListView.as_view(),
        name="booking-notifications",
    ),
    path(
        "notifications/<int:pk>/",
        NotificationDetailView.as_view(),
        name="booking-notification-details",
    ),
]
