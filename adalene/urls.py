"""adalene URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_page),
    path('store/',store),
    path('store/<x>',category),
    path('product_page/<product_id>',product_page),
    path('login/',login),
    path('logout/',logout),
    path('registration/',registration),
    path('activate_account/<user_id>/<token>',Activate),
    path('forgot/',forgot),
    path('reset-password/<uid>/<token>',forgot_email_activate),
    path('resetpass/',resetpassword),
    path('cart_page/<product_id>',Addcart),
    path('remove_product/<b>',remove_btn),
    path('minus_btn/<g>',minus_btn),
    path('plus_btn/<k>',plus_btn),
    path('ourstory/',ourstory),
    path('ourcraft/',ourcraft),
    path('giftcard_item/',giftcard),
    path('filter_price/',filter_price_product)

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
