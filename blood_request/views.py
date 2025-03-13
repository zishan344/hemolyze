from django.shortcuts import render
from rest_framework import viewsets
from blood_request.models import BloodRequest, AcceptBloodRequest
from blood_request.serializers import BloodRequestSerializer, AcceptBloodRequestSerializer
# Create your views here.

class BloodRequestViewSet(viewsets.ModelViewSet):
    """ Viewset for BloodRequest model """
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer

class AcceptBloodRequestViewSet(viewsets.ModelViewSet):
    """ Viewset for AcceptRequest model """
    queryset = AcceptBloodRequest.objects.all()
    serializer_class = AcceptBloodRequestSerializer