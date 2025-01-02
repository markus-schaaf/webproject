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
from django.shortcuts import redirect
from django.contrib.auth import logout
from .forms import UserProfileForm
from django.shortcuts import render, get_object_or_404
from .models import UserProfile




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



def logout_view(request):
    logout(request)
    return redirect('trackerapp')
 
def calculate_macros(weight, height, age, gender, activity, goal):
    # Geschlechtsfaktor: +5 für männlich, -161 für weiblich
    gender_factor = 5 if gender == 'M' else -161

    # Berechnung des Grundumsatzes (BMR)
    bmr = 10 * weight + 6.25 * height - 5 * age + gender_factor

    # Aktivitätsfaktor
    activity_factors = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9,
    }
    bmr *= activity_factors[activity]

    # Zielanpassung
    if goal == 'weight_loss':
        bmr -= 500
    elif goal == 'weight_gain':
        bmr += 500

    # Makronährstoffe berechnen
    proteins = weight * 2
    fats = weight * 1
    carbs = (bmr - (proteins * 4 + fats * 9)) / 4

    return round(bmr), round(carbs), round(proteins), round(fats)


def calories_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.daily_calories, user.daily_carbohydrates, user.daily_proteins, user.daily_fats = calculate_macros(
                user.weight, user.height, user.age, user.gender, user.activity, user.goal
            )
            user.save()
            return redirect('trackerapp')
    else:
        form = UserProfileForm()

    return render(request, 'calories.html', {'form': form})

def trackerapp(request):
    # Benutzer Markus abrufen
    try:
        user = UserProfile.objects.get(username="Markus")
        # Makros berechnen
        bmr, carbs, proteins, fats = calculate_macros(
            weight=user.weight,
            height=user.height,
            age=user.age,
            gender=user.gender,
            activity=user.activity,
            goal=user.goal
        )

        # Variablen in den Kontext übergeben
        context = {
            'bmr': bmr,
            'carbs': carbs,
            'proteins': proteins,
            'fats': fats,
            'username': user.username,
        }
    except UserProfile.DoesNotExist:
        # Wenn Markus nicht existiert, leeren Kontext übergeben
        context = {
            'error': "Keine Daten für Markus gefunden."
        }

    return render(request, 'trackerapp.html', context)

def account_view(request):
    # Benutzer Markus aus der Datenbank abrufen
    try:
        user = UserProfile.objects.get(username="Markus")
        # Kontext mit allen Benutzerdaten erstellen
        context = {
            'user': user,
        }
    except UserProfile.DoesNotExist:
        context = {
            'error': "Benutzer Markus wurde nicht gefunden."
        }

    return render(request, 'account.html', context)