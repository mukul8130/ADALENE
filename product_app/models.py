from django.db import models
from category_app.models import Category_table
# Create your models here.
class Product_table(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(max_length=500,blank=True)
    price=models.IntegerField()
    images=models.ImageField(upload_to='products_img')
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category_table,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    
    # jab ham product table ko kisi dusri table se link karenge to hame dusri table mai product name dikhai denge
    # like mene product table ko variation table se link kara hai to ab mujhe variation table mai product name dikhega
    # iss __str__ self function ki madat se
    def __str__(self):
        return self.product_name
    

class Variation_table(models.Model):
    PT=models.ForeignKey(Product_table, on_delete=models.CASCADE)
    VC=models.CharField(max_length=100,choices=[('color','color'),('size','size')])
    VV=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.VV