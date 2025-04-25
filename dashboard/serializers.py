from rest_framework import serializers
from django.contrib.auth import get_user_model
from blood_request.models import AcceptBloodRequest, BloodRequest


class DonarListSerializer(serializers.ModelSerializer):
    blood_group = serializers.CharField(source='userdetails.blood_group')
    last_donation_date = serializers.DateField(source='userdetails.last_donation_date')
    name = serializers.CharField(source='userdetails.name')
    address = serializers.CharField(source='userdetails.address')
    availability_status = serializers.BooleanField(source='userdetails.availability_status')
    userDetailId = serializers.IntegerField(source='userdetails.id')
    
    class Meta:
        model = get_user_model()
        fields = ['id','userDetailId', 'name', 'address', 'availability_status', 'blood_group', 'last_donation_date']

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