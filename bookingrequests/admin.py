from django.contrib import admin
from .models import BookingRequest


class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ("book", "requester", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("book__title", "requester__email")


admin.site.register(BookingRequest, BookingRequestAdmin)
