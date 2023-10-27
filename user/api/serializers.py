from rest_framework import serializers
from user.models import Loan, User
from books.api.serializers import BooksSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName', 'score', 'address', 'phone', 'birthDate', 'email', 'createDate', 'password', 'resetPasswordCode', 'builtIn']
        

class SignInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password= serializers.CharField()
    
    class Meta:
        model = User
        fields = ['email', 'password']
    
    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        
        if email and password:
            user= authenticate(request=self.context.get('request'),email=email,password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password')
            attrs['user']=user
            return attrs
        else:
            raise serializers.ValidationError('Both email and password are required')
        

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName', 'address', 'phone', 'birthDate', 'email', 'password', 'resetPasswordCode', 'builtIn']
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

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