from django.urls import path
from .views import BookingRequestCreateView, BookingRequestDetailView

urlpatterns = [
    path("", BookingRequestCreateView.as_view(), name="booking-requests-create"),
    path(
        "<uuid:pk>/", BookingRequestDetailView.as_view(), name="booking-requests-detail"
    ),
]
