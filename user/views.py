from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import UserDetails
from .serializers import UserDetailsSerializer

User = get_user_model()
class UserDetailsViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage user details.
    """
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        """
        Get the list of user details.

        - Superusers can view all user details.
        - Regular users can only view their own details.

        Returns:
            QuerySet: A filtered queryset of `UserDetails` objects.
        """
        if self.request.user.is_superuser:
            return UserDetails.objects.all()
        return UserDetails.objects.filter(user=self.request.user)
    
    def get_object(self):
        """
        Retrieve a specific user detail object.

        - Superusers can access any user detail.
        - Regular users can only access their own details.

        Returns:
            UserDetails: The requested user detail object.
        """
        user_id = self.kwargs.get('pk')
        queryset = UserDetails.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)
        obj = get_object_or_404(queryset, user_id=user_id)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def perform_create(self, serializer):
        
        """ Create or update user details for the authenticated user.

        - If user details already exist, they are updated.
        - Otherwise, new user details are created.
        """
        try:
            existing_details = UserDetails.objects.get(user=self.request.user)
            serializer.instance = existing_details
            serializer.save()
        except UserDetails.DoesNotExist:
            serializer.save(user=self.request.user)
