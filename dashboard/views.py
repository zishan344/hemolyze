from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q
from blood_request.models import BloodRequest, AcceptBloodRequest
from dashboard.serializers import DonarListSerializer
from .serializers import DonationHistorySerializer
# Create your views here.


class DonationHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DonationHistorySerializer

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



class DonarListViewSet(viewsets.ModelViewSet):
    """ViewSet for listing donors"""
    serializer_class = DonarListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            # Get distinct users who have accepted blood requests
            user_ids = AcceptBloodRequest.objects.values_list('user', flat=True).distinct()
            return get_user_model().objects.filter(id__in(user_ids))
        return get_user_model().objects.none()

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        return super().list(request, *args, **kwargs)
