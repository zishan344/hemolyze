# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import (
#     DonarListViewSet, 
#     DonationHistoryViewSet,
#     DonatedFundViewSet,
#     initiate_payment,
#     payment_success, 
#     payment_cancel, 
#     payment_fail
# )

# app_name = 'dashboard'

# router = DefaultRouter()
# router.register(r'donors', DonarListViewSet, basename='donar_list')
# router.register(r'donation-history', DonationHistoryViewSet, basename='donation_history')
# router.register(r'donations', DonatedFundViewSet, basename='donations')

# urlpatterns = [
#     path('', include(router.urls)),
#     path('initiate-payment/', initiate_payment, name='initiate_payment'),
#     path('payment/success/', payment_success, name='payment_success'),
#     path('payment/cancel/', payment_cancel, name='payment_cancel'),
#     path('payment/fail/', payment_fail, name='payment_fail'),
# ]