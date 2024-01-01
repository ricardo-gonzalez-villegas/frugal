from pyexpat import model
from django.db import models
import uuid

class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.IntegerField(default=0)
    favorite_name = models.CharField(max_length=50)
    date_created = models.DateTimeField()
    
    def get_id(self):
        return self.id
    
    def get_favorite_name(self):
        return self.favorite_name
    
    def __str__(self) -> str:
        return f"The products were saved under name {self.favorite_name} with id: {self.id}"



class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.IntegerField(default=0)
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=20)
    product_name = models.CharField(max_length=100)
    product_store_id = models.BigIntegerField(default=0)
    product_img_url = models.CharField()
    product_price = models.FloatField(default=0.00)
    product_sale_price = models.FloatField(default=0.00)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    
    def set_product_sale_price(self, sale_price: float):
        self.product_sale_price = sale_price
    
   
    
    def get_price(self):
        return self.product_price
    
    def get_sale_price(self):
        return self.product_sale_price
    
    def __str__(self) -> str:
        return f'Product: {self.product_name}, from {self.store_name},  costs: {self.product_price}.'
    
