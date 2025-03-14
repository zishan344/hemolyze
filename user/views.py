from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import UserDetails
from .serializers import UserDetailsSerializer

User = get_user_model()
class UserDetailsViewSet(viewsets.ModelViewSet):
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]
    # lookup_field = 'user_id'
    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserDetails.objects.all()
        return UserDetails.objects.filter(user=self.request.user)
    
    def get_object(self):
        user_id = self.kwargs.get('pk')
        queryset = UserDetails.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)
        obj = get_object_or_404(queryset, user_id=user_id)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def perform_create(self, serializer):
        try:
            existing_details = UserDetails.objects.get(user=self.request.user)
            serializer.instance = existing_details
            serializer.save()
        except UserDetails.DoesNotExist:
            serializer.save(user=self.request.user)
