from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from books.models import Book, Publisher, Author
from .serializers import BooksSerializer, PublisherSerializer, AuthorSerializer
from rest_framework.response import Response

# ----- AUTHORS -----
# Author List View
class AuthorListView(generics.ListAPIView):
    serializer_class = AuthorSerializer
    
    def get_queryset(self):
        page = self.request.query_params.get('page', 0)
        size = self.request.query_params.get('size', 20)
        sort = self.request.query_params.get('sort', 'name')
        type = self.request.query_params.get('type', 'asc')
        
        if sort not in [field.name for field in Author._meta.fields]:
            sort = 'name'
        
        if type not in ['asc', 'desc']:
            type = 'asc'
        
        queryset = Author.objects.all().order_by(f'{type}{sort}')
        
        start = int(page) * int(size)
        end = start + int(size)
        
        return queryset[start:end]
    
# Author Create View
class AuthorCreateView(generics.CreateAPIView):
    serializer_class = AuthorSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
# Author Detail View
class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorSerializer
    
    def get_queryset(self):
        return Author.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.books.exists():
            return Response({'error': 'Author has related books, cannot be deleted'}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# ----- BOOKS -----
# Book List View
class BookListView(generics.ListAPIView):
    serializer_class = BooksSerializer
    
    def get_queryset(self):
        q = self.request.query_params.get('q')
        cat = self.request.query_params.get('cat')
        author = self.request.query_params.get('author')
        publisher = self.request.query_params.get('publisher')
        page = self.request.query_params.get('page', 0)
        size = self.request.query_params.get('size', 20)
        sort = self.request.query_params.get('sort', 'name')
        type = self.request.query_params.get('type', 'asc')
        
        queryset = Book.objects.filter(active=True)
        
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(isbn__icontains=q) |
                Q(author__name__icontains=q) |
                Q(publisher__name__icontains=q)
            )
            
        if cat:
            queryset = queryset.filter(category=cat)
            
        if author:
            queryset = queryset.filter(author=author)
            
        if publisher:
            queryset = queryset.filter(publisher=publisher)
            
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            queryset = queryset.filter(loanable=True)
            
        queryset = queryset.order_by(f'{sort}' if type == 'asc' else f'-{sort}')
        
        return queryset[int(page) * int(size): int(page + 1) * int(size)]
    
# Book Create View  
class BookCreateView(generics.CreateAPIView):
    serializer_class = BooksSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
# Book Detail View
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BooksSerializer
    
    def get_queryset(self):
        return Book.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partail=True)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        serializer.save()
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.loan_set.exists():
            return Response({'error': 'Book has related loan records, cannot be deleted'}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# ----- PUBLISHERS -----
# Publisher List View
class PublisherListView(generics.ListAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    
    def get_queryset(self):
        page = self.request.query_params.get('page', 0)
        size = self.request.query_params.get('size', 20)
        sort = self.request.query_params.get('sort', 'name')
        type = self.request.query_params.get('type', 'asc')
        
        queryset = super().get_queryset()
        
        if sort not in [field.name for field in Publisher._meta.fields]:
            sort = 'name'
            
        if type not in ['asc', 'desc']:
            type = 'asc'
            
        queryset = queryset.order_by(f'{type}{sort}')
        
        start = int(page) * int(size)
        end = start + int(size)
        
        return queryset[start:end]
    
# Publisher Detail View
class PublisherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    
# Publisher Create View
class PublisherCreateView(generics.CreateAPIView):
    serializer_class = PublisherSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)