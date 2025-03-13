from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Use capital 'U' for class names

class BloodRequest(models.Model):
    CHOICE_BLOOD_GROUPS = [
        ('A+','A+'),
        ('A-','A-'),
        ('B+','B+'),
        ('B-','B-'),
        ('AB+','AB+'),
        ('AB-','AB-'),
        ('O+','O+'),
        ('O-','O-'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_request')
    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=10, choices=CHOICE_BLOOD_GROUPS)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blood request by {str(self.user.username) if self.user.username else str(self.user.email)}"
    
class AcceptBloodRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accept_request')
    request_accept = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name='accepted_by')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_str = str(self.user.username) if self.user.username else str(self.user.email)
        request_str = str(self.request_accept)
        return f"{user_str} accepted {request_str}"