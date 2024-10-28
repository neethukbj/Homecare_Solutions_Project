from django.contrib import admin
from django.urls import path
from . import views

urlpatterns =[

    # Provider details and booking views
    path('create_booking/<int:provider_id>/', views.create_booking, name='create_booking'),
    path('bookings/', views.client_bookings, name='client_bookings'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('providerbookings/', views.provider_bookings, name='provider_bookings'),

    # path('booking/success/', views.booking_success_view, name='booking_success'),
    
    # # Booking and payment views
    # path('works/', views.works, name='works'),
    # path('payments/', views.payments, name='payments'),
    # path('complete-work/<int:booking_id>/', views.complete_work, name='complete_work'),
    # path('confirm-work/<int:booking_id>/',views.confirm_work, name='confirm_work'),
    
    # # Notification views
    # path('notifications/', views.notifications, name='notifications'),
    # path('provider_notifications/', views.provider_notifications, name='provider_notifications'),
    # path('set-availability/', views.set_availability, name='set_provider_availability'),
    # path('fetch-availability/', views.fetch_availability, name='fetch_availability'),
    # path('provider/<int:provider_id>/available-times/', views.get_available_times, name='get_available_times'),

]