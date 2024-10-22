from django.contrib import admin
from django.urls import path
from . import views


urlpatterns =[

    #Home and common views
    path("",views.home,name="home"),
    path('entry/',views.entry,name="entry"),
    path("about/",views.aboutview,name="about"),
    path("contact/",views.contactview,name="contact"),
    path("serviceview/",views.serviceview,name="service"), 

]