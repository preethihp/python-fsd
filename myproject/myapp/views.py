from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import AnonymousUser


class CustomerRegistrationAPIView(APIView):
    def get(self,request,*args,**kwargs):
        result = User.objects.all()
        serializer = CustomerRegistrationSerializer(result, many = True)
        return Response({'status':'success','customer':serializer.data},status=200)
        
    def post(self, request, *args, **kwargs):
        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response({'message': 'Registration Successful'},status=status.HTTP_201_CREATED )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomerLoginAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = CustomerRegistrationSerializer(data = request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        #print(username,password)
        user =User.objects.get ( username=username, password= password)
        #print( user)
        if user:
            #login(request,user)
           
            serializer = CustomerRegistrationSerializer(user)
            return Response( {'message':'Login Successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
class CategoryCreateAPIView(APIView):
    permission_classes=[IsAdminUser]
    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Category created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductCreateAPIView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductListByCategoryAPIView(APIView):
    def get(self, request, category_name, *args, **kwargs):
        try:
            category = Category.objects.get(type=category_name)
            products = Product.objects.filter(category=category)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

class CategoryListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class InvoiceSerializerAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        username = request.headers.get('username') 
        password  = request.headers.get('password')
       
        try:
            customer = User.objects.get(username=username, password=password)
            serializer = InvoiceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(customer=customer)  
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class InvoiceStatusAPIView(APIView):
    def get(self, request, *args, **kwargs):
        order_status = request.query_params.get('status')
        username = request.headers.get('username') 
        password  = request.headers.get('password')
        try:
            customer = User.objects.get(username=username, password=password)
            if order_status in ['ORDERED', 'CANCELLED', 'DELIVERED']:
                invoices = Invoice.objects.filter(customer= customer, status=order_status)
                serializer = InvoiceSerializer(invoices, many = True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class PendingOrderAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        pending_orders = Invoice.objects.filter(status='ORDERED')
        serializer = InvoiceSerializer(pending_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        