from rest_framework import generics, status, permissions
from user.models import Loan, User
from .serializers import LoanSerializer, UserSerializer, SignInSerializer, RegisterSerializer
from books.models import Book, Author, Publisher, Category
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import MemberPermission, EmployeePermission, IsEmployeeOrAdmin, IsAdmin, IsMemberOrEmployeeOrAdmin
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import models
from datetime import datetime

# ----- AUTHENTICATION -----
# Sign In View
class SignInView(generics.CreateAPIView):
    serializer_class = SignInSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.MultipleObjectsReturned:
            return Response({'error': 'Many users found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        access_token = str(AccessToken.for_user(user))
        return Response({'token': access_token})

# Register View
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Registration successfully done', 'success': True})
    
# User Create View
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    permission_classes = [permissions.AllowAny]
    
    def get_permissions(self):
        if self.request.user.is_authenticated:
            if self.request.user.role == 'member':
                self.permission_classes = [MemberPermission]
            elif self.request.user.role == 'employee':
                self.permission_classes = [EmployeePermission]
            elif self.request.user.role == 'admin':
                self.permission_classes = [permissions.IsAdminUser]
                
        return super().get_permissions()
    
# User List View
class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [EmployeePermission, permissions.IsAdminUser]
    
    def get_queryset(self):
        return User.objects.all()
    
# Users Detail View
class UsersDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsEmployeeOrAdmin]
        elif self.request.method == 'PUT':
            permission_classes = [IsEmployeeOrAdmin]
        elif self.request.method == 'DELETE':
            permission_classes = [IsAdmin]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
    
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
    
# User Loan Create View    
class UserCreateLoanView(generics.CreateAPIView):
    serializer_class = LoanSerializer
    permission_classes = [IsMemberOrEmployeeOrAdmin]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
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
    
# ----- REPORTS -----
# Get Statistic
def get_statistic(request):
    statistics = {
        'books': Book.objects.count(),
        'authors': Author.objects.count(),
        'publishers': Publisher.objects.count(),
        'categories': Category.objects.count(),
        'loans': Loan.objects.count(),
        'unReturnedBooks': Loan.objects.filter(returned=False).count(),
        'expiredBooks': Loan.objects.filter(expired=True).count(),
        'members': User.objects.count()
    }
    
    return JsonResponse({'dashboard': statistics})

# Most Popular Books
def most_popular_books(request):
    amount = int(request.GET.get('amount', 20))
    page = int(request.GET.get('page', 0))
    size = int(request.GET.get('size', 20))
    
    loans = Loan.objects.values('book__id', 'book__name', 'book__isbn').annotate(borrow_count=models.Count('book__loan')).order_by('-borrow_count')[:amount]
    
    paginator = Paginator(loans, size)
    page_data = paginator.get_page(page + 1)
    
    response_data = [{
        'id': item['book__id'],
        'name': item['book__name'],
        'isbn': item['book__isbn'],
    } for item in page_data]
    
    return JsonResponse(response_data, safe=False)

# Unreturned Books
def unreturned_books(request):
    page = int(request.GET.get('page', 0))
    size = int(request.GET.get('size', 20))
    sort = request.GET.get('sort', 'expireDate')
    sort_type = request.GET.get('type', 'desc')
    
    unreturned_books = Loan.objects.filter(returnDate__isnull=True).order_by(f'{sort_type}{sort}')
    
    paginator = Paginator(unreturned_books, size)
    page_data = paginator.get_page(page + 1)
    
    response_data = [{
        'id': item.book.id,
        'name': item.book.name,
        'isbn': item.book.isbn,
    } for item in page_data]
    
    return JsonResponse(response_data, safe=False)

# Expired Books
def expired_books(request):
    page = int(request.GET.get('page', 0))
    size = int(request.GET.get('size', 20))
    sort = request.GET.get('sort', 'expireDate')
    sort_type = request.GET.get('type', 'desc')
    
    now = datetime.now()
    expired_books = Loan.objects.filter(returnDate__isnull=True, expireDate__lt=now).order_by(f'{sort_type}{sort}')
    
    paginator = Paginator(expired_books, size)
    page_data = paginator.get_page(page + 1)
    
    response_data = [{
        'id': item.book.id,
        'name': item.book.name,
        'isbn': item.book.isbn,
    } for item in page_data]
    
    return JsonResponse(response_data, safe=False)

# Most Borrowers
def most_borrowers(request):
    page = int(request.GET.get('page', 0))
    size = int(request.GET.get('size', 20))
    
    borrowers = Loan.objects.values('user__id', 'user_firstName', 'user_lastName').annotate(borrow_count=models.Count('user')).order_by('-borrow_count')
    
    paginator = Paginator(borrowers, size)
    page_data = paginator.get_page(page + 1)
    
    response_data = [{
        'id': item['user__id'],
        'name': f'{item["user_firstName"]} {item["user_lastName"]}',
    } for item in page_data]
    
    return JsonResponse(response_data, safe=False)