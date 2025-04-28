from rest_framework import serializers
from django.contrib.auth import get_user_model
from blood_request.models import AcceptBloodRequest, BloodRequest
from user.models import UserDetails
from .models import DonatedFund


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
        fields = ['id', 'blood_group', 'hospital_name','status', 'date']


class DonationHistorySerializer(serializers.ModelSerializer):
    blood_request = BloodRequestDetailSerializer(source='request_user')
    recipient_name = serializers.SerializerMethodField()
    donor_name = serializers.SerializerMethodField()
    
    def get_recipient_name(self, obj):
        # Get recipient name safely
        if hasattr(obj.request_accept, 'username'):
            return obj.request_accept.username
        return obj.request_accept.email if obj.request_accept else "Unknown"
    
    def get_donor_name(self, obj):
        # Get donor name safely
        if hasattr(obj.user, 'userdetails') and hasattr(obj.user.userdetails, 'name'):
            return obj.user.userdetails.name
        return obj.user.username or obj.user.email
    
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


class DonatedFundSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    
    def get_username(self, obj):
        return obj.user.username if hasattr(obj.user, 'username') else obj.user.email
    
    class Meta:
        model = DonatedFund
        fields = ['id', 'username', 'amount', 'transaction_id', 'created_date']
        read_only_fields = ['id', 'user', 'created_date']