from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib import messages
from adminapp.models import *
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from sapp.models import *
from django.utils import timezone
from django.core.mail import send_mail,BadHeaderError
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
import random
from django.contrib.auth import logout as auth_logout

def logout(request):
    if request.method=='POST':
        auth_logout(request)
        return redirect("sapp:home")
#User = get_user_model()
def verifcode(request):
    if request.method == "POST":
        orderid = request.POST.get('orderid')  # Use get() instead of []
        code = request.POST.get('code')  # Use get() instead of []
        ors = orders.objects.filter(id=orderid).first()
        deliv=deliverymappings.objects.filter(ord=ors).first()
        deli=deliveryboys.objects.filter(d_name=deliv.d_username).first()
        ord = orderverif.objects.filter(orderse=ors).first()
        if str(ord.verifcode) == code:
            ors.order_delivered = True
            ors.save()
            deli.availability = True
            ord.delete()
            inss=order(user_name=ors.user_name,dish_name=ors.dish_name,dish_code=ors.dish_code,quantity=ors.quantity,date_of_order=ors.date_of_order,finalpricee=ors.finalpricee,delivery_boy_assigned=ors.delivery_boy_assigned,delivery_boy_pickedpackage=ors.delivery_boy_pickedpackage,order_delivered=ors.order_delivered)
            inss.save()
            ins=deliverymappingss(ord=inss,users=deliv.users,d_username=deliv.d_username,address=deliv.address,phone=deliv.phone)
            print(ins)
            ins.save()
            ors.delete()
            deli.save()
            deliv.delete()
        return redirect("deliveryapp:deliverymain")
            
#ef fixed(request,users1):
#   i=False
#   user_data=UserProfile.objects.filter(username=users1).first()
#   ord=orders.objects.filter(user_name=user_data)
#   for ors in ord:
#       ors.delivery_boy_pickedpackage=True
#       ors.save()
#       i=True
#   context={'i':i}
#   return redirect('deliveryapp:delivermain',context)

#def verify_email(request, uidb64, token):
#    try:
#        uid = urlsafe_base64_decode(uidb64).decode()
#        user = User.objects.get(pk=uid)
#    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#        user = None
#
#    if user is not None and default_token_generator.check_token(user, token):
#        user.is_active = True
#        user.save()
#        messages.success(request, 'Your email has been verified successfully. You can now login.')
#        return redirect('login')  # Redirect to login page or any other page after successful verification
#    else:
#        messages.error(request, 'Invalid verification link.')
#        return render(request, 'verification_error.html')  # Render a page indicating verification error

#from sapp.forms import LocationForm
#from django.http import JsonResponse
#def update_quantity(request, cart_item_id, new_quantity):
#    cart_item = carts.objects.get(id=cart_item_id)
#    cart_item.quantity = new_quantity
#    cart_item.save()
#
#    # You can return additional data if needed
#    return JsonResponse({'status': 'success'})

#def place_order(request):
#    if request.method == 'POST':
#        logged_in_student = request.user.username
#        user_data = UserProfile.objects.filter(username=logged_in_student).first()
#        cart_items = carts.objects.filter(user=user_data)
#
#        # Create orders from cart items
#        for cart_item in cart_items:
#            dish = cart_item.dish_codes
#            order = orders(user=user_data, dish_codes=cart_item.dish_codes,dish_name=dish.dish_name, quantity=cart_item.quantity)
#            order.save()
#
#        # Clear the cart after placing the order
#        cart_items.delete()
#        print("yes")
#        #return redirect('order_confirmation')  # Redirect to a confirmation page or any other page you want
#
#    return redirect('view_cart')

# views.py

#def base(request):
    
 #   return render('base.html')
#def add_to_cart(request, product_id):
#    logged_in_student = request.user.username
#    user_data = UserProfile.objects.filter(username=logged_in_student).first()
#    # Get the dish object or return a 404 if not found
#    product = get_object_or_404(dishes, dish_code=product_id)
#    products = get_object_or_404(dishes, dish_code=product_id)
#    # Use update_or_create to simplify the logic
#    print(product.price)
#    p=0.01
#    q=1
#    cart_item, created = cartprice.objects.update_or_create(
#        dish_codese=product,
#        usere=user_data,
#        price=product.price,
#        discount=product.discount,
#        defaults={'quantity': 1},
#        finalprice=product.price-(product.price*q*product.discount*p)  
#    )
#    if not created:
#        # If the cart item already exists, increment the quantity
#        cart_item.quantity += 1
#        cart_item.finalprice=((cart_item.quantity*product.price)-(product.price*cart_item.quantity*product.discount*p))
#        cart_item.save()
#    #return render(request,"menu.html")
#    #return redirect('sapp:view_cart')
#    return redirect('sapp:view_cart') 
# 
#def remove_from_cart(request, item_id):
#    cart_item = carts.objects.get(id=item_id)
#    cart_item.delete()
#    return redirect('sapp:view_cart')
def menu2(request):
    q=0
    logged_in_student = request.user.username
    user_data=UserProfile.objects.filter(username=logged_in_student).first()
    cart_items = cartprice.objects.filter(usere=user_data)
    for cart in cart_items:
        q=q+cart.quantity
    dishes_data = dishes.objects.all()
    loc=Location.objects.filter(usersname=logged_in_student)
    context = {'dishes_dat': dishes_data, 'q':q,'carts':cart_items,'loc':loc}
    return render(request, "menu2.html", context)
    

def minus(request, productid):
    logged_in_student = request.user.username
    user_data = UserProfile.objects.filter(username=logged_in_student).first()
    dish=dishes.objects.filter(dish_name=productid).first()
    cart_items = cartprice.objects.filter(usere=user_data,dish_codese=dish)
    for cart_item in cart_items:
        if cart_item.dish_codese==dish:
            cart_item.quantity -= 1
            if cart_item.quantity<=0:
                cart_item.delete()
            else:
                cart_item.finalprice=(cart_item.price*cart_item.quantity)-(cart_item.price*cart_item.quantity*cart_item.discount*0.01)
                cart_item.save()
    return redirect('sapp:view_cart')

def add(request,producti):
    logged_in_student = request.user.username
    user_data = UserProfile.objects.filter(username=logged_in_student).first()
    dish=dishes.objects.filter(dish_name=producti).first()
    cart_items = cartprice.objects.filter(usere=user_data,dish_codese=dish)
    for cart_item in cart_items:
        if cart_item.dish_codese==dish:
            cart_item.quantity += 1
            cart_item.finalprice=(cart_item.price*cart_item.quantity)-(cart_item.price*cart_item.quantity*cart_item.discount*0.01)
            cart_item.save()
    return redirect('sapp:view_cart')

def place_order(request):
    logg = request.user.username
    locc = Location.objects.filter(usersname=logg)
    if locc:
        if request.method == 'POST':
            logged_in_student = request.user.username
            user_data = UserProfile.objects.filter(username=logged_in_student).first()
            cart_items = cartprice.objects.filter(usere=user_data)
            current_date = timezone.now()
            # Create orders from cart items
            total_price=0
            for cart_item in cart_items:
                dish=dishes.objects.filter(dish_name=cart_item.dish_codese)
                order = orders(user_name=user_data, dish_name=cart_item.dish_codese, dish_code=cart_item.dish_codese, finalpricee=cart_item.finalprice, quantity=cart_item.quantity,date_of_order=current_date)
                order.save()
            # Clear the cart after placing the order
            cart_items.delete()
            ord=orders.objects.filter(user_name=logged_in_student)
            for ors in ord:     
                code=0
                for i in range(6):
                    j=random.randint(1,9)
                    code=j+code*10
                ins=orderverif(useres=user_data,orderse=ors,verifcode=code)
                ins.save()
                subject = 'Verification code'
                message = f'Your Verification code is: {code} and this verification code is for the order {ors.dish_name}'
                from_email = 'ramanaidulokam@gmail.com'  # Update with your email address
                recipient_list = [user_data.email]
                send_mail(subject, message, from_email, recipient_list)
            # return redirect('order_confirmation')  # Redirect to a confirmation page or any other page you want
        return redirect('sapp:orderstatus')
    else:
        return redirect("sapp:address")
    
def address(request):
    logged_in_student=request.user.username
    userss=UserProfile.objects.filter(username=logged_in_student).first()
    if request.method=="POST":
        streetname=request.POST['streetname']
        villagecity=request.POST['villagecity']
        pincode=request.POST['pincode']
        state=request.POST['state']
        country=request.POST['country']
        ins=Location(usersname=userss,streetname=streetname,villagecity=villagecity,pincode=pincode,state=state,country=country)
        ins.save()
        return redirect("sapp:view_cart")
    return render(request,"address.html")
        
#def address2(request):
#    logged_in_student=request.user.username
#    userss=UserProfile.objects.filter(username=logged_in_student).first()
#    locc=Location.objects.get(usersname=userss)
#    context={'locc':locc}
#    if request.method=="POST":
#        locc.streetname=request.POST['streetname']
#        locc.villagecity=request.POST['villagecity']
#        locc.state=request.POST['state']
#        locc.pincode=request.POST['pincode']
#        locc.country=request.POST['country']
#        locc.save()
#        print(locc.pincode,"hi")
#        return redirect("sapp:view_cart")
#    return render(request,"address2.html",context)

def address2(request):
    logged_in_student = request.user.username
    userss = UserProfile.objects.filter(username=logged_in_student).first()
    locc, created = Location.objects.get_or_create(usersname=userss)
    context = {'locc': locc}
    if request.method == "POST":
        locc.streetname = request.POST['streetname']
        locc.villagecity = request.POST['villagecity']
        locc.state = request.POST['state']
        locc.pincode = request.POST['pincode']
        locc.country = request.POST['country']
        ins=Location(usersname=userss,streetname=locc.streetname,villagecity=locc.villagecity,pincode=locc.pincode,state=locc.state,country=locc.country)
        ins.save()
        locc.delete()
        return redirect("sapp:view_cart")

    return render(request, "address2.html", context)
#def signup(request):
#    if request.method=="POST":
#        email=request.POST['email']
#        username=request.POST['username']
#        phone=request.POST['phone']
#        password=request.POST['password']
#        if User.objects.filter(username=username):
#            messages.error(request,"username already exists")
#        elif User.objects.filter(email=email):
#            messages.error(request,"Email already registered")
#        elif len(username)>10:
#            messages.error(request,"username must be under 10 characters")
#        elif (len(phone)>10) or (len(phone)<10):
#            messages.error(request,"phone number must be 10 characters")
#        elif not username.isalnum():
#            messages.error(request,"username must be a alpha numeric")
#        else:
#            myuser = User.objects.create_user(username, email, password)
#            myuser.save()
#            ins=UserProfile(email=email,username=username,phone=phone,password=password)
#            ins.save()
#            messages.success(request, 'Your account has been created successfully. Please sign in.')
#    return render(request,"signup.html")
#def orderstatus(request):
#    q=0
#    total_price=0
#    logged_in_student = request.user.username
#    user_data=UserProfile.objects.filter(username=logged_in_student).first()
#    cart_items = cartprice.objects.filter(usere=user_data)
#    for cart in cart_items:
#      q=q+cart.quantity
#    orderss=orders.objects.filter(user_name=logged_in_student)
#    for ord in orderss:
#        total_price=total_price + ord.finalpricee
#    deliver=deliverymapping.objects.filter(users=logged_in_student)
#    context={'deliver':deliver,'orderss':orderss, 'q':q, 'total':total_price}
#    return render(request,"orderstatus.html",context)

def orderstatus(request):
    q=0
    a=False
    context={}
    p=0
    total_price=0
    logged_in_student = request.user.username
    user_data=UserProfile.objects.filter(username=logged_in_student).first()
    cart_items = cartprice.objects.filter(usere=user_data)
    for cart in cart_items:
      q=q+cart.quantity
    orderss=orders.objects.filter(user_name=logged_in_student)
    for ord in orderss:
        p=p+ord.quantity
        total_price=total_price + ord.finalpricee
    deliver=deliverymappings.objects.filter(users=logged_in_student).first()
    if deliver:
       a=True
       dels=deliveryboys.objects.filter(d_username=deliver.d_username).first()
    loc=Location.objects.filter(usersname=user_data).first()
    context={'deliver':deliver,'orderss':orderss, 'q':q, 'p':p, 'total':total_price,'loc':loc}
    if a:
      context={'deliver':deliver,'orderss':orderss, 'q':q, 'p':p, 'total':total_price,'loc':loc,'dels':dels}
    return render(request,"orderstatus.html",context)

def home(request):
    return render(request,"home.html")
#def menu(request):
#   print("hi0")
#   if request.method=="POST":
#       print("hi1")
#       logged_in_student = request.user.username
#       id=('#add-cart').val()
#       print("hi2")
#       dish_data=dishes.objects.filter(dish_code=id)
#       ins=cart(username=logged_in_student,dish_name=dish_data.dish_name)
#       ins.save()
#   dishes_data = dishes.objects.all()
#   context = {'dishes_dat': dishes_data}
#   return render(request,"menu.html",context)

#def menu(request):
#    print("hi0")
#    if request.method=="POST":
#        print("hi1")
#        logged_in_student = request.user.username
#        id = request.POST.get('dish_code')
#        print("hi2")
#        dish_data = dishes.objects.filter(dish_code=id).first()
#        ins = cart(username=logged_in_student, dish_name=dish_data.dish_name)
#        ins.save()
#    dishes_data = dishes.objects.all()
#    context = {'dishes_dat': dishes_data}
#    return render(request,"menu.html",context)

#def menu(request):
#    if request.method=="POST":
#        logged_in_student_username = request.user.username
#        dish_code = request.POST['dish_code']
#        logged_in_student = UserProfile.objects.get(username=logged_in_student_username)
#        dish_data = dishes.objects.get(dish_code=dish_code)
#        ins = carts(user=logged_in_student,dish_codes=dish_code)
#        print(ins)
#        ins.save()
#    dishes_data = dishes.objects.all()
#    context = {'dishes_dat': dishes_data}
#    return render(request,"menu.html",context)

def menu(request):
    q=0
    logged_in_student = request.user.username
    user_data=UserProfile.objects.filter(username=logged_in_student).first()
    cart_items = cartprice.objects.filter(usere=user_data)
    for cart in cart_items:
        q=q+cart.quantity
    dishes_data = dishes.objects.all()
    loc=Location.objects.filter(usersname=user_data).first()
    context = {'dishes_dat': dishes_data, 'q':q,'carts':cart_items,'loc':loc}
    return render(request, "menu.html", context)

#def signup2(request,email):
#    if request.method=="POST":
#        verifcode=request.POST['code']
#        print(verifcode)
#        if (verifcode==code):
#            print("hi1")
#            user_data=User.objects.filter(email=email).first()
#            user_data.is_active=True
#            return redirect("sapp:signin")
#    return render(request,"signup2.html", {"code": code, "email": email})
def signup2(request,code,email,phone,username,password):
    if request.method == "POST":
        code=1000000-code
        verifcode = request.POST.get('code')
        if verifcode == str(code):
            user_data = User.objects.filter(email=email).first()
            if user_data:
                user_data.is_active = True
                user_data.save()
            ins=UserProfile(email=email,username=username,phone=phone,password=password)
            ins.save()
            messages.success(request, 'Your account has been created successfully. Please sign in.')
            return redirect("sapp:signin")
    return render(request, "signup2.html")
#def signup(request):
#    code = 0  # Initialize code outside the if block
#    
#    if request.method == "POST":
#        email = request.POST['email']
#        username = request.POST['username']
#        phone = request.POST['phone']
#        password = request.POST['password']
#        
#        if User.objects.filter(username=username).exists():
#            messages.error(request, "Username already exists")
#        elif User.objects.filter(email=email).exists():
#            messages.error(request, "Email already registered")
#        elif len(username) > 10:
#            messages.error(request, "Username must be under 10 characters")
#        elif len(phone) != 10:
#            messages.error(request, "Phone number must be 10 characters")
#        elif not username.isalnum():
#            messages.error(request, "Username must be alphanumeric")
#        else:
#            for i in range(6):
#                j = random.randint(1, 9)
#                code = j + code * 10
#                
#            subject = 'Verification code'
#            message = f'Your Verification code is: {code}'
#            from_email = 'ramanaidulokam@gmail.com'  # Update with your email address
#            recipient_list = [email]
#            send_mail(subject, message, from_email, recipient_list)
#            
#            # Create user
#            myuser = User.objects.create_user(username, email, password)
#            myuser.is_active = False
#            myuser.save()
#  # Redirect to signup2 view with email
#        
#    elif request.method == "GET":
#        verifcode = request.GET.get('code')  # Fetch verifcode from query params
#        if verifcode == str(code):  # Convert code to string for comparison
#            myuser.is_active = True
#            myuser.save()
#            # Create UserProfile instance
#            ins = UserProfile(email=email, username=username, phone=phone, password=password)
#            ins.save()
#            messages.success(request, 'Your account has been created successfully. Please sign in.')
#            return render(request, "signin.html")
#       
#    return render(request, "signup.html")
#def signup(request):
#    if request.method=="POST":
#        email=request.POST['email']
#        username=request.POST['username']
#        phone=request.POST['phone']
#        password=request.POST['password']
#        if User.objects.filter(username=username):
#            messages.error(request,"username already exists")
#        elif User.objects.filter(email=email):
#            messages.error(request,"Email already registered")
#        elif len(username)>10:
#            messages.error(request,"username must be under 10 characters")
#        elif (len(phone)>10) or (len(phone)<10):
#            messages.error(request,"phone number must be 10 characters")
#        elif not username.isalnum():
#            messages.error(request,"username must be a alpha numeric")
#        else:
#            code=0
#            for i in range(6):
#                j=random.randint(1,9)
#                code=j+code*10
#            subject = 'Verification code'
#            message = f'Your Verification code is: {code}'
#            from_email = 'ramanaidulokam@gmail.com'  # Update with your email address
#            recipient_list = [email]
#            send_mail(subject, message, from_email, recipient_list)
#            myuser = User.objects.create_user(username, email, password)
#            myuser.is_active=False
#            myuser.save()
#            code=1000000-code
#            return redirect(reverse('sapp:signup2', kwargs={'code': code, 'email': email,'phone':phone,'password':password,'username':username}))
#            #return redirect(request,"signup2.html",code=code, email=email)
#    return render(request,"signup.html")
def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        phone = request.POST['phone']
        password = request.POST['password']
        try:
            if User.objects.filter(username=username):
                messages.error(request, "Username already exists")
            elif User.objects.filter(email=email):
                messages.error(request, "Email already registered")
            elif len(username) > 10:
                messages.error(request, "Username must be under 10 characters")
            elif len(phone) != 10:
                messages.error(request, "Phone number must be 10 characters")
            elif not username.isalnum():
                messages.error(request, "Username must be alphanumeric")
            else:
                code = 0
                for i in range(6):
                    j = random.randint(1, 9)
                    code = j + code * 10
                subject = 'Verification code'
                message = f'Your Verification code is: {code}'
                from_email = 'ramanaidulokam@gmail.com'  # Update with your email address
                recipient_list = [email]
                try:
                    send_mail(subject, message, from_email, recipient_list)
                    myuser = User.objects.create_user(username, email, password)
                    myuser.is_active = False
                    myuser.save()
                    code = 1000000 - code
                    return redirect(reverse('sapp:signup2', kwargs={'code': code, 'email': email, 'phone': phone, 'password': password, 'username': username}))
                except BadHeaderError:
                    messages.error(request, "Invalid header found in email")
                except Exception as e:
                    messages.error(request, f"Error sending email: {str(e)}")
                    return render(request, "signup.html", {'email_error': True})  # Render signup page with error
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return render(request, "signup.html")
#def foruser(request):
#    if request.method == "POST":
#        email = request.POST.get('email')
#        user_profile = UserProfile.objects.filter(email=email).first()
#        if user_profile:
#            # Send email containing the forgotten username
#            subject = 'Forgotten Username'
#            message = f'Your username is: {user_profile.username}'
#            from_email = 'ramanaidulokam@gmail.com'  # Update with your email address
#            recipient_list = [email]
#            send_mail(subject, message, from_email, recipient_list)
#            return render(request, "foruser.html", {'success': True})
#        else:
#            return render(request, "foruser.html", {'error': 'No user found with this email.'})    
#    return render(request,"foruser.html")
#def signup(request):
#    if request.method == "POST":
#        email = request.POST['email']
#        username = generate_unique_username([email])  # Generate a unique username based on email
#        phone = request.POST['phone']
#        password = request.POST['password']
#
#        if User.objects.filter(username=username).exists():
#            messages.error(request, "Username already exists")
#        elif User.objects.filter(email=email).exists():
#            messages.error(request, "Email already registered")
#        elif len(username) > 10:
#            messages.error(request, "Username must be under 10 characters")
#        elif len(phone) != 10:
#            messages.error(request, "Phone number must be 10 characters")
#        elif not username.isalnum():
#            messages.error(request, "Username must be alphanumeric")
#        else:
#            myuser = User.objects.create_user(username, email, password)
#            myuser.save()
#            ins = UserProfile(email=email, username=username, phone=phone, password=password)
#            ins.save()
#
#    return render(request, "signup.html")

def address3(request):
    logged_in_student=request.user.username
    userss=UserProfile.objects.filter(username=logged_in_student).first()
    if request.method=="POST":
        streetname=request.POST['streetname']
        villagecity=request.POST['villagecity']
        pincode=request.POST['pincode']
        state=request.POST['state']
        country=request.POST['country']
        ins=Location(usersname=userss,streetname=streetname,villagecity=villagecity,pincode=pincode,state=state,country=country)
        ins.save()
        return redirect("sapp:menu")
    return render(request,"address3.html")

def signin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=UserProfile.objects.filter(username=username,password=password).first()
        locc=Location.objects.filter(usersname=user).first()
        if user is not None:
            user=authenticate(request=request,username=username,password=password)
            login(request,user)
            dishes_data = dishes.objects.all()
            context = {'dishes_dat': dishes_data}
            ord=orders.objects.filter(user_name=username)
            #if ord is not None:
            #    return redirect("sapp:orderstatus")
            #return redirect("sapp:menu")
            if orders.objects.filter(user_name=username,order_delivered=False).exists():
                return redirect("sapp:orderstatus")
            elif locc is not None:
                return redirect("sapp:menu")
            else:
                return redirect("sapp:address3")
        else:
            messages.error(request,"you entered wrong credentials")
            return render(request,"signin.html")
    return render(request,"signin.html")

def locationform(request):
    return render(request,"inputform.html")
from itertools import groupby
#def profile(request):
#    q=0
#    group={}
#    logged_in_student = request.user.username
#    user_data=UserProfile.objects.filter(username=logged_in_student).first()
#    cart_items = cartprice.objects.filter(usere=user_data)
#    for cart in cart_items:
#      q=q+cart.quantity
#    loc=Location.objects.filter(usersname=user_data).first()
#    orde=orders.objects.filter(user_name=logged_in_student,order_delivered=True)
#    for ord in orde:
#      dis=dishes.objects.filter(dish_name=ord.dish_name)
#      print(dis)
#      for dish_name, image in groupby(dis, key=lambda x: x.dish_name):
#        group[dish_name] = list(image)
#    print(group)
#    context={'user_dat':user_data, 'q':q,'loc':loc,'orde':orde}
#    return render(request,"profile.html",context)
from django.conf import settings

#def profile(request):
#    q = 0
#    group = {}
#    logged_in_student = request.user.username
#    user_data = UserProfile.objects.filter(username=logged_in_student).first()
#    cart_items = cartprice.objects.filter(usere=user_data)
#    
#    for cart in cart_items:
#        q += cart.quantity
#    
#    loc = Location.objects.filter(usersname=user_data).first()
#    orde = orders.objects.filter(user_name=logged_in_student, order_delivered=True)
#    
#    for ord in orde:
#        dis = dishes.objects.filter(dish_name=ord.dish_name)
#        for dish in dis:
#            if dish.dish_name not in group:
#                group[dish.dish_name] = {
#                    settings.MEDIA_URL + str(dish.image)
#                }
#    print(group)
#    context = {'user_dat': user_data, 'q': q, 'loc': loc, 'orde': orde, 'group': group}
#    return render(request, "profile.html", context)
#from django.conf import settings
#def profile(request):
#    q = 0
#    iy=0
#    re={}
#    group = {}
#    context={}
#    logged_in_student = request.user.username
#    user_data = UserProfile.objects.filter(username=logged_in_student).first()
#    cart_items = cartprice.objects.filter(usere=user_data)
#    
#    for cart in cart_items:
#        q += cart.quantity
#    pre={}
#    loc = Location.objects.filter(usersname=user_data).first()
#    orde = order.objects.filter(user_name=logged_in_student)
#    ty=orde.count()
#    if orde is None:
#        context= {'user_dat': user_data, 'q': q, 'loc': loc}
#    else:
#        for ord in orde:
#            iy+=1
#            rev=Review.objects.filter(ords=ord).first()
#            print(rev)
#            if rev is None:
#              pre[ord.dish_name]=ord.id
#              dis = dishes.objects.filter(dish_name=ord.dish_name)
#              for dish in dis:
#                  if dish.dish_name not in group:
#                      group[dish.dish_name] = settings.MEDIA_URL + str(dish.image)
#            else:
#                re[rev.user]=rev.ords
#                pre[ord.dish_name]=ord.id
#                dis = dishes.objects.filter(dish_name=ord.dish_name)
#                for dish in dis:
#                    if dish.dish_name not in group:
#                        group[dish.dish_name] = settings.MEDIA_URL + str(dish.image)
#        # Extracting just the image URLs from the dictionary
#        print(re)
#        #image_urls = list(group.values())
#        context = {'user_dat': user_data, 'q': q, 'loc': loc, 'orde': orde,'pre':pre,'re':re,'group':group}
#    return render(request, "profile.html", context)
#def profile(request):
#    q = 0
#    re = {}
#    group = {}
#    context = {}
#    logged_in_student = request.user.username
#    user_data = UserProfile.objects.filter(username=logged_in_student).first()
#    cart_items = cartprice.objects.filter(usere=user_data)
#    
#    for cart in cart_items:
#        q += cart.quantity
#    
#    pre = {}
#    loc = Location.objects.filter(usersname=user_data).first()
#    orde = order.objects.filter(user_name=logged_in_student)
#    
#    # Get the length of the queryset `orde`
#    orde_length = orde.count()
#    
#    if orde_length == 0:
#        context = {'user_dat': user_data, 'q': q, 'loc': loc}
#    else:
#        for ord in orde:
#            rev = Review.objects.filter(ords=ord).first()
#            print(rev)
#            if rev:
#                re[rev.user] = rev.ords
#            pre[ord.dish_name] = ord.id
#            dis = dishes.objects.filter(dish_name=ord.dish_name)
#            for dish in dis:
#                if dish.dish_name not in group:
#                    group[dish.dish_name] = settings.MEDIA_URL + str(dish.image)
#        
#        # Extracting just the image URLs from the dictionary
#        print(re)
#        image_urls = list(group.values())
#        context = {'user_dat': user_data, 'q': q, 'loc': loc, 'orde': orde, 'image_urls': image_urls, 'pre': pre, 're': re, 'group': group}
#    
#    return render(request, "profile.html", context)
def profile(request):
    q = 0
    rt=False
    re = {}  # Change this to a dictionary where each user has a list of reviews
    group = {}
    context = {}
    r={}
    lrn=False
    logged_in_student = request.user.username
    user_data = UserProfile.objects.filter(username=logged_in_student).first()
    cart_items = cartprice.objects.filter(usere=user_data)
    irs=orders.objects.filter(user_name=logged_in_student)
    if not irs:
        lrn=True
    for cart in cart_items:
        q += cart.quantity
    
    pre = {}
    loc = Location.objects.filter(usersname=user_data).first()
    orde = order.objects.filter(user_name=logged_in_student)
    
    # Get the length of the queryset `orde`
    orde_length = orde.count()
    
    if orde_length == 0:
        context = {'user_dat': user_data, 'q': q, 'loc': loc}
    else:
        for ord in orde:
            rev = Review.objects.filter(ords=ord).first()
            if rev:
                # Append the review to the list of reviews for the user
                if rev.user not in re:
                    re[rev.user] = []
                    r[rev.user] = {}
                r[rev.user][rev.ords]=rev.points
                re[rev.user].append(rev.ords)
            pre[ord.dish_name] = ord.id
            dis = dishes.objects.filter(dish_name=ord.dish_name)
            for dish in dis:
                if dish.dish_name not in group:
                    group[dish.dish_name] = settings.MEDIA_URL + str(dish.image)
        
        # Extracting just the image URLs from the dictionary
       #print(r)
       #print(re)
       #print(pre)
        if not re:
            rt=True
       #print(rt)
        image_urls = list(group.values())
        context = {'user_dat': user_data, 'q': q, 'loc': loc, 'orde': orde, 'image_urls': image_urls, 'pre': pre, 'lrn':lrn, 're': re, 'rt':rt, 'r':r, 'group': group}
    
    return render(request, "profile.html", context)

#def review(request):
#    logged_in_user=request.user.username
#    user=UserProfile.objects.filter(username=logged_in_user)
#    if request.method=="POST":
#        orderid=request.POST['orderid']
#        point = request.POST['point']
#        comp = request.POST['comp']
#        ordss=orders.objects.filter(id=orderid).first()
#        dish=dishes.objects.filter(dish_name=ordss.dish_name)
#        ins=review(ords=ordss,user=user,dish=dish,points=point,complaint=comp)
#        ins.save()
#    return redirect("sapp:profile")
def review(request):
    logged_in_user = request.user.username
    user = UserProfile.objects.get(username=logged_in_user)  # Assuming only one user can exist with a specific username
    if request.method == "POST":
        order_id = request.POST['orderid']
        point = request.POST['point']
        comp = request.POST['comp']
        ordss = order.objects.get(id=order_id)
        dish = dishes.objects.get(dish_name=ordss.dish_name)
        # Assuming 'Review' model is imported as well
        ins = Review.objects.create(ords=ordss, user=user, dish=dish, points=point, complaint=comp)
    return redirect("sapp:profile")

#def cart(request):
 #   return render(request,"cart.html")

#def view_cart(request):
#    q=0
#    logged_in_student = request.user.username
#    user_data=UserProfile.objects.filter(username=logged_in_student).first()
#    cart_items = carts.objects.filter(user=user_data)
#    total_price=0
#    for cart_item in cart_items:
#        dish = cart_item.dish_codes
#        price = dish.price
#        total_price = total_price+price*cart_item.quantity
#    for cart in cart_items:
#      q=q+cart.quantity
#    context={'cart_item': cart_items,'total_price': total_price,'q':q}
#    return render(request, 'cart.html', context)#, 'total_price': total_price})

#def forget(request):
#    if request.method=="POST":
#        email=request.POST['email']
#        password=request.POST['password']
#        conpassword=request.POST['conpassword']
#        userss=UserProfile.objects.filter(email=email).first()
#        if password==conpassword:
#          if userss is not None:
#              myuser = User.objects.filter(email=email).first()
#              us=myuser.username
#              myuser.delete()
#              myusers = User.objects.create_user(us, email, password)
#              myusers.save()
#              myuser.delete()
#              ins=UserProfile(email=email,username=userss.username,phone=userss.phone,password=password)
#              ins.save()
#              userss.delete()
#    return render(request,"forget.html")
def forget(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        conpassword = request.POST.get('conpassword')

        if password == conpassword:
            user_profile = UserProfile.objects.filter(email=email).first()
            if user_profile is not None:
                user = User.objects.filter(email=email).first()
                if user:
                    # Update the password for the existing user
                    user.set_password(password)
                    user.save()
                    # Update the password for UserProfile
                    user_profile.password = password
                    user_profile.save()
                    return redirect('sapp:signin')  # Redirect to login page after password reset
            else:
                # Handle case when user_profile doesn't exist
                return render(request, "forget.html", {'error': 'User not found!'})
        else:
            # Handle case when passwords don't match
            return render(request, "forget.html", {'error': 'Passwords do not match!'})

    return render(request, "forget.html")

def foruser(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user_profile = UserProfile.objects.filter(email=email).first()
        if user_profile:
            # Send email containing the forgotten username
            subject = 'Forgotten Username'
            message = f'Your username is: {user_profile.username}'
            from_email = 'ramanaidulokam@gmail.com'  # Update with your email address
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            return render(request, "foruser.html", {'success': True})
        else:
            return render(request, "foruser.html", {'error': 'No user found with this email.'})    
    return render(request,"foruser.html")

def view_cart(request):
    q=0
    p=False
    logged_in_student = request.user.username
    user_data=UserProfile.objects.filter(username=logged_in_student).first()
    cart_items = cartprice.objects.filter(usere=user_data)
    total_price=0
    for cart_item in cart_items:
        dish = cart_item.dish_codese
        price = dish.price
        total_price = total_price+((cart_item.quantity*price)-price*cart_item.quantity*(0.01)*cart_item.discount)
    for cart in cart_items:
      q=q+cart.quantity
    locc=Location.objects.filter(usersname=user_data).first()
    ord=orders.objects.filter(user_name=logged_in_student,order_delivered=False)
    if ord.exists():
        p = True
    context={'cart_item': cart_items,'total_price': total_price,'q':q,'locc':locc,'ord':ord,'p':p}
    return render(request, 'cart.html', context)#, 'total_price': total_price})

#def view_cart(request):
#    logged_in_student = request.user.username
#    user_data=UserProfile.objects.filter(username=logged_in_student)
#    cart_items = carts.objects.filter(user=user_data)
#    #total_price = sum(item.product.price * item.quantity for item in cart_items)
#    return render(request, 'cart.html', {'cart_items': cart_items}) #'total_price': total_price})
 
#def add_to_cart(request, product_id):
#    logged_in_student = request.user.username
#    user_data=UserProfile.objects.filter(username=logged_in_student).first()
#    #product = get_object_or_404(dishes, dish_code=product_id)
#    product = dishes.objects.get(dish_code=product_id)
#    cart_item, created = carts.objects.get_or_create(dish_codes=product.dish_code,user=user_data)
#    cart_item.quantity += 1
#    cart_item.save()
#    return redirect('cart:view_cart')


#def add_to_cart(request, product_id):
#    logged_in_student = request.user.username
#    user_data = UserProfile.objects.filter(username=logged_in_student).first()
#    # Get the dish object or return a 404 if not found
#    product = get_object_or_404(dishes, dish_code=product_id)
#    # Use update_or_create to simplify the logic
#    print(product.price)
#    cart_item, created = carts.objects.update_or_create(
#        dish_codes=product,
#        user=user_data,
#        defaults={'quantity': 1}  # Set default quantity to 1 if the cart item is created
#    )
#    if not created:
#        # If the cart item already exists, increment the quantity
#        cart_item.quantity += 1
#        cart_item.save()
#    #return render(request,"menu.html")
#    #return redirect('sapp:view_cart')
#    return redirect('sapp:view_cart')
 
def add_to_cart(request, product_id):
    logged_in_student = request.user.username
    user_data = UserProfile.objects.filter(username=logged_in_student).first()
    # Get the dish object or return a 404 if not found
    product = get_object_or_404(dishes, dish_code=product_id)
    products = get_object_or_404(dishes, dish_code=product_id)
    # Use update_or_create to simplify the logic
    p=0.01
    q=1
    cart_item, created = cartprice.objects.update_or_create(
        dish_codese=product,
        usere=user_data,
        price=product.price,
        discount=product.discount,
        defaults={'quantity': 1},
        finalprice=product.price-(product.price*q*product.discount*p)  
    )
    if not created:
        # If the cart item already exists, increment the quantity
        cart_item.quantity += 1
        cart_item.finalprice=((cart_item.quantity*product.price)-(product.price*cart_item.quantity*product.discount*p))
        cart_item.save()
    #return render(request,"menu.html")
    #return redirect('sapp:view_cart')
    return redirect('sapp:view_cart') 
 
def remove_from_cart(request, item_id):
    cart_item = carts.objects.get(id=item_id)
    cart_item.delete()
    return redirect('sapp:view_cart')