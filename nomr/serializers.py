from rest_framework import serializers
from nomr.models import Book, BookPart, Page

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'uuid',
            'title',
            'description',
            'is_manuscript',
            'printers',
            'publication_date',
            'location',
            'printing_technology',
            'genre',
            'is_sacred',
            'alternate_id'
        )

class BookPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookPart
        fields = ('uuid', 'book', 'part_type')

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'uuid', 
            'book_part',
            'image',
            'image_width',
            'image_height',
            'mei',
            'sequence'
        )
