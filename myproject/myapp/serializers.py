from rest_framework import serializers
from .models import *
from django.core.exceptions import  ValidationError 
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    
    password =  serializers.CharField(write_only=True, required = True)
    class Meta:
        model = User
        fields =['first_name','last_name','phone','email','address','username','password']
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')

        # Check if email format is valid
        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format")

        # Check password complexity (e.g., length)
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'\d', password):
            raise serializers.ValidationError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise serializers.ValidationError("Password must contain at least one special character")
        
        #validating phone number
        if not re.match(r'^\d{10}$', phone):
            raise serializers.ValidationError("Invalid phone number format. Must be exactly 10 digits.")

        return data

    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_type(self, value):
        if not value.strip():
            raise serializers.ValidationError('Type field cannot be empty')
        return value



class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields ='__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

        
        
