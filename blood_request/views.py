from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from blood_request.models import BloodRequest, AcceptBloodRequest
from blood_request.serializers import BloodRequestSerializer, AcceptBloodRequestSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.

class BloodRequestViewSet(viewsets.ModelViewSet):
    """ Viewset for BloodRequest model """
    queryset = BloodRequest.objects.all().order_by('-created_at')
    serializer_class = BloodRequestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['blood_group', 'status', 'urgency_level']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'], url_path='my-requests')
    def my_requests(self, request):
        """Get all blood requests created by the current user"""
        # Check if this is a schema generation request from Swagger
        if getattr(self, 'swagger_fake_view', False):
            return Response([])
            
        queryset = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='donors')
    def donors(self, request, pk=None):
        """Get all donors for a blood request"""
        blood_request = self.get_object()
        donations = AcceptBloodRequest.objects.filter(request_user=blood_request)
        serializer = AcceptBloodRequestSerializer(donations, many=True)
        return Response(serializer.data)


class AcceptBloodRequestViewSet(viewsets.ModelViewSet):
    """ Viewset for AcceptRequest model """
    queryset = AcceptBloodRequest.objects.all()
    serializer_class = AcceptBloodRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['donation_status']
    lookup_field = 'request_user_id'

    def get_queryset(self):
        # Check if this is a schema generation request from Swagger
        if getattr(self, 'swagger_fake_view', False):
            # Return empty queryset for Swagger schema generation
            return AcceptBloodRequest.objects.none()
        
        # Check if the current action is my_donations - this needs special handling
        if self.action == 'my_donations':
            # For my_donations, ignore blood_request_pk and filter by user only
            return AcceptBloodRequest.objects.filter(user=self.request.user)
        
        # For regular endpoints, filter by blood_request_pk if provided
        blood_request_id = self.kwargs.get('blood_request_pk')
        if blood_request_id:
            return AcceptBloodRequest.objects.filter(request_user=blood_request_id)
        return AcceptBloodRequest.objects.all()

    def perform_create(self, serializer):
        accepted_user = self.request.user
        blood_request_id = self.kwargs.get('blood_request_pk')
        
        blood_request_post = get_object_or_404(BloodRequest, pk=blood_request_id)
        
        if accepted_user == blood_request_post.user:
            raise ValidationError({
                "error": "You cannot accept your own blood request",
                "status": 400
            })
            
        # Check if user has already accepted this request
        if AcceptBloodRequest.objects.filter(user=accepted_user, request_user=blood_request_post).exists():
            raise ValidationError({
                "error": "You have already accepted this blood request",
                "status": 400
            })
        
        # When donor accepts, explicitly set donation_status to pending
        accept_request = serializer.save(
            user=accepted_user, 
            request_user=blood_request_post, 
            request_accept=blood_request_post.user,
            donation_status=AcceptBloodRequest.PENDING
        )
        
        # Update the BloodRequest status to "accepted"
        blood_request_post.status = "accepted"
        blood_request_post.save()

    @action(detail=False, methods=['get'], url_path='my-donations')
    def my_donations(self, request, blood_request_pk=None):
        """Get all donations made by the current user"""
        # Check if this is a schema generation request from Swagger
        if getattr(self, 'swagger_fake_view', False):
            return Response([])

        # Use the queryset from get_queryset which will filter by user
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Only request owner can delete the request
        if instance.request_user.user != request.user and instance.user != request.user:
            return Response(
                {"error": "You don't have permission to delete this donation request"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        return super().destroy(request, *args, **kwargs)
        
    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None, blood_request_pk=None, request_user_id=None):
        """Update the donation status based on frontend action indicators"""
        instance = self.get_object()
        
        # Check who is making the status update
        is_donor = instance.user == request.user
        is_requester = instance.request_user.user == request.user
        
        if not (is_donor or is_requester):
            return Response(
                {"error": "You don't have permission to update this donation status"}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        donation_status = request.data.get('donation_status')
        
        # Handle frontend action indicators
        if donation_status == AcceptBloodRequest.CANCELED_BY_USER:
            if not is_requester:
                return Response(
                    {"error": "Only the blood requester can cancel a donation"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            # Delete the accept request when canceled by requester
            blood_request = instance.request_user
            blood_request.status = 'pending'
            blood_request.save()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        if donation_status == AcceptBloodRequest.CANCELED_BY_DONOR:
            if not is_donor:
                return Response(
                    {"error": "Only the donor can cancel their own donation"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            # Set status to canceled when donor cancels
            instance.donation_status = AcceptBloodRequest.CANCELED
            blood_request = instance.request_user
            blood_request.status = 'pending'
            blood_request.save()
            instance.save()
            return Response(self.get_serializer(instance).data)
                
        if donation_status == AcceptBloodRequest.ACCEPTED_BY_USER:
            if not is_requester:
                return Response(
                    {"error": "Only the blood requester can accept a donation"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            # Set status to donated when requester accepts
            instance.donation_status = AcceptBloodRequest.DONATED
            # Update the blood request status to completed
            blood_request = instance.request_user
            blood_request.status = 'completed'
            blood_request.save()
            instance.save()
            return Response(self.get_serializer(instance).data)
        
        # For direct status updates (if needed, though frontend should use action indicators)
        if donation_status in dict(AcceptBloodRequest.BLOOD_STATUS):
            instance.donation_status = donation_status
            instance.save()
            return Response(self.get_serializer(instance).data)
            
        return Response(
            {"error": f"Invalid status. Choose from {dict(AcceptBloodRequest.BLOOD_STATUS).keys()} or action indicators"}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class MyDonationsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """ViewSet for retrieving a user's donations"""
    serializer_class = AcceptBloodRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['donation_status']
    lookup_field = 'request_user_id'  # Use request_accept_id as the lookup field
    
    def get_queryset(self):
        # Check if this is a schema generation request from Swagger
        if getattr(self, 'swagger_fake_view', False):
            # Return empty queryset for Swagger schema generation
            return AcceptBloodRequest.objects.none()
            
        # Return only donations made by the current user
        return AcceptBloodRequest.objects.filter(user=self.request.user)
