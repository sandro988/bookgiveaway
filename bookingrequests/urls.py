from django.urls import path
from .views import (
    BookingRequestListCreateView,
    BookingRequestDetailView,
    ManageBookingRequestView,
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
]
