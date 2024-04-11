from django.shortcuts import render,redirect
from deliveryapp.models import deliverdetails
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from adminapp.models import *
from django.contrib.auth.models import User
from itertools import groupby
from django.db.models import Sum

# Create your views here.
def fixed(request,users1):
    user_data=UserProfile.objects.filter(username=users1).first()
    ord=orders.objects.filter(user_name=user_data)
    for ors in ord:
        ors.delivery_boy_pickedpackage=True
        ors.save()
    return redirect('deliveryapp:deliverymain')

def verified(request):
    return render(request,'verified.html')

def home2(request):
    if request.method =="POST":
        d_username=request.POST['username']
        password=request.POST['password']
        users=deliveryboys.objects.filter(d_username=d_username,password=password).first()
        users=authenticate(request=request,username=d_username,password=password)
        if users is not None:
            login(request,users)
            user_logged_in=request.user.username
            #user_data=UserProfile.objects.filter(username=user_logged_in)
            userss=deliveryboys.objects.filter(d_username=user_logged_in).first()
            if userss is not None:
                dele=deliverymappings.objects.filter(d_username=userss).first()
                if dele is None:
                    return redirect("deliveryapp:deliverymain")
                else:
                    delei = orders.objects.filter(user_name=dele.users).first()
                    if delei.delivery_boy_pickedpackage and delei.order_delivered is False:
                        return redirect("deliveryapp:deliverymain")
                    elif delei.order_delivered:
                        return redirect("deliveryapp:delivermain")
                    else:
                        return redirect("deliveryapp:delivermain")
            else:
                return redirect("deliveryapp:home2")
        else:
            messages.error(request,"you entered wrong credentials")
            return render(request,"home2.html")
    return render(request,"home2.html")

def delivermain(request):
    context = {}
    if request.user.is_authenticated:
      user_logged_in=request.user.username
      #user_data=UserProfile.objects.filter(username=user_logged_in)
      userss=deliveryboys.objects.filter(d_username=user_logged_in).first()
      if userss is not None:
        dele=deliverymappings.objects.filter(d_username=userss).first()
        user_data=UserProfile.objects.filter(username=dele.users)
        #deleie=orders.objects.filter(user_name=user_data).first()
        #print(deleie)
        order = orders.objects.all()
        grouped_orders = {}
        for username, user_orders in groupby(order, key=lambda x: x.user_name):
            grouped_orders[username] = list(user_orders)
        delei = orders.objects.filter(user_name=dele.users).values('dish_name__dish_name','order_delivered').annotate(total_quantity=Sum('quantity'))
        context={'dele':dele, 'orders':grouped_orders,'delei':delei}
      else:
        return render(request, 'delivermain.html')
    return render(request,'delivermain.html',context)

def deliverymain(request):
    context = {}
    if request.user.is_authenticated:
      user_logged_in=request.user.username
      #user_data=UserProfile.objects.filter(username=user_logged_in)
      userss=deliveryboys.objects.filter(d_username=user_logged_in).first()
      if userss is not None:
        dele=deliverymappings.objects.filter(d_username=userss).first()
        if dele is None:
            return render(request,'deliverymain.html',context)
        #user_data=UserProfile.objects.filter(username=dele.users)
        #deleie=orders.objects.filter(user_name=user_data).first()
        #print(deleie)
        else:
          order = orders.objects.all()
          grouped_orders = {}
          for username, user_orders in groupby(order, key=lambda x: x.user_name):
              grouped_orders[username] = list(user_orders)
          delei = orders.objects.filter(user_name=dele.users).values('dish_name__dish_name','id','order_delivered').annotate(total_quantity=Sum('quantity'))
          context={'dele':dele, 'orders':grouped_orders,'delei':delei}
      else:
        return render(request, 'deliverymain.html')
    return render(request,'deliverymain.html',context)
    

def dprofile(request):
    userss=request.user.username
    dus=deliveryboys.objects.filter(d_username=userss).first()
    return render(request,"dprofile.html",{'dus':dus})

def currentorders(request):
    return render(request,"currentorders.html")