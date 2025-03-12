from django.shortcuts import render
from .models import UserDetails
from .serializers import UserDetailsSerializer, UserSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class UserDetailsView(viewsets.ModelViewSet):
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'

    def get_queryset(self):
        return UserDetails.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "You do not have permission to delete this user details."},
            status=status.HTTP_403_FORBIDDEN
        )

    def perform_destroy(self, instance):
        instance.delete()

