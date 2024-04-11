from django.db import models

# Create your models here.

class UserProfile(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True,max_length=100,primary_key=True)
    phone = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=128)
    def __str__(self):
        return self.username
    
class Location(models.Model):
    usersname=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    streetname=models.CharField(max_length=50,default="a")
    villagecity=models.CharField(max_length=50,default="v")
    pincode=models.BigIntegerField(default=0)
    state=models.CharField(max_length=50,default="andhra pradesh")
    country=models.CharField(max_length=50,default="india")
    def __str__(self):
        return str(self.usersname)
    