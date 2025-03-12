from django.db import models
from django.contrib.auth.models import User

class UserDetails(models.Model):
    """ this is user detail model """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userdetails')
    address = models.TextField()
    age = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    last_donation_date = models.DateField(blank=True, null=True)
    availability_status = models.BooleanField()
    
    def __str__(self):
        return self.user.username