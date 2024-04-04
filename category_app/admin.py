from django.contrib import admin
from .models import Category_table
# Register your models here.

@admin.register(Category_table)
class Category_tableAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)} # iss auto fill ho jayega slug name 
    list_display=('category_name','slug') #ye table ka column name hai jo mujhe admin mai dikhega 
