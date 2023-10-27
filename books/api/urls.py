from django.urls import path
from .views import BookListView, BookCreateView, BookDetailView, PublisherListView, PublisherDetailView, PublisherCreateView, AuthorListView, AuthorDetailView, AuthorCreateView, CategoryListView, CategoryDetailView, CategoryCreateView


urlpatterns = [
    # AUTHORS
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/create/', AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    # CATEGORIES
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    # BOOKS
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    # PUBLISHERS
    path('publishers/', PublisherListView.as_view(), name='publisher-list'),
    path('publishers/create/', PublisherCreateView.as_view(), name='publisher-create'),
    path('publishers/<int:pk>/', PublisherDetailView.as_view(), name='publisher-detail'),
]
