from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    bio = models.CharField(max_length=100)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self) :
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image", default="userimage.jpg")
    full_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username
    
class ContactUs(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="XYZ@gmail.com")
    phone = models.CharField(max_length=50, default="+123 (456) 789")
    subject = models.CharField(max_length=50, default="Help!")
    message = models.TextField()

    def __str__(self) -> str:
        return self.full_name
    
    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_profile, sender = User)
post_save.connect(save_profile, sender = User)