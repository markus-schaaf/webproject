from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

# Create your views here.
def trackerapp(request):
    return render(request, 'Trackerapp.html')

def login_view(request):
    return render(request, 'login.html')  

def calendar_view(request):
    return render(request, 'calendar.html')  

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatisch einloggen nach der Registrierung
            return redirect('home')  # Weiterleitung nach dem erfolgreichen Login
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # Speichert den neuen Benutzer
            return redirect('login')  # Weiterleitung nach erfolgreicher Registrierung
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Nutzer nach der Registrierung einloggen
            return redirect("home")  # Weiterleitung nach erfolgreicher Registrierung /Kommentar Markus: Muss hier die Homepage noch verlinkt werden?
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})
  
def fasting_view(request):
    return render(request, 'fasting.html')  

