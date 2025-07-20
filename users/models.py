from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    # is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255, blank=True,null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
class ContactInfo(models.Model):
    map = models.URLField(max_length=1000,blank=True, null=True)
    email = models.EmailField()
    address= models.CharField(max_length=200)
    sub_address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15)
    facebook = models.CharField(max_length=50)
    twitter = models.CharField(max_length=50)
    youtube = models.CharField(max_length=50)
    instagram = models.CharField(max_length=50)


class ContactUs(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    email= models.EmailField()
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f"Contact from {self.name} ({self.email})"
