from rest_framework import serializers
from django.contrib.auth import get_user_model
from blood_request.models import AcceptBloodRequest, BloodRequest
from user.models import UserDetails


class DonarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = [
            'id','user', 'name', 'address', 'phone_number', 'age', 
            'availability_status', 'blood_group', 'last_donation_date'
        ]

class BloodRequestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodRequest
        fields = ['id', 'blood_group', 'city', 'date']

class DonationHistorySerializer(serializers.ModelSerializer):
    blood_request = BloodRequestDetailSerializer(source='request_accept')
    recipient_name = serializers.CharField(source='request_user.username')
    donor_name = serializers.CharField(source='user.username')
    
    class Meta:
        model = AcceptBloodRequest
        fields = [
            'id', 
            'donor_name',
            'recipient_name', 
            'donation_status',
            'date',
            'blood_request'
        ]