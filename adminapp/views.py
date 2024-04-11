from django.shortcuts import render,redirect
from adminapp.models import adminss
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from adminapp.models import *
from adminapp.forms import DishForm
from itertools import groupby
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # Add this import
from sapp.models import *
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
#@require_POST
#def assign_deliveryboy(request,username,delivery_boy_username):
#    print("hi1")
#    username = request.POST.get('username')
#    delivery_boy_username = request.POST.get('deliveryBoyUsername')
#    user_profile = get_object_or_404(UserProfile, username=username)
#    delivery_boy = get_object_or_404(deliveryboys, d_username=delivery_boy_username)
#    location = get_object_or_404(Location, user_profile=user_profile)
#
#    # Create an instance of deliverymapping
#    delivery_mapping_instance = deliverymapping.objects.create(
#        users=user_profile,
#        d_username=delivery_boy,
#        address=location,
#        phone=user_profile  # Assuming you want to use the user's phone
#    )
#    return JsonResponse({'success': True})

#@require_POST
#def assign_deliveryboy(request, username, delivery_boy_username):
#    # Remove the lines below
#    # username = request.POST.get('username')
#    # delivery_boy_username = request.POST.get('deliveryBoyUsername')
#    i=0
#    user_profile = get_object_or_404(UserProfile, username=username)
#    delivery_boy = get_object_or_404(deliveryboys, d_username=delivery_boy_username)
#    location = get_object_or_404(Location, usersname=username)
#    concatenated_address = f"{location.streetname}, {location.villagecity}, {location.pincode}, {location.state}, {location.country}"
#    # Create an instance of deliverymapping
#    delivery_mapping_instance = deliverymapping.objects.create(
#        users=user_profile,
#        d_username=delivery_boy,
#        address=concatenated_address,
#        phone=user_profile.phone
#    )
#    delivery_boy.availability=False
#    delivery_boy.save()
#    ord=orders.objects.filter(user_name=username)
#    for ors in ord:
#        ors.delivery_boy_assigned=True
#        ors.save()
#        i=i+1
#    if i!=0:
#        return redirect("adminapp:adminmain")
#    return redirect("adminapp:adminmain")


@require_POST
def assign_deliveryboy(request, username, delivery_boy_username):
    i=0
    user_profile = get_object_or_404(UserProfile, username=username)
    #ors=get_object_or_404(orders,user_name=user_profile)
    orse=orders.objects.filter(user_name=username)
    delivery_boy = get_object_or_404(deliveryboys, d_username=delivery_boy_username)
    location = get_object_or_404(Location, usersname=username)
    concatenated_address = f"{location.streetname}, {location.villagecity}, {location.pincode}, {location.state}, {location.country}"
    # Create an instance of deliverymapping
    for orss in orse:
        delivery_mapping_instance = deliverymappings.objects.create(
            ord=orss,
            users=user_profile,
            d_username=delivery_boy,
            address=concatenated_address,
            phone=user_profile.phone
        )
    delivery_boy.availability=False
    delivery_boy.save()
    ord=orders.objects.filter(user_name=username)
    for ors in ord:
        ors.delivery_boy_assigned=True
        ors.save()
        i=i+1
    if i!=0:
        return redirect("adminapp:adminmain")
    return redirect("adminapp:adminmain")

# Create your views here.
def home1(request):
    if request.method =="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=adminss.objects.filter(username=username,password=password).first()
        if user is not None:
            user=authenticate(request=request,username=username,password=password)
            login(request,user)
            return redirect("adminapp:adminmain")
        else:
            messages.error(request,"you entered wrong credentials")
            return render(request,"home1.html")
    return render(request,"home1.html")


#def adminmain(request):
#    # Assuming orders is a queryset or list of order objects
#    order = orders.objects.all()
#    grouped_orders = {}
#    group={}
#    for username, user_orders in groupby(order, key=lambda x: x.user_name):
#        grouped_orders[username] = list(user_orders)
#    deliver=deliveryboys.objects.all()
#    deliverymappings=deliverymapping.objects.all()
#    context = {'orders': grouped_orders,'deliver':deliver,'deliverymappings':deliverymappings}
#    return render(request, 'adminmain.html', context)

#def adminmain(request):
#    order = orders.objects.all()
#    grouped_orders = {}
#    for username, user_orders in groupby(order, key=lambda x: x.user_name):
#        grouped_orders[username] = list(user_orders)
#
#    deliver = deliveryboys.objects.all()
#    deliverymappings = deliverymapping.objects.all()
#
#    # Create a dictionary with users as keys and delivery usernames as values
#    user_delivery_mapping = {}
#    for mapping in deliverymappings:
#        user_delivery_mapping[mapping.users] = mapping.d_username
#
#    # Create a dictionary with users as keys and filtered deliverymappings as values
#    filtered_deliverymappings = {}
#    for username, user_orders in grouped_orders.items():
#        user = UserProfile.objects.get(username=username)
#        filtered_deliverymappings[username] = deliverymappings.filter(users=user)
#
#    context = {'orders': grouped_orders, 'deliver': deliver, 'deliverymappings': user_delivery_mapping, 'filtered_deliverymappings': filtered_deliverymappings}
#    return render(request, 'adminmain.html', context)


#def adminmain(request):
#    # Assuming orders is a queryset or list of order objects
#    order = orders.objects.all()
#    grouped_orders = {}
#    for username, user_orders in groupby(order, key=lambda x: x.user_name):
#        grouped_orders[username] = list(user_orders)
#    deliver = deliveryboys.objects.all()
#    deliverymappingss = deliverymappings.objects.all()
#    group={}
#    for username, user_orders in groupby(deliverymappingss, key=lambda x: x.ord):
#        group[username] = list(user_orders)
#    context = {'orders': grouped_orders, 'deliver': deliver, 'deliverymappings': deliverymappingss,'group':group}
#    return render(request, 'adminmain.html', context)

def adminmain(request):
    # Assuming orders is a queryset or list of order objects
    orders_not_delivered = orders.objects.filter(order_delivered=False)
    grouped_orders = {}
    deliverymappingss = {}  # Dictionary to store delivery mappings for each order
    for username, user_orders in groupby(orders_not_delivered, key=lambda x: x.user_name):
        grouped_orders[username] = list(user_orders)
    deliver = deliveryboys.objects.all()
    for order_instance in orders_not_delivered:
        deliverymappingss[order_instance] = deliverymappings.objects.filter(ord=order_instance)
    context = {'orders': grouped_orders, 'deliver': deliver, 'deliverymappings': deliverymappingss}
    return render(request, 'adminmain.html', context)


def changedelivery(request):
    dele=deliveryboys.objects.all()
    context={'dele':dele}
    return render(request,'changedelivery.html',context)

#def adddeliver(request):
#    if request.method=="POST":
#        d_username=request.POST['d_username']
#        d_name=request.POST['d_name']
#        d_phone=request.POST['d_phone']
#        availability=request.POST['availability']
#        password=request.POST['password']
#        address=request.POST['address']
#        ins=deliveryboys(d_username=d_username,d_name=d_name,d_phone=d_phone,availability=availability,password=password,address=address)
#        ins.save()
#    return render(request,"addminmain.html")

#def adddishes(request):
#    form=DishForm()
#    if request.method == 'POST':
#        form = DishForm(request.POST, request.FILES)
#        if form.is_valid():
#            form.save()
#            # Handle successful form submission
#    else:
#        form = DishForm()
#    return render(request, 'adddishes.html', {'form': form})
@csrf_exempt
def adddishes(request):
    if request.method=="POST" or request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        dishname=request.POST.get('dish_name')
        dishcode=request.POST.get('dish_code')
        price=request.POST.get('price')
        type=request.POST.get('types')
        availability=request.POST.get('availability') =='on'
        image=request.POST.get('image')
        discount=request.POST.get('discount')
        description=request.POST.get('description')
        ins=dishes(dish_name=dishname,dish_code=dishcode,price=price,types=type,availability=availability,image=image,discount=discount,description=description)
        ins.save()
    return redirect("adminapp:adminmain")
         
#def changesdish(request,pro):
#    dis=dishes.objects.filter(dish_code=pro).first()
#    if request.method=="POST":
#        dishname=request.POST['dishname']
#        dishcode=request.POST['dishcode']
#        price=request.POST['price']
#        type=request.POST['types']
#        avail=request.POST['availability']
#        discount=request.POST['discount']
#        description=request.POST['description']
#        ins=dishes(dish_code=pro,dish_name=dishname,price=price,types=type,availability=avail,image=dis.image,discount=discount,description=description)
#        dis.delete()
#        ins.save()
#    return redirect("adminapp:changedish")

def changesdish(request, pro):
    dis = dishes.objects.filter(dish_code=pro).first()
    
    if request.method == "POST":
        dishname = request.POST.get('dishname')
        dishcode = request.POST.get('dishcode')
        price = request.POST.get('price')
        dish_type = request.POST.get('types')
        avail = request.POST.get('availability')  # Assuming availability is a boolean field
        discount = request.POST.get('discount')
        description = request.POST.get('description')
        
        # Update the existing dish with the new data
        dis.dish_name = dishname
        dis.dish_code = dishcode
        dis.price = price
        dis.types = dish_type
        dis.availability = True if avail == 'on' else False  # Convert 'on'/'off' to boolean
        dis.discount = discount
        dis.description = description
        
        dis.save()
        return redirect("adminapp:changedish")  
    
    return redirect("adminapp:changedish")  

def changesdelivery(request,emai):
    dele=deliveryboys.objects.filter(email=emai).first()
    if request.method=='POST':
        email=request.POST.get('email')
        dname=request.POST.get('dname')
        dusername=request.POST.get('username')
        phone=request.POST.get('dphone')
        avail = request.POST.get('availability')
        dele.email=email
        dele.d_name=dname
        dele.d_username=dusername
        dele.d_phone=phone
        dele.availability = True if avail == 'on' else False
        dele.save()
        return redirect('adminapp:changedelivery')
    return redirect('adminapp:changedelivery')

def changedish(request):
    dish=dishes.objects.all()
    context={'dishes_dat':dish}
    return render(request,"changedish.html",context)


@csrf_exempt  # Add this decorator to disable CSRF protection for this view
def adddeliver(request):
    if request.method == "POST" or request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        email=request.POST.get('email')
        d_username = request.POST.get('d_username')
        d_name = request.POST.get('d_name')
        d_phone = request.POST.get('d_phone')
        availability = request.POST.get('availability') =='on'
        password = request.POST.get('password')
        address = request.POST.get('address')
        myuser = User.objects.create_user(d_username, email, password)
        myuser.save()
        ins = deliveryboys(
            email=email,
            d_username=d_username,
            d_name=d_name,
            d_phone=d_phone,
            availability=availability,
            password=password,
        )
        ins.save()     
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
    
    return redirect("adminapp:adminmain")