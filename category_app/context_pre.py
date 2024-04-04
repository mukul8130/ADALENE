from .models import Category_table

def abc(req):
    cat_name=Category_table.objects.all()
    return {'cn':cat_name}