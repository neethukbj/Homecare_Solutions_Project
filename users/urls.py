# from django.urls import path
from . import views
# from .auth_views import urlpatterns as auth_urls

# urlpatterns = [
#     path('signup/', views.signupprovider, name='providersignup'),
#     path('login/', views.loginprovider, name='loginprovider'),
#     path('logout/', views.logoutprovider, name='logoutprovider'),
#     path('profile/', views.providerprofile, name='providerprofile'),
# ] + auth_urls



from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #Provider views
    path('signupprovider/',views.signupprovider,name="signupprovider"),
    path('providersignup/', views.providersignup, name="providersignup"),
    path('loginprovider/',views.loginprovider,name="loginprovider"),
    path('logoutprovider/',views.logoutprovider,name="logoutprovider"),
    #path('providerdashboard/<int:user_profile_id>/', views.providerdashboard, name='providerdashboard'),
    path('providerdashboard/',views.providerdashboard,name="providerdashboard"),
    path('providerprofile/',views.providerprofile,name="providerprofile"),


    # ####Client views
    path('signupclient/',views.signupclient,name="signupclient"),
    path('clientsignup/',views.clientsignup,name="clientsignup"),
    path('logoutclient/',views.logoutclient,name="logoutclient"),
    path('loginclient/',views.loginclient,name="loginclient"),


    # #Provider listing and Payments

    path('allproviders/',views.allproviders,name="allproviders"),
    # path('payment/<int:booking_id>/', views.payment_view, name='payment_view'),
    # path('create-razorpay-order/<int:booking_id>/', views.create_razorpay_order, name='create_razorpay_order'),
    # #path('create_razorpay_order/<int:booking_id>/', views.payment_view, name='create_razorpay_order'),
    
]
