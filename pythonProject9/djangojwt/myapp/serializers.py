from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Seller, Book

class UserSerializer(serializers.ModelSerializer):
     class Meta:
         model = User
         fields = ('id','username','email')


class RegisterSerializer(serializers.ModelSerializer):
     class Meta:
         model = User
         fields = ('username','email','password')

     def create(self, validted_data):
         user = User.objects.create_user(
             validted_data['username'],
             validted_data['email'],
             validted_data['password'],
         )
         return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only = True)

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'name', 'email', 'address', 'phone', 'available_to_deliver']

class BookSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)  # Ensure seller is not expected from the frontend

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'publication_date', 'publisher_name', 'edition',
            'category', 'language', 'condition', 'price', 'seller'
        ]
