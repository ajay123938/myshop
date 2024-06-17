from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    cateogry = models.CharField(max_length=100)
    img =models.ImageField(upload_to="products")


class Order(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE,related_name="userorder")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="order")
    status = models.BooleanField(default=False)
    user_received = models.BooleanField(default=False)
    qty = models.IntegerField(default=0)

class user(models.Model):
    user1 = models.ForeignKey(User,on_delete=models.CASCADE,related_name="üser")
    