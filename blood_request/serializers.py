from rest_framework import serializers
from blood_request.models import BloodRequest, AcceptBloodRequest

class BloodRequestSerializer(serializers.ModelSerializer):
  """ Serializer for BloodRequest model """
  class Meta:
    model = BloodRequest
    fields = '__all__'
    extra_kwargs={'user':{'read_only':True}}

class AcceptBloodRequestSerializer(serializers.ModelSerializer):
  """ Serializer for AcceptBloodRequestSerializer model """
  class Meta:
    model = AcceptBloodRequest
    fields = ['user','request_user','request_accept','donation_status']
    extra_kwargs={'request_user':{'read_only':True},'user':{'read_only':True}, "request_accept":{'read_only':True}}
  




