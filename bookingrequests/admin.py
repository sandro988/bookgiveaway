from django.contrib import admin
from .models import BookingRequest
from .models import Notification


class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ("book", "requester", "id", "created_at")
    search_fields = ("book__title", "requester__email")


admin.site.register(BookingRequest, BookingRequestAdmin)
admin.site.register(Notification)
