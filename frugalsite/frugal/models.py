from django.db import models
from django.utils import timezone
import uuid


class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    average_price = models.FloatField(default=0.00)
    
    def update_date_updated(self):
        self.date_updated = timezone.now()

    def set_average_price(self, prices: list):
        total = 0.00
        for price in prices:
            total = total + float(price)
        self.average_price = format((total / len(prices)), ".2f")
        self.update_date_updated()

    def __str__(self) -> str:
        return f"The products were saved under name {self.name} with id: {self.id}"


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.IntegerField(default=0)
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=20)
    name = models.CharField(max_length=500)
    store_id = models.CharField()
    imgage_url = models.CharField()
    price = models.FloatField(default=0.00)
    sale_price = models.FloatField(default=0.00)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    
    def set_price(self, price: float):
        self.price = price
        self.update_date_updated()

    def set_sale_price(self, sale_price: float):
        self.sale_price = sale_price
        self.update_date_updated()
        
    def update_date_updated(self):
        self.date_updated = timezone.now()
        

    def __str__(self) -> str:
        return f"Product: {self.product_name}, from {self.store_name},  costs: {self.product_price}."
