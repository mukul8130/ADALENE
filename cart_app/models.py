from django.db import models
from product_app.models import Product_table,Variation_table
from django.contrib.auth.models import User
# Create your models here.

class Cart_item_table(models.Model):
    pc=models.ForeignKey(Product_table,on_delete=models.CASCADE)
    v=models.ManyToManyField(Variation_table)
    u=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    q=models.IntegerField()
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.pc.product_name
    
    def get_total(self):
        return self.pc.price * self.q