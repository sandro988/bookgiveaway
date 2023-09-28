from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "owner",
        "author",
        "genre",
        "condition",
        "location",
        "available",
    ]


admin.site.register(Book, BookAdmin)
