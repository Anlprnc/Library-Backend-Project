from rest_framework import serializers
from books.models import Book, Publisher, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'builtIn']


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'isbn', 'author', 'publisher', 'category', 'shelfCode', 'featured']
        
        
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'builtIn']