"""sproject URL Configuration

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
from django.urls import path,include
from sapp import views
from django.conf import settings
from django.conf.urls.static import static
#from .views import verify_email
app_name='sapp'

urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('menu',views.menu,name='menu'),
    path('menu2',views.menu2, name='menu2'),
    path('signin',views.signin,name='signin'),
    path('profile',views.profile,name='profile'),
    #path('cart',views.cart,name='cart'),
    path('cart', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    #path('update_quantity/<int:cart_item_id>/<int:new_quantity>/', views.update_quantity, name='update_quantity'),
    path('place_order',views.place_order,name='place_order'),
    path('orderstatus',views.orderstatus,name='orderstatus'),
    path('minus/<str:productid>/', views.minus, name='minus'),
    path('add/<str:producti>/', views.add, name='add'),
    path('address', views.address, name='address'),
    path('address2',views.address2,name='address2'),
    path('address3',views.address3,name='address3'),
    path('forget',views.forget,name='forget'),
    path('foruser',views.foruser,name='foruser'),
    path('signup2/<int:code>/<str:email>/<int:phone>/<str:username>/<str:password>/',views.signup2,name="signup2"),
    # path('base',views.base,name='base'),
    #path('verify/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
    #path('fixed/<str:users1>/', views.fixed,name='fixed'),
    path('verifcode',views.verifcode,name='verifcode'),
    path('review',views.review,name='review'),
    path('logout',views.logout,name='logout'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
