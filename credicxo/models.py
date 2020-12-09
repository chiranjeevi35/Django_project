from django.db import models

# Create your models here.

class signup_info(models.Model):
    name=models.CharField(max_length=50)
    pwd=models.CharField(max_length=250)
    mob_no=models.CharField(max_length=10)
    email=models.CharField(max_length=150,primary_key=True)
    role = models.CharField(max_length=10,blank=True)
