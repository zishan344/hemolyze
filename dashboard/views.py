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
    """
    ViewSet for retrieving the donation and received history of the authenticated user.
    """
    serializer_class = DonationHistorySerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        """
        Retrieve the queryset of accepted blood requests where the authenticated user
        is either the donor or the recipient.

        Returns:
            QuerySet: Filtered and ordered queryset of `AcceptBloodRequest` objects.
        """
        return AcceptBloodRequest.objects.filter(
            Q(user=self.request.user) | 
            Q(request_user=self.request.user) 
        ).select_related('user', 'request_user', 'request_accept').order_by('-date')
    
    def list(self, request, *args, **kwargs):
        """
        List the donation and received history for the authenticated user.

        Separates the records into two categories:
        - Donations: Blood requests where the user is the donor.
        - Received: Blood requests where the user is the recipient.

        Returns:
            Response: A JSON response containing two lists: `donations` and `received`.
        """
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
        """
        Retrieve the queryset of users who are available for donation.

        Filters users based on their availability status and orders them by their
        last donation date.

        Add also custome filter query can filter with blood gruoup.
        
        Returns:
            QuerySet: Filtered and ordered queryset of user objects.
        """
        return get_user_model().objects.filter(
            userdetails__availability_status=True
        ).select_related('userdetails').order_by('userdetails__last_donation_date')
