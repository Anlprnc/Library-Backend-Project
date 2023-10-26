from django.urls import path
from .views import BookListView, BookCreateView, BookDetailView


urlpatterns = [
    # BOOKS
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]
