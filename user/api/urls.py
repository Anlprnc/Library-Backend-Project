from django.urls import path
from .views import LoanListView, LoanCreateView, LoanDetailView, UserLoanListView, BookListLoanView, AuthLoanDetailView, SignInView, RegisterView, UserCreateView, UserCreateLoanView, UserListView, UsersDetailView, get_statistic, most_popular_books, unreturned_books, expired_books, most_borrowers


urlpatterns = [
    # LOAN
    path('loans/', LoanListView.as_view(), name='loan-list'),
    path('loans/create/', LoanCreateView.as_view(), name='loan-create'),
    path('loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),
    path('loans/user/<int:userId>/', UserLoanListView.as_view(), name='user-loan-list'),
    path('loans/book/<int:bookId>/', BookListLoanView.as_view(), name='book-loan-list'),
    path('loans/auth/<int:pk>/', AuthLoanDetailView.as_view(), name='auth-loan-detail'),
    # AUTH
    path('signin/', SignInView.as_view(), name='signin'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UsersDetailView.as_view(), name='users-detail'),
    path('user/create/', UserCreateView.as_view(), name='user-create'),
    path('user/loan/create/', UserCreateLoanView.as_view(), name='user-loan-create'),
    # REPORTS
    path('report/', get_statistic, name='statistics_report'),
    path('report/most-popular-books/', most_popular_books, name='most_popular_books'),
    path('report/unreturned-books/', unreturned_books, name='unreturned_books'),
    path('report/expired-books/', expired_books, name='expired_books_report'),
    path('report/most-borrowers/', most_borrowers, name='most_borrowers'),
]