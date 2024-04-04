from .models import Cart_item_table
def cart(req):
    cart_item=[]
    total=0
    tax=0
    grand_total=0
    user=req.user
    if user.is_authenticated:
        cart_item=Cart_item_table.objects.filter(u=user) 
        for i in cart_item:
            total=total+i.pc.price * i.q   
        tax=round(total*0.18,2)
        grand_total=round(total+total*0.18,2)
    return{'cd':cart_item,'total':total,'tax':tax,'grand_total':grand_total}

def ci(req):
    u=req.user
    if u.is_authenticated:
        cu=Cart_item_table.objects.filter(u=u).count()
    else:
        cu=0
    return {'count_item':cu}
    


    
    