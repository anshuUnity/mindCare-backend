from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 
            'title', 
            'author', 
            'description', 
            'published_date', 
            'isbn', 
            'language', 
            'pages', 
            'tag', 
            'cover_image', 
            'file',
            'is_available'
        ]
