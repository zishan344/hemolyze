from rest_framework import viewsets
from blood_request.models import BloodRequest, AcceptBloodRequest
from dashboard.serializers import DonarListSerializer
from django.contrib.auth import get_user_model
# Create your views here.
class DonarListViewSet(viewsets.ModelViewSet):
    """ Viewset for BloodRequest model """
    def get_queryset(self):
        user_ids = AcceptBloodRequest.objects.values_list('user', flat=True).distinct()
        return get_user_model().objects.filter(id__in=user_ids)
    serializer_class = DonarListSerializer
