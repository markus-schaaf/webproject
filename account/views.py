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

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Erfolgreich eingeloggt!")
            return redirect('trackerapp')  # Redirect zur trackerapp-URL
        else:
            messages.error(request, "Ungültiger Benutzername oder Passwort!")

    return render(request, 'login.html')  # Template-Pfad anpassen


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