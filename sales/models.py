from django.db import models
from django.db.models.fields import DateTimeField
from django.utils import timezone
from django.shortcuts import reverse
# Models
from products.models import Products
from customers.models import Customer
from profiles.models import Profile
from django.shortcuts import reverse
# Utils
from .utilis import generate_code
class Position(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    price = models.FloatField(blank=True)
    created = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        return super().save(*args, **kwargs)
    def get_sales_id(self):
        sale_obj=self.sale_set.first()
        return sale_obj.id
    
    def get_sales_customer(self):
        sale_obj=self.sale_set.first()
        return sale_obj.customer.name
    
    def __str__(self):
        return f"id: {self.id}, product: {self.product.name}, quantity: {self.quantity}"
# Create your models here.
class Sale(models.Model):
    transaction_id = models.CharField(max_length=12, blank=True)
    positions = models.ManyToManyField(Position)
    total_price = models.FloatField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.transaction_id == "":
            self.transaction_id = generate_code()       
        if self.created is None:
            self.created = timezone.now()

        return super().save(*args, **kwargs)
    
    def get_positions(self):
        return self.positions.all()
    

    def __str__(self):
        return f"Sales for the amount of PKR {self.total_price} and id: {self.id}"

    def get_absolute_url(self):
        return reverse('sales:detail',kwargs={'pk':self.pk})

class CSV(models.Model):
    file_name = models.CharField(max_length=120, null=True)
    csv_file = models.FileField(upload_to = 'csvs', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.file_name)    