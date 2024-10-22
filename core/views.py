from django.shortcuts import render

# Create your views here
#################
# Common Views
#################


def home(request):
    return render(request,'core/index.html')

def entry(request):
    return render(request,'core/entry.html')

def aboutview(request):
    return render(request,"core/about.html")

def contactview(request):
    return render(request,"core/contact.html")

def serviceview(request):
    return render(request,"core/service.html")