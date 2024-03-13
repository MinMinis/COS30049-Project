from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import uuid
from backend_app.manager import UserManager
from django.contrib.auth.signals import user_logged_in, user_logged_out 
from django.utils import timezone
import random 
import bcrypt
from django.conf import settings

from django.core.mail import EmailMessage

def generate_random_pin():
    pin = str(random.randint(1000000, 9999999))
    return bytes(pin, 'utf-8')

class User(AbstractUser):
    username = models.CharField(max_length= 255 , unique = True ) 
    email = models.EmailField( unique=True)
    last_name = models.CharField( max_length = 100 )
    first_name = models.CharField( max_length = 100 )
    phoneNumber = models.CharField( max_length = 20 )
    pin = models.BinaryField(unique=True , default = generate_random_pin)
    user_address = models.CharField( max_length = 255 )
    data = models.JSONField(default=dict)
    is_superuser = models.BooleanField( default= False ) 
    is_active = models.BooleanField( default= False ) 
    is_staff = models.BooleanField( default= False ) 
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length= 6 , null = True , blank = True)
    date_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(auto_now = True )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'last_name', 'first_name', 'phoneNumber']
    
    objects = UserManager()
    
    @property
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email

    def token(self):
        pass

class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    expiration_time = models.DateTimeField(default=timezone.now)

    def check_run_time(self) : 
        return timezone.now() > self.expiration_time


    def __str__(self):
        return f"{self.user.first_name} - passcode"
    

class SaveEmailModel(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6, unique=True)
    expiration_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.email
    def check_run_time(self) : 
        return timezone.now() > self.expiration_time

class HistoryModel(models.Model):
    user_address = models.CharField(max_length = 255 , default='' )
    username = models.CharField(max_length = 255 , default='' )
    hash_block = models.CharField(max_length= 255 ,default= 'default' ,blank = True) 
    contract_address = models.CharField(max_length = 255 , default = "default" , blank = True)
    transaction_hash = models.CharField(max_length = 255 , default= "default"  ,blank = True)
    hash_block_transaction = models.CharField(max_length = 255 , default = "" , blank = True)
    execute_transaction_hash = models.CharField(max_length = 255 , default = "" , blank = True)
    receiver_address  = models.CharField(max_length = 255 , default = "" , blank = True)
    is_send = models.BooleanField(default=False)

    def __str__(self) : 
        return self.username