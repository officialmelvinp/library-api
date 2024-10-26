from django.contrib import admin
from .models import Book

# Register the Product model in the Django admin site
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Display fields in the admin list view
    list_display = ['id', 'title']
    # Add a search box to filter products by name
    search_fields = ['title']
    # Add filters to the right side for easier navigation (if needed in the future)
    list_filter = ['title']
