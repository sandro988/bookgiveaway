from django.contrib import admin
from .models import Book, Genre


class BookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "owner",
        "author",
        # "genre",
        "condition",
        "retrieval_location",
        "available",
    ]


admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
