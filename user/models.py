from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class NGO(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  
    organization_name = models.CharField(max_length=255)  
    email = models.EmailField(unique=True, null=False, blank=False)  
    contact_person = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.organization_name


class Donation(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Request Sent'),
        ('accepted', 'Request Accepted'),
        ('received', 'Donation Received'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='donation_images/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    mfg_date = models.DateField(blank=True, null=True)
    exp_date = models.DateField(blank=True, null=True)
    date_donated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent')  
    assigned_ngo = models.ForeignKey(NGO, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.item_name} ({self.status})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    mobile_number = models.CharField(max_length=15, blank=True, null=True)  

    def __str__(self):
        return f'{self.user.username} Profile'

class SystemMessage(models.Model):
    key = models.CharField(max_length=10, unique=True)  
    message = models.TextField()

    def __str__(self):
        return self.key


class Message(models.Model):
    message_type = models.CharField(max_length=50)  
    content = models.TextField()

    def __str__(self):
        return f"{self.message_type}"


