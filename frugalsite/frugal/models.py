from django.db import models
import uuid

class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField()
    saved_date = models.DateTimeField()
    
    def get_uuid(self):
        return self.id
    
    def __str__(self) -> str:
        return self.id



class Meijer(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=20)
    product_id = models.IntegerField()
    product_img_url = models.CharField()
    product_price = models.FloatField()
    product_sale_price = models.FloatField()
    


class Kroger(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    product = models.CharField()


class Walmart(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    product = models.CharField()
