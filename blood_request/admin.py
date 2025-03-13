from django.contrib import admin
from blood_request.models import BloodRequest, AcceptBloodRequest
# Register your models here.
admin.site.register(BloodRequest)
admin.site.register(AcceptBloodRequest)