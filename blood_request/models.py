from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.exceptions import ValidationError as DRFValidationError
from user.models import UserDetails
User = get_user_model()  
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
    PENDING = 'pending'
    DONATED = 'donated'
    CANCELED = 'canceled'
    BLOOD_STATUS = [
        (PENDING, 'Pending'),
        (DONATED, 'Donated'),
        (CANCELED, 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accept_requests')
    request_accept = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name='accepted_by')
    request_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    donation_status = models.CharField(max_length=10, choices=BLOOD_STATUS, default=PENDING)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.request_user_id:
            self.request_user = self.request_accept.user
            
        try:
            donor_details = UserDetails.objects.get(user=self.user)
            if self.donation_status == self.DONATED:
                donor_details.last_donation_date = timezone.now().date()
                donor_details.save()
        except ObjectDoesNotExist:
            raise DRFValidationError({
                "error": "Please complete your profile details before changing donation status.",
                "status": 400
            })
            
        super().save(*args, **kwargs)
        
        received_blood, created = ReceivedBlood.objects.get_or_create(
            user=self.request_user,
            donor=self.user,
            accept_request=self,
            defaults={
                'received_status': ReceivedBlood.PENDING,
                'donor': self.user 
            }
        )
        
        # Update ReceivedBlood status
        if self.donation_status == self.DONATED:
            received_blood.received_status = ReceivedBlood.RECEIVED
        elif self.donation_status == self.CANCELED:
            received_blood.received_status = ReceivedBlood.CANCELED
        else:
            received_blood.received_status = ReceivedBlood.PENDING
        received_blood.blood_post = self.request_accept
        received_blood.save()

    def __str__(self):
        user_str = str(self.user.username) if self.user.username else str(self.user.email)
        request_str = str(self.request_accept)
        return f"{user_str} accepted {request_str}"

    class Meta:
        unique_together = ['user', 'request_accept']

class ReceivedBlood(models.Model):
    PENDING = 'pending'
    RECEIVED = 'received'
    CANCELED = 'canceled'
    BLOOD_STATUS = [
        (PENDING, 'Pending'),
        (RECEIVED, 'Received'),
        (CANCELED, 'Canceled'),
    ]
    blood_post = models.ForeignKey(BloodRequest, on_delete=models.SET_NULL, null=True, related_name='blood_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donor')
    accept_request = models.ForeignKey('AcceptBloodRequest', on_delete=models.CASCADE, related_name='received_blood')
    received_status = models.CharField(max_length=10, choices=BLOOD_STATUS, default=PENDING)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blood donation from {self.donor} to {self.user} - {self.received_status}"


