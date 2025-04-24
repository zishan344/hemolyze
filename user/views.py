from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import UserDetails
from .serializers import UserDetailsSerializer

User = get_user_model()

class AllUserDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for administrators to view all user details.
    This view is restricted to admin users only.
    """
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAdminUser]

class UserDetailsViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage individual user details.
    Users can only view and modify their own details.
    """
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        """
        Get only the current user's details
        """
        return UserDetails.objects.filter(user=self.request.user)
    
    def get_object(self):
        """
        Retrieve the user's own detail object
        """
        return get_object_or_404(UserDetails, user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Create or update user details for the authenticated user.
        """
        try:
            existing_details = UserDetails.objects.get(user=self.request.user)
            serializer.instance = existing_details
            serializer.save()
        except UserDetails.DoesNotExist:
            serializer.save(user=self.request.user)
