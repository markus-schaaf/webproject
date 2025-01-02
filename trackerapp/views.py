from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def trackerapp(request):
    return render(request, 'Trackerapp.html')

def login_view(request):
    return render(request, 'login.html')  

def calendar_view(request):
    return render(request, 'calendar.html')  

def calories_view(request):
    return render(request, 'calories.html')  

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


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # Speichert den neuen Benutzer
            return redirect('login')  # Weiterleitung nach erfolgreicher Registrierung
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Benutzer wird erstellt
            form.save()
            messages.success(request, 'Erfolgreich registriert!')
            return redirect('login')
        else:
            # Hier können auch spezifische Fehlermeldungen hinzugefügt werden
            if form.errors.get('username'):
                messages.error(request, 'Dieser Benutzername ist bereits vergeben.')
            if form.errors.get('email'):
                messages.error(request, 'Diese E-Mail-Adresse wird bereits verwendet.')
            if form.errors.get('password1'):
                messages.error(request, 'Die Passwörter stimmen nicht überein oder sind zu kurz.')

    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

  
def fasting_view(request):
    return render(request, 'fasting.html')  


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Benutzer authentifizieren
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Benutzer einloggen
            messages.success(request, "Erfolgreich eingeloggt!")
            return redirect('trackerapp')  # 'trackerapp' sollte der Name der URL sein
        else:
            messages.error(request, "Ungültiger Benutzername oder Passwort!")
    
    return render(request, 'account/login.html')

def recipes_view(request):
    # Beispielrezepte, die du später durch echte Daten ersetzen kannst
    recipes = [
        {'name': 'Mongolian Beef', 'description': 'Ein scharfes Rindfleischgericht aus der Mongolischen Küche.'},
        {'name': 'Spaghetti Bolognese', 'description': 'Klassische italienische Bolognese mit frischen Zutaten.'},
        {'name': 'Vegetarische Lasagne', 'description': 'Lasagne mit frischem Gemüse und Tomatensauce.'},
        {'name': 'Chicken Tikka Masala', 'description': 'Würziges Hühnchen in einer cremigen Tomatensauce.'},
        {'name': 'Caesar Salad', 'description': 'Frischer Salat mit Caesar-Dressing und knusprigen Croutons.'}
    ]
    return render(request, 'recipes.html', {'recipes': recipes})


@csrf_exempt
def check_username(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')

        # Überprüfe, ob der Benutzername bereits existiert
        exists = User.objects.filter(username=username).exists()
        return JsonResponse({'exists': exists})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def check_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        # Überprüfen, ob die E-Mail gültig ist
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'valid': False}, status=400)

        # Überprüfe, ob die E-Mail bereits existiert
        exists = User.objects.filter(email=email).exists()
        return JsonResponse({'exists': exists})

    return JsonResponse({'error': 'Invalid request'}, status=400)
