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
from deliveryapp import views
app_name='deliveryapp'

urlpatterns = [
    path('',views.home2,name='home2'),
    path('delivermain/',views.delivermain,name='delivermain'),
    path('deliverymain/',views.deliverymain,name='deliverymain'),
    path('dprofile/',views.dprofile,name='dprofile'),
    path('currentorders/', views.currentorders,name='currentorders'),
    path('fixed/<str:users1>/', views.fixed,name='fixed'),
    path('verified/',views.verified,name='verified'),
]
