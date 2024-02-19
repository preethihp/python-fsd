from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import  ValidationError as DjangoValidationError
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    
    password =  serializers.CharField(write_only=True, required = True)
    class Meta:
        model = User
        fields =['first_name','last_name','phone','email','address','username','password']

    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','type']

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

        
        
