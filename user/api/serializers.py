from rest_framework import serializers
from user.models import Loan, User
from books.api.serializers import BooksSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName', 'score', 'address', 'phone', 'birthDate', 'email', 'createDate', 'password', 'resetPasswordCode', 'builtIn']


class LoanSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    book = BooksSerializer()
    
    class Meta:
        model = Loan
        fields = ['id', 'user', 'book', 'loanDate', 'expireDate', 'returnDate']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['request'].user
        if not user.is_staff:
            data.pop('notes', None)
        return data