from django.shortcuts import render,redirect,HttpResponse
from product_app.models import Product_table,Variation_table
from category_app.models import Category_table
from cart_app.models import Cart_item_table
from django.core.paginator import Paginator 
# login
from django.contrib import auth
from django.contrib import messages
# /login

# Registration
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
#/ Registration

def home_page(req):
    product=Product_table.objects.all()
    con={
        'pro':product
    }
    return render(req,'index.html',con)

def store(req):
    try:
        name=req.GET['sunny']
        product=Product_table.objects.filter(product_name__icontains=name)
        paginator=Paginator(product,12)
        # cat=Category_table.objects.all() ye mene aise hi samjhne ke liye data pass kara hai 

    except:
        product=Product_table.objects.all()
        paginator=Paginator(product,12)
        # cat=Category_table.objects.all()

    try:
        page=req.GET['page']
    except:
        page=1

    product=paginator.get_page(page)

    con={
        'pro':product,
        # 'cat':cat
    }
    return render(req,'store.html',con)


def category(req,x):
    product=Product_table.objects.filter(category__category_name=x)
    con={
        "pro":product,
        'x':x
    }
    return render(req,'store.html',con)

def filter_price_product(req):
    if req.method=='POST':
        min_price=req.POST['minprice']
        max_price=req.POST['maxprice']
        
        if(min_price and max_price):
            p = Product_table.objects.filter(price__range=(min_price,max_price))

            context = {
                'pro': p
            }
            return render(req, 'store.html',context)
        
        else:
            p=Product_table.objects.all()
            context={
                'pro':p
            }
            messages.error(req,'please enter the price')
            return render(req, 'store.html',context)


    

def product_page(req,product_id):
    product=Product_table.objects.get(id=product_id)
    color_variant=Variation_table.objects.filter(PT=product,VC='color')
    size_variant=Variation_table.objects.filter(PT=product,VC='size')
    con={
        'product':product,
        'colors':color_variant,
        'sizes':size_variant

    }
    return render(req,'product.html',con)

def login(req):
    if req.method=='POST':
        u=req.POST['username']
        p=req.POST['password']
        user=auth.authenticate(username=u,password=p)

        if user is not None:
            auth.login(req,user)
            messages.success(req,'Login Successfull')
            return redirect('/')
        else:
            messages.error(req,'User does not exist')
            return render(req,'login.html')


    return render(req,'login.html')




def logout(req):
    auth.logout(req)
    messages.error(req,'Logout Successfull')
    return redirect('/')

def registration(req):
    if req.method=='POST':
        fn=req.POST['firstname']
        ln=req.POST['lastname']
        em=req.POST['email']
        u=req.POST['username']
        cp=req.POST['cp']
        rp=req.POST['rp']

        

        def BCA(cp,rp,em,u,fn,ln):
            if cp != rp:
                messages.error(req,'Passowrd Does Not Match')
        
            elif User.objects.filter(email=em).exists():
                messages.error(req,'Email is already exists')

            elif User.objects.filter(username=u).exists():
                messages.error(req,'Username is already exists')

            else:
                # admin mai jo table bani hui hai usme value bhej di
                user=User.objects.create_user(first_name=fn,last_name=ln,email=em,username=u,password=cp,is_active=False)
                user.save()

                domain_name=get_current_site(req)
                mail_subject='Plase click and activate your account'
                user_id=urlsafe_base64_encode(force_bytes(user.pk))
                token=default_token_generator.make_token(user)
                msg=f'http://{domain_name}/activate_account/{user_id}/{token}'
                to_email=em
                send_email=EmailMessage(mail_subject,msg,to=[to_email])
                send_email.send()
                messages.success(req,"Check Your Mail")
        
        BCA(cp,rp,em,u,fn,ln)
        
    return render(req,'registration.html')

def Activate(req,user_id,token):
    try:
        k=urlsafe_base64_decode(user_id) #ye user ki primary key ko decode kar raha hai upar hamne isse encode kara tha
        u=User.objects.get(pk=k)

        if default_token_generator.check_token(u,token):
            u.is_active=True
            u.save()
            messages.success(req,"Verification Successfull")

            return redirect("/login")
    except:
        messages.error(req,"Invalid Credentials")
    return redirect('/registration')

from django.core.exceptions import ObjectDoesNotExist
def forgot(req):
    if req.method=='POST':
        e=req.POST['for_pas']
        try:
            user=User.objects.get(email=e)
            domain_name=get_current_site(req)
            mail_subject="Reset Password"
            userid_encode=urlsafe_base64_encode(force_bytes(user.pk))
            token=default_token_generator.make_token(user)
            message=f'http://{domain_name}/reset-password/{userid_encode}/{token}'
            to_email=e

            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(req,'Reset link sent to your email')
        
        except ObjectDoesNotExist:
            messages.error(req,'No email exists')

    return render(req,'forgot.html')

def forgot_email_activate(req,uid,token):
    try:
        x=urlsafe_base64_decode(uid)
        user=User.objects.get(pk=x)

        if default_token_generator.check_token(user,token):
            req.session['uid']=uid
            messages.success(req,'Please create New Password')
            return render(req,'reset_pass.html')
    except:
        return redirect('/registration.html')


def resetpassword(req):
    if req.method=='POST':
        password=req.POST['P']
        confirm_password=req.POST['CP']

        if(password == confirm_password):
            uid=req.session['uid']
            u=User.objects.get(id=urlsafe_base64_decode(uid))
            u.set_password(password)
            u.save()
            messages.success(req,'Password Reset Successfully')
            return redirect('/login')
        
        else:
            messages.error(req,'Password Are Does Not Match')
            return redirect('/resetpass')
    else:
        return render(req,'reset_pass.html')


# def Cart(req):
#     us=req.user # default hai user
#     cart_items=Cart_item_table.objects.filter(u=us)
#     total=0

#     for i in cart_items:
#         total+=i.pc.price * i.q

#         c={
#             'cart_item':cart_items,
#             'total':total,
#             'tax':round(total*0.18,2),
#             'grand_total':round(total+total*0.18,2)
#         }

        
#     return render(req,'header/header.html',c)
    
def Addcart(req,product_id):
    user=req.user
    if user.is_authenticated:    
        p=Product_table.objects.get(id=product_id)

        if req.method=="POST":
            color=req.POST['color']
            size=req.POST['size']

        
            size_variant=Variation_table.objects.get(VV=size,PT=p)
            color_variant=Variation_table.objects.get(VV=color,PT=p)

            current_variant=[color_variant,size_variant]
            print(current_variant)

            is_product_exists=Cart_item_table.objects.filter(pc=p,u=user).exists()
       
            if is_product_exists:

                each_product_variant=[]
                products=Cart_item_table.objects.filter(pc=p,u=user)
            
                for product1 in products:
                    each_product_variant.append(list(product1.v.all()))
                    #print(l1)
                if current_variant in each_product_variant:
                    product_index=each_product_variant.index(current_variant)
                    product1=products[product_index]
                    product1.q+= 1
                    product1.save()
            
                else:
                    product1=Product_table.objects.get(id=product_id)
                    c=Cart_item_table.objects.create(pc=product1,u=user,q=1)
                    c.v.add(color_variant)
                    c.v.add(size_variant)
                    messages.success(req,"Please Check Your Cart")


            else:
                z=Cart_item_table.objects.create(pc=p,u=user,q=1)
                z.v.add(color_variant)
                z.v.add(size_variant)
                messages.success(req,"Please Check Your Cart")
    else:
        messages.error(req,'Please Login ')    

    return redirect('/')


def remove_btn(req,b):
    user=req.user
    ci=Cart_item_table.objects.get(id=b,u=user)
    ci.delete()
    return redirect("/")


def minus_btn(req,g):
    user=req.user
    z=Cart_item_table.objects.get(id=g,u=user)

    if(z.q>1):
        # z.q= z.q-1
        z.q-=1
        z.save()
    else:
        z.delete()
    
    return redirect('/')

from django.shortcuts import get_object_or_404
def plus_btn(req,k):
    user=req.user
    n=Cart_item_table.objects.get(id=k,u=user)
    
    n1=get_object_or_404(Cart_item_table,id=k)
    stock_quantity=n1.pc.stock
    # pro_name=n1.pc.product_name
    # print(stock_quantity)
    # print(pro_name)
    
    if(n.q<stock_quantity):
        if(n.q>=1):
            n.q=n.q+1
            # n.q+=1
            n.save()
        return redirect("/")
    else:
        messages.error(req,'out of stock')
        return redirect("/")



def ourstory(req):
    return render(req,'ourstory.html')

def ourcraft(req):
    return render(req,'ourcraft.html')

def giftcard(req):
    return render(req,'giftcard.html')

