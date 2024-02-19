from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/',CustomerRegistrationAPIView.as_view(), name = 'customer-registration'),
    path('login/', CustomerLoginAPIView.as_view(), name ='customer-login'),
    path('category/', CategoryCreateAPIView.as_view(), name = 'create-category'),
    path('product/',ProductCreateAPIView.as_view(), name = 'create-product'),
    path('products/<str:category_name>', ProductListByCategoryAPIView.as_view(),  name='product-by-category'),
    path('categories/', CategoryListAPIView.as_view(), name ='list-category'),
    path('invoice/', InvoiceSerializerAPIView.as_view(), name = 'invoice-management'),
    path('invoices/',InvoiceStatusAPIView.as_view(), name = 'invoice-by-status'),
    path('pending-orders/', PendingOrderAPIView.as_view(), name = 'pending-orders'),
]