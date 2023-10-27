from django.urls import path
from .views import LoanListView, LoanCreateView, LoanDetailView, UserLoanListView, BookListLoanView, AuthLoanDetailView, SignInView, RegisterView, UserCreateView, UserCreateLoanView, UserListView


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
    path('user/create/', UserCreateView.as_view(), name='user-create'),
    path('user/loan/create/', UserCreateLoanView.as_view(), name='user-loan-create'),
]