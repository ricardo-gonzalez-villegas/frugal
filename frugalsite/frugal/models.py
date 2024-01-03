from django.db import models
import uuid


class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField()
    average_price = models.FloatField(default=0.00)

    def set_average_price(self, prices: list):
        total = 0
        for price in prices:
            total = total + price
        self.average_price = format((total / len(prices)), ".2f")

    def __str__(self) -> str:
        return f"The products were saved under name {self.name} with id: {self.id}"


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.IntegerField(default=0)
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    store_id = models.CharField()
    imgage_url = models.CharField()
    price = models.FloatField(default=0.00)
    sale_price = models.FloatField(default=0.00)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()

    def set_product_sale_price(self, sale_price: float):
        self.product_sale_price = sale_price

    def __str__(self) -> str:
        return f"Product: {self.product_name}, from {self.store_name},  costs: {self.product_price}."
