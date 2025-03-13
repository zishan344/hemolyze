from django.contrib import admin
from blood_request.models import BloodRequest, AcceptBloodRequest,ReceivedBlood
# Register your models here.
admin.site.register(BloodRequest)
admin.site.register(AcceptBloodRequest)
admin.site.register(ReceivedBlood)
