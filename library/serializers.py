from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'url', 'id', 'title', 'author', 'genre', 'publication_date', 
            'status', 'edition', 'summary', 'borrowed_by', 
            'borrow_date', 'return_date'
        ]