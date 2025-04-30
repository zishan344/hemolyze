from sslcommerz_lib import SSLCOMMERZ
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Q
from blood_request.models import BloodRequest, AcceptBloodRequest
from dashboard.serializers import DonarListSerializer, DonatedFundSerializer
from user.models import UserDetails
from .models import DonatedFund
from .serializers import DonationHistorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect
import uuid
from django.conf import settings as main_settings

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
        # Check if this is a schema generation request
        if getattr(self, 'swagger_fake_view', False):
            return AcceptBloodRequest.objects.none()

        return AcceptBloodRequest.objects.filter(
            Q(user=self.request.user) | 
            Q(request_accept=self.request.user) 
        ).select_related('user', 'request_user', 'request_accept').order_by('-date')

    def list(self, request, *args, **kwargs):
        """
        List the donation and received history for the authenticated user.

        Separates the records into two categories:
        - Donations: Blood requests where the user is the donor.
        - Received: Blood requests where the user is the recipient, excluding canceled donations.

        Returns:
            Response: A JSON response containing two lists: `donations` and `received`.
        """
        queryset = self.get_queryset()
        
        # Separate donations and received records
        donations = self.serializer_class(
            queryset.filter(user=request.user), 
            many=True
        ).data
        
        # Filter received records to exclude those with 'canceled' donation status
        received = self.serializer_class(
            queryset.filter(
                request_accept=request.user
            ).exclude(
                donation_status='canceled'
            ), 
            many=True
        ).data

        return Response({
            'donations': donations,
            'received': received
        })

class AllBloodDonationHistory(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving the donation and received history of the authenticated user.
    """
    serializer_class = DonationHistorySerializer
    permission_classes=[IsAdminUser]
    def get_queryset(self):
        """
        Retrieve the queryset of accepted blood requests where the authenticated user
        is either the donor or the recipient.

        Returns:
            QuerySet: Filtered and ordered queryset of `AcceptBloodRequest` objects.
        """
        # Check if this is a schema generation request
        if getattr(self, 'swagger_fake_view', False):
            return AcceptBloodRequest.objects.none()

        return AcceptBloodRequest.objects.select_related('user', 'request_user', 'request_accept').order_by('-date')

    def list(self, request, *args, **kwargs):
        """
        List the donation and received history for the admin user.
        Separates the records into two categories:
        - Donations: Blood requests where the user is the donor.
        

        Returns:
            Response: A JSON response containing 1 list: `donations`.
        """
        queryset = self.get_queryset()
        
        # Separate donations and received records
        donations = self.serializer_class(
            queryset, 
            many=True
        ).data
        return Response(donations)

class DonarListViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for listing available donors with their details"""
    serializer_class = DonarListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['blood_group']

    def get_queryset(self):
        """
        Retrieve the queryset of user details who are available for donation.

        Filters user details based on their availability status and orders them by their
        last donation date.

        Returns:
            QuerySet: Filtered and ordered queryset of UserDetails objects.
        """
        return UserDetails.objects.filter(
            availability_status=True
        ).order_by('last_donation_date')


class StatisticsViewSet(viewsets.ViewSet):
    """
    ViewSet for retrieving system-wide statistics:
    - Total Users
    - Total Blood Donations
    - Total Donation Pending Requests
    - Total Fund Amount
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request):
        """
        Returns a summary of key statistics for the admin dashboard
        """
        # Get the User model
        User = get_user_model()
        
        # Calculate statistics
        total_users = User.objects.count()
        total_blood_donations = AcceptBloodRequest.objects.filter(
            donation_status='donated'
        ).count()
        total_pending_requests = BloodRequest.objects.filter(
            status='pending'
        ).count()
        
        # Calculate total fund by summing all donation amounts
        from django.db.models import Sum
        total_fund = DonatedFund.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Format as decimal with 2 decimal places
        total_fund = round(float(total_fund), 2)
        
        return Response({
            'total_users': total_users,
            'total_blood_donations': total_blood_donations,
            'total_pending_requests': total_pending_requests,
            'total_fund': total_fund,
        })


# patch the user role
@api_view(['PATCH'])
def patch_user_role(request, user_id):
    """
    Update the role of a user to 'admin' or 'user' based on the request data.
    """
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        role = request.data.get('role')
        if role in ['admin', 'user']:
            # Remove user from all existing role groups
            user.groups.clear()
            
            # Get or create the appropriate group
            group, _ = Group.objects.get_or_create(name=role)
            
            # Add user to the new role group
            user.groups.add(group)
            
            # If role is admin, make the user staff as well
            if role == 'admin':
                user.is_staff = True
            else:
                user.is_staff = False
            user.save()
            
            return Response({"message": "User role updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def initiate_payment(request):
    user = request.user
    amount = request.data.get('amount')
    settings = { 'store_id': 'phima68034d9834517', 'store_pass': 'phima68034d9834517@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['payment_type_name'] = "donation"
    post_body['tran_id'] = f"txn_{user.id}_{str(uuid.uuid4())} "
    post_body['success_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/success/"
    post_body['fail_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/fail/"
    post_body['cancel_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/cancel/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = user.username
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = "01700000000"
    post_body['cus_add1'] = "customer address"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "donated"
    post_body['product_category'] = "donate"
    post_body['product_profile'] = "general"
    
    response = sslcz.createSession(post_body)
    if response.get("status") == 'SUCCESS':
        return Response({
            "payment_url":response['GatewayPageURL'],

        })
    return Response({"error":"Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def payment_success(request):
    """
    Handle successful payment and create donation record
    """
    transaction_id = request.data.get('tran_id')
    amount = request.data.get('amount')
    # email = request.data.get('cus_email')
    userid = int(transaction_id.split("_")[1])


    
    # Find the user by email
    User = get_user_model()
    try:
        user = User.objects.get(id=userid)
        # Create donation record
        DonatedFund.objects.create(
            user=user,
            amount=amount,
            transaction_id=transaction_id
        )
    except User.DoesNotExist:
        # Log error - user not found
        pass
        
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/payment-success")
    

@api_view(['POST'])
def payment_cancel(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/")

@api_view(['POST'])
def payment_fail(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/orders/")

class DonatedFundViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling donation funds.
    - Regular users can only view their own donations
    - Admin users can view all donations
    """
    serializer_class = DonatedFundSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Returns donations filtered by user permissions:
        - Admin users see all donations
        - Regular users see only their own donations
        """
        if getattr(self, 'swagger_fake_view', False):
            return DonatedFund.objects.none()
            
        user = self.request.user
        if user.is_staff:  # Admin can see all donations
            return DonatedFund.objects.all()
        # Regular users can only see their own donations
        return DonatedFund.objects.filter(user=user)
    
    def perform_create(self, serializer):
        """Automatically set the user to the current authenticated user"""
        serializer.save(user=self.request.user)

