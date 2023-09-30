from django.urls import path
from .views import BookingRequestCreateView

urlpatterns = [
    path("", BookingRequestCreateView.as_view(), name="booking-requests-create"),
]
