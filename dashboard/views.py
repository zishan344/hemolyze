from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q
from blood_request.models import BloodRequest, AcceptBloodRequest
from dashboard.serializers import DonarListSerializer
from .serializers import DonationHistorySerializer
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
class DonationHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DonationHistorySerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return AcceptBloodRequest.objects.filter(
            Q(user=self.request.user) | 
            Q(request_user=self.request.user) 
        ).select_related('user', 'request_user', 'request_accept').order_by('-date')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Separate donations and received records
        donations = self.serializer_class(
            queryset.filter(user=request.user), 
            many=True
        ).data
        
        received = self.serializer_class(
            queryset.filter(request_user=request.user), 
            many=True
        ).data

        return Response({
            'donations': donations,
            'received': received
        })



class DonarListViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for listing available donors with their details"""
    serializer_class = DonarListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['userdetails__blood_group']

    def get_queryset(self):
        return get_user_model().objects.filter(
            userdetails__availability_status=True
        ).select_related('userdetails').order_by('userdetails__last_donation_date')
