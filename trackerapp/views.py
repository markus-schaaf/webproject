from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth import logout
from .forms import SignUpForm
from .forms import UserProfileForm
from .models import UserProfile
from fitness.models import Workout_Type
from django.http import JsonResponse


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
            return redirect('trackerapp')
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
    return redirect('login')
 

@login_required
def user_profile_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        
        context = {
            'user_profile': user_profile
        }
    except UserProfile.DoesNotExist:
        context = {
            'error': "Kein Profil für den angemeldeten Benutzer gefunden."
        }

    return render(request, 'account.html', context)


from django.utils.timezone import now
from .models import DailyFood

@login_required
def edit_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=user_profile)
            if form.is_valid():
                form.save()

                daily_calories = user_profile.daily_calories
                carbohydrates = user_profile.daily_carbohydrates
                protein = user_profile.daily_proteins
                fat = user_profile.daily_fats

                daily_food_entry = DailyFood.objects.filter(user=request.user, day=now().date()).first()

                if not daily_food_entry:
                    DailyFood.objects.create(
                        user=request.user,
                        day=now().date(),
                        daily_calorie_target=daily_calories,
                        carbohydrates=carbohydrates,
                        protein=protein,
                        fat=fat,
                        calories_eaten=0,
                        fat_eaten=0,
                        carbohydrates_eaten=0,
                        protein_eaten=0,
                        calories_burned=0,
                        calorie_result=0,
                    )
                else: 
                    daily_food_entry.daily_calorie_target = daily_calories
                    daily_food_entry.carbohydrates = carbohydrates
                    daily_food_entry.protein = protein
                    daily_food_entry.fat = fat
                    daily_food_entry.save()

                messages.success(request, 'Profil erfolgreich aktualisiert und DailyFood-Werte gespeichert!')
                return redirect('trackerapp')
        else:
            form = UserProfileForm(instance=user_profile)
    except UserProfile.DoesNotExist:
        form = UserProfileForm()

    return render(request, 'edit_profile.html', {'form': form})


def high_protein(request):
    return render(request, 'recipes/high_protein.html')  # Template für High Protein Rezepte

def low_carb(request):
    return render(request, 'recipes/low_carb.html')  # Template für Low Carb Rezepte

def low_fat(request):
    return render(request, 'recipes/low_fat.html')  # Template für Low Fat Rezepte

def calories_100_200(request):
    return render(request, 'recipes/calories_100_200.html')  # Template für 100-200 Kalorien Rezepte

def calories_200_400(request):
    return render(request, 'recipes/calories_200_400.html')  # Template für 200-400 Kalorien Rezepte

def calories_400_600(request):
    return render(request, 'recipes/calories_400_600.html')  # Template für 400-600 Kalorien Rezepte

def calories_600_800(request):
    return render(request, 'recipes/calories_600_800.html')  # Template für 600-800 Kalorien Rezepte

def calories_800_1000(request):
    return render(request, 'recipes/calories_800_1000.html')  # Template für 800-1000 Kalorien Rezepte

def calories_1000_1200(request):
    return render(request, 'recipes/calories_1000_1200.html')  # Template für 1000-1200 Kalorien Rezepte

def calories_1200_1400(request):
    return render(request, 'recipes/calories_1200_1400.html')  # Template für 1200-1400 Kalorien Rezepte


from django import forms
from django.forms import ModelForm

from datetime import datetime, timedelta
from django.utils.timezone import now
from django.shortcuts import render, redirect
from .models import DailyFood, UserProfile

@login_required
def trackerapp(request):
    today = now().date()

    daily_food_today = DailyFood.objects.filter(user=request.user, day=today).first()

    if not daily_food_today:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            DailyFood.objects.create(
                user=request.user,
                day=today,
                daily_calorie_target=user_profile.daily_calories,
                carbohydrates=user_profile.daily_carbohydrates,
                protein=user_profile.daily_proteins,
                fat=user_profile.daily_fats,
                calories_eaten=0,
                fat_eaten=0,
                carbohydrates_eaten=0,
                protein_eaten=0,
                calories_burned=0,
                calorie_result=0,
            )
        except UserProfile.DoesNotExist:
            return render(request, 'trackerapp.html', {'error': 'Kein Benutzerprofil gefunden. Bitte erstellen Sie ein Profil.'})

    selected_date = request.GET.get('date')
    if selected_date:
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            return redirect('trackerapp')
    else:
        selected_date = today

    if selected_date > today:
        return redirect('trackerapp')

    daily_food_entry = DailyFood.objects.filter(user=request.user, day=selected_date).first()

    prev_date = selected_date - timedelta(days=1)
    next_date = selected_date + timedelta(days=1) if selected_date < today else None

    context = {
        'daily_food_entry': daily_food_entry,
        'selected_date': selected_date,
        'prev_date': prev_date if prev_date <= today else None,  
        'next_date': next_date,
        'today': today,
    }

    return render(request, 'trackerapp.html', context)

from .models import DailyWaterIntake
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.dateparse import parse_date

@login_required
@csrf_exempt
def water_tracker_view(request):
    if request.method == "GET":
        date_str = request.GET.get('date')
        selected_date = parse_date(date_str) if date_str else now().date()

        water_entry = DailyWaterIntake.objects.filter(user=request.user, date=selected_date).first()
        if water_entry:
            return JsonResponse({'glasses': water_entry.glasses})
        else:
            return JsonResponse({'glasses': 0})

    elif request.method == "POST":
        data = json.loads(request.body)
        date_str = data.get('date')
        selected_date = parse_date(date_str) if date_str else now().date()
        glasses = data.get('glasses', 0)

        water_entry, created = DailyWaterIntake.objects.get_or_create(user=request.user, date=selected_date)
        water_entry.glasses = glasses
        water_entry.save()

        return JsonResponse({'message': 'Erfolgreich gespeichert', 'glasses': water_entry.glasses})
