
from djongo import models
from django.contrib.auth.models import AbstractUser, Group,Permission

class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10) 
    address = models.TextField() 
    password = models.CharField(max_length=128)

    groups = models.ManyToManyField(Group, related_name='customer_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='customer_user_permissions')



class Category(models.Model):
    type = models.CharField(max_length = 100)
    image = models.URLField(max_length=300)

class Product(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField()
    condition = models.CharField(max_length = 100) 
    noofdays = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    option = models.JSONField()
    rental_option= models.JSONField()

class Invoice(models.Model):
    status_choices= [("ORDERED", 'ordered'), ("DELIVERED",'delivered'),("CANCELLED",'cancelled')]
    customer = models.ForeignKey(User, on_delete = models.CASCADE)
    status = models.CharField(choices = status_choices, max_length=20)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    

