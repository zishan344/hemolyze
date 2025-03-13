from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
user = get_user_model()

class BloodRequest(models.Model):
    CHOICE_BLOOD_GROUPS =[
        ('A+','A+'),
        ('A-','A-'),
        ('B+','B+'),
        ('B-','B-'),
        ('AB+','AB+'),
        ('AB-','AB-'),
        ('O+','O+'),
        ('O-','O-'),
    ]
    user = models.ForeignKey(user, on_delete=models.CASCADE,related_name='blood_request')
    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=10, choices=CHOICE_BLOOD_GROUPS)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
    
class AcceptRequest(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='accept_request')
    request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE,related_name='accepted_by')
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} accepted by {self.request}"