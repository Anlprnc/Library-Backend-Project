from rest_framework import generics, status
from user.models import Loan
from .serializers import LoanSerializer
from books.models import Book
from rest_framework.response import Response

# ----- LOANS -----
# Loan List View
class LoanListView(generics.ListAPIView):
    serializer_class = LoanSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Loan.objects.filter(user=user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
# Loan Create View
class LoanCreateView(generics.CreateAPIView):
    serializer_class = LoanSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
# Loan Detail View
class LoanDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LoanSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Loan.objects.filter(user=user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        serializer.save()
        
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
# User Loan List View
class UserLoanListView(generics.ListAPIView):
    serializer_class = LoanSerializer
    
    def get_queryset(self):
        user_id = self.kwargs['userId']
        return Loan.objects.filter(user__id=user_id)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
# Book Loan List View
class BookListLoanView(generics.ListAPIView):
    serializer_class = LoanSerializer
    
    def get_queryset(self):
        book_id = self.kwargs['bookId']
        return Loan.objects.filter(book__id=book_id)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
# Auth Loan List View
class AuthLoanDetailView(generics.RetrieveAPIView):
    serializer_class = LoanSerializer
    
    def get_queryset(self):
        return Loan.objects.select_related('user', 'book').all()