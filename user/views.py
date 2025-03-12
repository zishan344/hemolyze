from django.shortcuts import render
from .models import UserDetails
from .serializers import UserDetailsSerializer
from rest_framework import viewsets
# Create your views here.

class UserDetailsView(viewsets.ModelViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer

