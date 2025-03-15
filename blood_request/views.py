from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,BasePermission
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from blood_request.models import BloodRequest, AcceptBloodRequest
from blood_request.serializers import BloodRequestSerializer, AcceptBloodRequestSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.

class BloodRequestViewSet(viewsets.ModelViewSet):
    """ Viewset for BloodRequest model """
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['blood_group']
    def perform_create(self,request):
        request.save(user=self.request.user)

class AcceptBloodRequestViewSet(viewsets.ModelViewSet):
    """ Viewset for AcceptRequest model """
    queryset = AcceptBloodRequest.objects.all()
    serializer_class = AcceptBloodRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_accept = serializer.validated_data.get('request_accept')
        request_user = request_accept.user
        accepted_user = self.request.user
        print("request_user:- ",request_user, "accepted_user: ",accepted_user)
        # print(request_accept.user , self.request.user)
        # Check if user is trying to accept their own request
        if request_accept.user == self.request.user:
            raise ValidationError({
                "error": "You cannot accept your own blood request",
                "status": 400
            })
            
        serializer.save(user=accepted_user)