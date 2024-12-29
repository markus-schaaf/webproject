from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib import messages

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authentifizierung des Benutzers
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Benutzer einloggen
            messages.success(request, "Erfolgreich eingeloggt!")
            
            # Weiterleitung zur 'trackerapp' URL nach erfolgreichem Login
            return redirect('trackerapp')  # 'trackerapp' ist der Name der URL in deiner urls.py
        else:
            messages.error(request, "Ungültiger Benutzername oder Passwort!")
    
    return render(request, 'account/login.html')

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Nutzer direkt anmelden
            return redirect("trackerapp")  # Nach Registrierung zur Startseite weiterleiten
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})