from django.db import models
from books.models import Book
from django.core.validators import RegexValidator
from django_use_email_as_username.models import BaseUser, BaseUserManager
from django.contrib.auth.models import Group, Permission


# Create your models here.

class User(BaseUser):
    phone_regex = RegexValidator(
        regex=r'^\(\d{3}\) \d{3}-\d{4}$',
        message="Phone number must be in the format: (999) 999-9999"
    )
    
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    score = models.IntegerField(default=0)
    address = models.CharField(max_length=100)
    phone = models.CharField(validators=[phone_regex], max_length=17)
    birthDate = models.DateField()
    email = models.EmailField(max_length=80, unique=True)
    password = models.CharField(max_length=30)
    createDate = models.DateTimeField(auto_now_add=True)
    resetPasswordCode = models.CharField(max_length=6, blank=True, null=True)
    builtIn = models.BooleanField(default=False)
    
    objects = BaseUserManager()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    def __str__(self):
        return f"{self.firstName} {self.lastName}"
    
    
class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    loanDate = models.DateTimeField()
    expireDate = models.DateTimeField()
    returnDate = models.DateTimeField(blank=True, null=True)
    notes = models.CharField(max_length=300, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'
        
    def __str__(self):
        return f"{self.user} - {self.book}"
    
    
class Role(models.Model):
    ADMIN = 'admin'
    STAFF = 'staff'
    MEMBER = 'member'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (STAFF, 'Staff'),
        (MEMBER, 'Member')
    ]
    
    name = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=MEMBER,
        unique=True
    )
    
    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return self.name