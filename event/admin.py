from django.contrib import admin
from . import models
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ['creator_name', 'title', 'blood_group','created_at']
    def creator_name(self,obj):
        return obj.creator.first_name
    
admin.site.register(models.Event, EventAdmin)