from django.shortcuts import render


# Create your views here.
def trackerapp(request):
    return render(request, 'Trackerapp.html')

def login_view(request):
    return render(request, 'login.html')  

def calendar_view(request):
    return render(request, 'calendar.html')  

def fasting_view(request):
    return render(request, 'fasting.html')  
