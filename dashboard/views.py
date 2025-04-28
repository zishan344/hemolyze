from sslcommerz_lib import SSLCOMMERZ
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q
from blood_request.models import BloodRequest, AcceptBloodRequest
from dashboard.serializers import DonarListSerializer
from user.models import UserDetails
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
    post_body['tran_id'] = f"txn_{user.id,str(uuid.uuid4())} "
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
    """  order_id = request.data.get('tran_id').split('_')[1]
    order = Order.objects.get(id=order_id)
    order.status = 'Ready To Ship'
    order.save() """
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/payment-success")
    
@api_view(['POST'])
def payment_cancel(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/")

@api_view(['POST'])
def payment_fail(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/orders/")

