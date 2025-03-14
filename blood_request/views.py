from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from blood_request.models import BloodRequest, AcceptBloodRequest
from blood_request.serializers import BloodRequestSerializer, AcceptBloodRequestSerializer
# Create your views here.

class BloodRequestViewSet(viewsets.ModelViewSet):
    """ Viewset for BloodRequest model """
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['blood_group']

class AcceptBloodRequestViewSet(viewsets.ModelViewSet):
    """ Viewset for AcceptRequest model """
    queryset = AcceptBloodRequest.objects.all()
    serializer_class = AcceptBloodRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_accept = serializer.validated_data.get('request_accept')
        print(request_accept.user , self.request.user)
        # Check if user is trying to accept their own request
        if request_accept.user == self.request.user:
            raise ValidationError({
                "error": "You cannot accept your own blood request",
                "status": 400
            })
            
        serializer.save()