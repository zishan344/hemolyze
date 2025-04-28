from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from user.models import UserDetails, CustomUser


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ['email', 'username', 'password']

class UserSerializer(BaseUserSerializer):
    role = serializers.SerializerMethodField()
    
    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ['id', 'email', 'username', 'role']
        
    def get_role(self, obj):
        # Get the first group name as the role (assuming each user has only one group)
        if obj.groups.exists():
            return obj.groups.first().name
        return None

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__' 
        extra_kwargs = {
            'last_donation_date': {'read_only': True},
            'user':{'read_only':True}
        }
