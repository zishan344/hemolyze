
class UserCreateSerializer(serializers.ModelSerializer):
    """
    UserSerializer is used to serialize and deserialize User model instances.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserDetailsSerializer(serializers.ModelSerializer):
    """ this is user detail serializer """
    class Meta:
        model = UserDetails
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model including related UserDetails."""
    userdetails = UserDetailsSerializer(required=False, allow_null=True)
    permission_classes = [permissions.IsAuthenticated]

    class Meta:
        """Meta class to specify model and fields for serialization."""
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'userdetails']
      
    def destroy(self, instance):
        """Delete user if user has permission. UserDetails will be deleted automatically via CASCADE."""
        if self.context['request'].user.has_permission('user.delete_user'):
            try:
                instance.delete()
                return True
            except Exception as e:
                raise serializers.ValidationError(f"Error deleting user: {str(e)}")
        raise serializers.ValidationError("You don't have permission to delete this user.")
    def to_representation(self, instance):
        """Custom representation to handle null userdetails."""
        ret = super().to_representation(instance)
        try:
            ret['userdetails'] = UserDetailsSerializer(instance.userdetails).data
        except UserDetails.DoesNotExist:
            ret['userdetails'] = None
        return ret

    def update(self, instance, validated_data):
        """Update the User instance and its related UserDetails."""
        userdetails_data = validated_data.pop('userdetails', None)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        if userdetails_data:
            userdetails, created = UserDetails.objects.get_or_create(
                user=instance,
                defaults={
                    'address': userdetails_data.get('address', ''),
                    'age': userdetails_data.get('age'),
                    'phone_number': userdetails_data.get('phone_number', ''),
                    'last_donation_date': userdetails_data.get('last_donation_date'),
                    'availability_status': userdetails_data.get('availability_status', False)
                }
            )
            if not created:
                for attr, value in userdetails_data.items():
                    setattr(userdetails, attr, value)
                userdetails.save()

        return instance

class CustomUserDeleteSerializer(serializers.Serializer):
    """
    Custom serializer for user deletion that doesn't require current_password
    """
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.delete()

        