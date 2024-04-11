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
from adminapp import views
app_name='adminapp'

urlpatterns = [
    path('',views.home1,name='home1'),
    path('adminmain',views.adminmain,name='adminmain'),
    path('adminmain/adddishes',views.adddishes,name='adddishes'),
    path('adminmain/changedish',views.changedish,name='changedish'),
    path('adminmain/adddeliver',views.adddeliver,name='adddeliver'),
    path('adminmain/changedish/<str:pro>/', views.changesdish, name='changesdish'),
    #path('adminmain/<str:username>/<str:delivery_boy_username>/', views.assign_deliveryboy, name='assign_deliveryboy'),
    path('adminmain/<str:username>/<str:delivery_boy_username>', views.assign_deliveryboy, name='assign_deliveryboy'),
    path('adminmain/changedelivery',views.changedelivery,name='changedelivery'),
    path('adminmain/changesdelivery/<str:emai>/',views.changesdelivery,name='changesdelivery'),
]
