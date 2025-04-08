from django.db import models
from django.contrib.auth.models import User


# Create your models here.



# PRODUCT TABLE
class Product(models.Model):
    name = models.CharField(max_length=50, default='', verbose_name="Product Name")
    price = models.FloatField()
    pdetails = models.CharField(max_length=150, verbose_name="Product Details")
    is_active = models.BooleanField(default=True, verbose_name="Available")
    pimage = models.ImageField(upload_to='image')

    def __str__(self):
        return self.name



# CART TABLE
class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE, db_column="user_id")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE, db_column="product_id")
    qty=models.IntegerField(default=1)



# ORDER TABLE
class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="user_id")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="product_id")
    qty=models.IntegerField(default=1)



# PATTERN TABLE
class Pattern(models.Model):
    name = models.CharField(max_length=100, default='', verbose_name="Pattern Name")
    description = models.TextField()
    difficulty = models.CharField(
        max_length=50, 
        choices=[
            ('Beginner', 'Beginner'), 
            ('Intermediate', 'Intermediate'), 
            ('Advanced', 'Advanced')
        ]
    )
    patterndetails = models.CharField(max_length=50, verbose_name="Pattern Details")
    pimage = models.ImageField(upload_to='image')

    def __str__(self):
        return self.name




# PAYMENT TABLE
class Payment(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    address = models.CharField(max_length=1000, default='', verbose_name="Shipping Address")
    payment = models.CharField(
        max_length=50,
        choices=[
            ('Credit Card', 'Credit Card'),
            ('Razor Pay', 'Razor Pay'),
            ('PayPal', 'PayPal'),
            ('UPI', 'UPI'),
            ('GPay', 'GPay')
        ]
    )
    total = models.FloatField()



