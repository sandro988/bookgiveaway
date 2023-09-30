from django.contrib import admin
from .models import Book, Genre


class BookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "owner",
        "condition",
        "available",
        "retrieval_location",
    ]


admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
