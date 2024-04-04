from django.db import models

# Create your models here.
class Category_table(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(max_length=255,blank=True)
    cat_image=models.ImageField(upload_to='catgory_img',blank=True)

# iss function ki vajhe se mujhe category name product table mai dikhega , 
# jab ham category table ko product table se link karenge tab ye function default call ho jayega
# jab ham product table mai data add karenge tab mujhe ye self vaala function vaha dikhega  
    def __str__(self):  
        return self.category_name