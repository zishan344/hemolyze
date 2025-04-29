from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
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
    # urgency_level: "normal" | "urgent" | "critical";
    CHOICE_URGENCY_LEVEL = [
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('critical', 'Critical'),
    ]
    # RequestStatus "pending" | "accepted" | "completed" | "cancelled"
    REQUEST_STATUS = [
        ("pending", 'Pending'),
        ("accepted", 'Accepted'),
        ("completed", 'Completed'),
        ("cancelled", 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_request')
    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=10, choices=CHOICE_BLOOD_GROUPS)
    required_units = models.IntegerField()
    fulfilled_units = models.IntegerField(default=0)
    urgency_level = models.CharField(max_length=10, choices=CHOICE_URGENCY_LEVEL, default='normal')
    phone = models.CharField(max_length=15)
    hospital_address = models.TextField()
    hospital_name = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=REQUEST_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Update status based on fulfilled units
        if self.fulfilled_units >= self.required_units:
            self.status = 'completed'
        super().save(*args, **kwargs)

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
    
    # Frontend action indicators (not stored in database)
    CANCELED_BY_DONOR = 'canceled_by_donor'
    CANCELED_BY_USER = 'canceled_by_user'
    ACCEPTED_BY_USER = 'accepted_by_user'
    # ACCEPTED_BY_DONOR = 'accepted_by_DONOR'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accept_requests')
    request_user = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name='received_requests')
    request_accept = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accepted_by')
    
    donation_status = models.CharField(max_length=10, choices=BLOOD_STATUS, default=PENDING)
    units = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Set request_user to the blood request creator if not provided
        if not self.request_user_id:
            self.request_user = self.request_accept.user
        
        # Check if this is an existing record being updated
        is_new = self.pk is None
        old_status = None
        
        if not is_new:
            try:
                old_instance = AcceptBloodRequest.objects.get(pk=self.pk)
                old_status = old_instance.donation_status
            except AcceptBloodRequest.DoesNotExist:
                pass
            
        # Get user details and check availability status
        try:
            donor_details = UserDetails.objects.get(user=self.user)
            
            # Check availability status only for new records
            if is_new and not donor_details.availability_status:
                raise DRFValidationError({
                    "error": "Your availability status is set to inactive. Please update your profile and set your availability status to active before accepting blood requests.",
                    "status": 400
                })
                
            # Update donor's last donation date if donation is completed
            if self.donation_status == self.DONATED:
                donor_details.last_donation_date = timezone.now().date()
                donor_details.save()
                
        except ObjectDoesNotExist:
            raise DRFValidationError({
                "error": "Please complete your user profile with all required details before accepting blood requests.",
                "status": 400
            })
            
        super().save(*args, **kwargs)
        
        # Update blood request fulfilled units when donation status changes to donated
        if old_status != self.donation_status:
            blood_request = self.request_user
            if self.donation_status == self.DONATED and (old_status != self.DONATED):
                blood_request.fulfilled_units += self.units
                blood_request.save()
            elif old_status == self.DONATED and self.donation_status != self.DONATED:
                # Reduce fulfilled units if donation is canceled after being marked as donated
                blood_request.fulfilled_units = max(0, blood_request.fulfilled_units - self.units)
                blood_request.save()

    def __str__(self):
        user_str = str(self.user.username) if self.user.username else str(self.user.email)
        request_str = str(self.request_user)
        return f"{user_str} accepted {request_str}"

    class Meta:
        unique_together = ['user', 'request_user']


