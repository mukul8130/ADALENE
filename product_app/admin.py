from django.contrib import admin
from .models import Product_table,Variation_table
# Register your models here.

@admin.register(Product_table)
class xyzAdmin(admin.ModelAdmin):
    list_display=('id','product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields={'slug':('product_name',)}

@admin.register(Variation_table)
class zyx(admin.ModelAdmin):
    list_display=('id','VC','VV')