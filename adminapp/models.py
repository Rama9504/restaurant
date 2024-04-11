from django.db import models
from sapp.models import UserProfile, Location
# Create your models here.

class adminss(models.Model):
    username = models.CharField(max_length=20, unique=True,default=0)
    password = models.CharField(max_length=10)

    def __str__(self):
        return self.username


class dishes(models.Model):
    VEG_BIRYANI = 'vegbiryani'
    NON_VEG_BIRYANI = 'nonvegbiryani'
    NON_VEG_STARTER = 'nonvegstarter'
    VEG_STARTER = 'vegstarter'

    DISH_TYPES_CHOICES = [
        (VEG_BIRYANI, 'Veg Biryani'),
        (NON_VEG_BIRYANI, 'Non-Veg Biryani'),
        (NON_VEG_STARTER, 'Non-Veg Starter'),
        (VEG_STARTER, 'Veg Starter'),
    ]

    dish_name = models.CharField(max_length=50, unique=True)
    dish_code = models.CharField(max_length=20, unique=True)
    price = models.IntegerField()
    types = models.CharField(max_length=20, choices=DISH_TYPES_CHOICES)
    availability = models.BooleanField(default=True)
    image = models.ImageField(upload_to='dishes/images/', height_field=None, width_field=None, max_length=None)
    discount = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.dish_name


class deliveryboys(models.Model):
    email=models.EmailField(unique=True,default=0)
    d_username = models.CharField(max_length=20, unique=True,primary_key=True)
    d_name = models.CharField(max_length=50)
    d_phone = models.PositiveBigIntegerField()
    availability = models.BooleanField(default=True)
    password=models.CharField(max_length=12,default=0)

    def __str__(self):
        return self.d_name  # Corrected from self.name

class orders(models.Model):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    dish_name = models.ForeignKey(dishes, on_delete=models.CASCADE, related_name='orders_dish_name')
    dish_code = models.ForeignKey(dishes, on_delete=models.CASCADE, related_name='orders_dish_code')
    quantity = models.IntegerField()
    date_of_order=models.DateField()
    finalpricee=models.FloatField(default=0.0)
    delivery_boy_assigned=models.BooleanField(default=False)
    delivery_boy_pickedpackage=models.BooleanField(default=False)
    order_delivered=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user_name} - {self.dish_name} - {self.quantity}"

class order(models.Model):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    dish_name = models.ForeignKey(dishes, on_delete=models.CASCADE, related_name='orders_dish_namee')
    dish_code = models.ForeignKey(dishes, on_delete=models.CASCADE, related_name='orders_dish_codee')
    quantity = models.IntegerField()
    date_of_order=models.DateField()
    finalpricee=models.FloatField(default=0.0)
    delivery_boy_assigned=models.BooleanField(default=False)
    delivery_boy_pickedpackage=models.BooleanField(default=False)
    order_delivered=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user_name} - {self.dish_name} - {self.quantity}"


class orderverif(models.Model):
    useres=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    orderse=models.ForeignKey(orders,on_delete=models.CASCADE)
    verifcode=models.BigIntegerField()

class deliverymapping(models.Model):
    users = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='deliverymapping_username')
    d_username = models.ForeignKey(deliveryboys, on_delete=models.CASCADE, related_name='deliverymapping_d_username')
    address = models.TextField(max_length=300,default=0)
    phone = models.BigIntegerField()
    def __str__(self):
        return f"{self.users}-{self.d_username}"
    
class deliverymappings(models.Model):
    ord=models.ForeignKey(orders, on_delete=models.CASCADE, related_name='orders_user')
    users = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='deliverymapping_usernames')
    d_username = models.ForeignKey(deliveryboys, on_delete=models.CASCADE, related_name='deliverymapping_d_usernames')
    address = models.TextField(max_length=300,default=0)
    phone = models.BigIntegerField()
    def __str__(self):
        return f"{self.users}-{self.d_username}"

class deliverymappingss(models.Model):
    ord=models.ForeignKey(order, on_delete=models.CASCADE, related_name='orders_usere')
    users = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='deliverymapping_usernamese')
    d_username = models.ForeignKey(deliveryboys, on_delete=models.CASCADE, related_name='deliverymapping_d_usernamese')
    address = models.TextField(max_length=300,default=0)
    phone = models.BigIntegerField()
    def __str__(self):
        return f"{self.users}-{self.d_username}"    

class carts(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    dish_codes = models.ForeignKey(dishes,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
 
    def __str__(self):
        return f'{self.quantity} x {self.dish_codes}'
    
    
class cartprice(models.Model):
    usere = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    dish_codese = models.ForeignKey(dishes,on_delete=models.CASCADE)
    price=models.IntegerField()
    finalprice =models.FloatField(default=0.0)
    discount=models.IntegerField()
    quantity=models.IntegerField()
    def __str__(self):
      return f'{self.quantity} x {self.dish_codese}'
  
class Review(models.Model):
    ords=models.ForeignKey(order, on_delete=models.CASCADE)
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    dish=models.ForeignKey(dishes,on_delete=models.CASCADE)
    points=models.IntegerField()
    complaint=models.CharField(max_length=200)
    def __str__(self):
        return f'{self.dish} x {self.points} x {self.user}'
    