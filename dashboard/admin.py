from django.contrib import admin
from . import models
# Register your models here.
class DonationHistorytAdmin(admin.ModelAdmin):
    list_display = ['donor_first_name','donor_last_name','recipient_first_name','recipient_last_name','status','event']
    
    def donor_first_name(self,obj):
        return obj.donor.first_name
    def donor_last_name(self,obj):
        return obj.donor.last_name
    
    def recipient_first_name(self,obj):
        return obj.recipient.first_name
    def recipient_last_name(self,obj):
        return obj.recipient.last_name
    
    
admin.site.register(models.DonationHistory, DonationHistorytAdmin)