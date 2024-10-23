from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Booking)
class BookingModelAdmin(admin.ModelAdmin):
	list_display=['client_name','provider','booking_date','status','payment_status']
	list_filter = ('status', 'provider', 'service_type')
admin.site.register(Message)

