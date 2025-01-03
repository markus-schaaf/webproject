from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from .forms import SignUpForm
from .forms import UserProfileForm, NewExerciseForm
from .models import UserProfile
from fitness.models import Workout_Type
from django.http import JsonResponse

# Create your views here.
def trackerapp(request):
    return render(request, 'Trackerapp.html')

def login_view(request):
    return render(request, 'login.html')  

def calendar_view(request):
    return render(request, 'calendar.html')  

def calories_view(request):
    return render(request, 'calories.html')

def recipes_view(request):
    return render(request, 'recipes.html')    

def account_view(request):
    return render(request, 'account.html')   

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
  
def logout_view(request):
    logout(request)  # Benutzer ausloggen
    return redirect('trackerapp')  # Weiterleitung zur Homepage



def fasting_view(request):
    return render(request, 'fasting.html')  

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
                user.weight, user.height, user.age, user.activity, user.activity, user.goal
            )
            user.save()
            return redirect('trackerapp')
    else:
        form = UserProfileForm()

    return render(request, 'calories.html', {'form': form})

def trackerapp(request):
    return render(request, 'trackerapp.html')

from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from .views import calculate_macros  # Importiere die Berechnungsfunktion

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

def workout_type_options(request):
    workout_class_id = request.GET.get("workout_class")
    workout_types = Workout_Type.objects.filter(workout_class_id=workout_class_id)

    # Handle form submission (POST)
    if request.method == "POST":
        form = NewExerciseForm(request.POST)  
        if form.is_valid():   
            form.save()
            return redirect('fitness/exercise_overview')  
    else:
        form = NewExerciseForm()  

    if workout_class_id:
        options_html = ''.join([f'<option value="{wt.workout_type_id}">{wt.workout_type}</option>' for wt in workout_types])
        return JsonResponse({'options_html': options_html})

    return render(request, "workout_type_options.html", {"workout_types": workout_types, "form": form})