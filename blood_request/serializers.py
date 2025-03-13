from rest_framework import serializers
from blood_request.models import BloodRequest, AcceptBloodRequest

class BloodRequestSerializer(serializers.ModelSerializer):
  """ Serializer for BloodRequest model """
  class Meta:
    model = BloodRequest
    fields = '__all__'

class AcceptBloodRequestSerializer(serializers.ModelSerializer):
  """ Serializer for AcceptBloodRequestSerializer model """
  class Meta:
    model = AcceptBloodRequest
    fields = ['user','request_accept','request_user','donation_status']
    extra_kwargs={'request_user':{'read_only':True}}
  




