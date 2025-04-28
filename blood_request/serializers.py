from rest_framework import serializers
from blood_request.models import BloodRequest, AcceptBloodRequest

class BloodRequestSerializer(serializers.ModelSerializer):
  """ Serializer for BloodRequest model """
  progress_percentage = serializers.SerializerMethodField()
  
  def get_progress_percentage(self, obj):
    if obj.required_units <= 0:
      return 0
    return min(100, int((obj.fulfilled_units / obj.required_units) * 100))
    
  class Meta:
    model = BloodRequest
    fields = '__all__'
    extra_kwargs={'user':{'read_only':True}, 'fulfilled_units':{'read_only':True}}

class AcceptBloodRequestSerializer(serializers.ModelSerializer):
  """ Serializer for AcceptBloodRequestSerializer model """
  donor_name = serializers.SerializerMethodField()
  
  def get_donor_name(self, obj):
    # Use the name from UserDetails if available, otherwise fall back to username or email
    try:
      if hasattr(obj.user, 'userdetails') and obj.user.userdetails.name:
        return obj.user.userdetails.name
    except:
      pass
    return obj.user.username or obj.user.email
    
  class Meta:
    model = AcceptBloodRequest
    fields = ['id', 'user', 'request_user', 'request_accept', 'donation_status', 'units', 'date', 'donor_name']
    extra_kwargs = {
      'request_user': {'read_only': True},
      'user': {'read_only': True}, 
      'request_accept': {'read_only': True},
      'date': {'read_only': True}
    }





