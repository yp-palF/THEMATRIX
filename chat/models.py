from django.db import models
from django.contrib.auth.models import User
	
class Profile(models.Model):
    title=models.CharField(max_length=10)
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    gender=models.CharField(max_length=6)
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    image=models.CharField(max_length=200)
    user_name=models.OneToOneField(User,primary_key=True,related_name='profile')
    
class Message(models.Model):
	message=models.CharField(max_length=200)
	user_name=models.CharField(max_length=10)
	image=models.CharField(max_length=200)
    
    
    
