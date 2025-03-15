from django.shortcuts import get_object_or_404
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

    def get_queryset(self):
        blood_request_id = self.kwargs.get('blood_request_pk')
        print("blood request", blood_request_id)
        return AcceptBloodRequest.objects.filter(request_accept=blood_request_id)

    def perform_create(self, serializer):
        accepted_user = self.request.user
        blood_request_id = self.kwargs.get('blood_request_pk')
        
        blood_request_post = get_object_or_404(BloodRequest, pk=blood_request_id)
        # print("accepted_user \n",accepted_user, "request_user",blood_request_post.user)
        if accepted_user == blood_request_post.user:
            raise ValidationError({
                "error": "You cannot accept your own blood request",
                "status": 400
            })
        serializer.save(user=accepted_user, request_accept=blood_request_post)