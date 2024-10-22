from django.db import models
from django.contrib.auth.models import User
from services.models import ServiceType
from django.forms import ValidationError
from django.utils import timezone
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_provider = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    def clean(self):
        if self.is_provider and self.is_client:
            raise ValidationError("A user cannot be both a provider and a client.")

class Provider(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    #services_offered = models.ManyToManyField(Service)
    name = models.CharField(max_length=100,blank=True, null=True)
    age = models.PositiveIntegerField( blank=True, null=True)
    gender = models.CharField(max_length=10,blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100,default='unknown')
    phone_number = models.CharField(max_length=15,blank=True, null=True)
    alternate_phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='user_pics/', blank=True, null=True)
    
    aadhar_number = models.CharField(max_length=12, blank=True, null=True)
    #dob = models.DateField(blank=True, null=True)
    #identification = models.CharField(max_length=100,blank=True, null=True)
    bank_account = models.CharField(max_length=20,null=True)
    ifsc_code = models.CharField(max_length=11,null=True)
    govt_id = models.FileField(upload_to='govt_ids/', blank=True, null=True)
    #verified = models.BooleanField(default=False)

    #health_condition = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    service_types = models.ManyToManyField('services.ServiceType', blank=True)
    availability = models.CharField(max_length=50, choices=[
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
    ], blank=True, null=True)
    hourly_salary = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    about_me = models.TextField(blank=True, null=True)
    password=models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - Provider"

class Client(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True, null=True)
    age = models.PositiveIntegerField( blank=True, null=True)
    gender = models.CharField(max_length=10,blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100,default='unknown')
    phone_number = models.CharField(max_length=15,blank=True, null=True)
    alternate_phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='user_pics/', blank=True, null=True)
    
    aadhar_number = models.CharField(max_length=12, blank=True, null=True)
    #dob = models.DateField(blank=True, null=True)
    #identification = models.CharField(max_length=100,blank=True, null=True)
    bank_account = models.CharField(max_length=20,null=True)
    ifsc_code = models.CharField(max_length=11,null=True)
    govt_id = models.FileField(upload_to='govt_ids/', blank=True, null=True)
    #verified = models.BooleanField(default=False)

    #health_condition = models.TextField(blank=True, null=True)
    #experience = models.TextField(blank=True, null=True)
    service_needed = models.ManyToManyField('services.ServiceType', blank=True)
    availability = models.CharField(max_length=50, choices=[
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('temporary', 'Temporary'),
    ], blank=True, null=True)
    #hourly_salary = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    about_work = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - Client"







