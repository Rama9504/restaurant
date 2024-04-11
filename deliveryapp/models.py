from django.db import models

# Create your models here.
class deliverdetails(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=10)

    def __str__(self):
        return self.username