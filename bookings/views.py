from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages 
from django.core.paginator import Paginator
from .forms import ProviderAvailabilityForm
from django.http import JsonResponse
from .models import ProviderAvailability
from datetime import date

from .models import *
from .forms import BookingForm
import datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

#################
#Provider Detail
#################


def create_booking(request, provider_id):
    provider = get_object_or_404(Provider, id=provider_id)
    service_choices = [(service.id, service.name) for service in provider.service_types.all()]
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile_id = request.session.get('user_profile_id')    
    clientx = Client.objects.get(user_profile_id=user_profile_id)
    available_times = []
    selected_date = None
    if request.method == 'POST':
        form = BookingForm(request.POST, service_choices=service_choices)
        
        if form.is_valid():
            selected_date = form.cleaned_data['booking_date']  # Get selected date
            # Fetch available times for the selected date
            
            booking = Booking(
                provider=provider,
                client_name=request.user,
                booking_date=form.cleaned_data['booking_date'],
                service_type=ServiceType.objects.get(id=form.cleaned_data['service_type']),
                start_time=form.cleaned_data['start_time'],
                end_time=form.cleaned_data['end_time'],
                about_work=form.cleaned_data['about_work'],
            )
            booking.save()
            # Send real-time notification via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'notifications',  # group_name
                {
                    'type': 'send_message',  # custom message handler in consumer
                    'message': f"New booking for {provider.name}!"
                }
            )
            # Redirect to the provider's page or a success page
            return redirect('client_bookings')
        else:
            print("error",form.errors)
    else:
        form = BookingForm(service_choices=service_choices)
    messages = Message.objects.filter(client=request.user)
    return render(request, 'client/home/create_booking.html', {'clientx':clientx,'form': form, 'provider': provider,'messages':messages,"user_profile":user_profile,'available_times': available_times,})
def notifications_view(request):
    messages = Message.objects.filter(client=request.user).order_by('-created_at')
    return render(request, 'client/home/notifications.html',{'messages': messages})
# def get_available_times(request, provider_id):
#     if request.method == 'GET':
#         selected_date = request.GET.get('date')
#         provider = get_object_or_404(Provider, id=provider_id)
        
#         available_slots = ProviderAvailability.objects.filter(
#             provider=provider, 
#             date=selected_date, 
#             is_available=True
#         ).values('start_time', 'end_time')
        
#         # Convert to list of dicts for JSON response
#         available_times = list(available_slots)
#         return JsonResponse({'available_times': available_times})


#Booking List View (For Clients)
def client_bookings(request):
    bookings = Booking.objects.filter(client_name=request.user)
    return render(request, 'client/home/bookingsview.html', {'bookings': bookings})



def provider_bookings(request):
    user_profile_id = request.session.get('user_profile_id')
    
    if not user_profile_id:
        # Handle case where user_profile_id is missing
        return redirect('loginprovider')  # or another appropriate redirect
    
    try:
        provider = Provider.objects.get(user_profile_id=user_profile_id)
    except Provider.DoesNotExist:
        # Handle the case where the Provider does not exist
        return redirect('loginprovider')  # or another appropriate redirect

    # Handle booking actions
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        action = request.POST.get('action')
        booking = get_object_or_404(Booking, id=booking_id)
        channel_layer = get_channel_layer()

        if action == 'accept':
            booking.status = 'Accepted'
            booking.save()

            message_text = f"Your booking for {booking.service_type.name} on {booking.booking_date} has been accepted!"
            #send_notification(booking.client_name.id, message_text)
            payment_url = f"/payment/{booking.id}"  # Assuming there's a payment view that handles payments
            Message.objects.create(
                client=booking.client_name,
                booking=booking,
                provider=provider,
                text=message_text,
                status='accepted',
                payment_url=payment_url
            )
             # Notify via WebSocket
            
            async_to_sync(channel_layer.group_send)(
                'notifications',
                {
                    'type': 'send_message',
                    'message': message_text
                }
            )

        elif action == 'reject':
            booking.status = 'Rejected'
            booking.save()
            message_text = f"Your booking for {booking.service_type.name} on {booking.booking_date} was rejected."
            Message.objects.create(
                client=booking.client_name,
                booking=booking,
                provider=provider,
                text=message_text,
                status='rejected'
            )
            # Notify via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'notifications',
                {
                    'type': 'send_message',
                    'message': message_text
                }
            )
        return redirect('providerdashboard')
    today= datetime.date.today()
    upcoming_bookings = Booking.objects.filter(
        provider=provider,
        status__in=['Pending'],  # Only show pending bookings
        booking_date__gte=datetime.date.today()  # Only show future bookings
    )

    # Fetch bookings for the provider
    bookings = Booking.objects.filter(provider=provider)
    messages = Message.objects.filter(client=provider.user_profile.user).order_by('-created_at')
    return render(request, 'provider/dashboard/provider_bookings.html', {
        'provider': provider,
        'bookings': bookings,
        'upcoming_bookings':upcoming_bookings,
        'messages':messages,
    })


# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer

# def send_notification(user_id, message):
#     channel_layer = get_channel_layer()
#     group_name = f'user_{user_id}'

#     async_to_sync(channel_layer.group_send)(
#         group_name,
#         {
#             'type': 'send_notification',
#             'message': message
#         }
#     )
# views.py
from django.shortcuts import render
from .models import Message

def notification_view(request):
    user = request.user  # Assuming the user is logged in
    messages = Message.objects.filter(client=user).order_by('-created_at')  # Retrieve messages for the logged-in client

    return render(request, 'client/home/notifications.html', {
        'messages': messages,
    })
