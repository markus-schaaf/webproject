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
from fitness.models import Workout_Unit
from django.http import JsonResponse
from django.utils.timezone import localtime


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
            login(request, user)  
            return redirect('home')  
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Erfolgreich registriert!')
            return redirect('login')
        else:
            if form.errors.get('username'):
                messages.error(request, 'Dieser Benutzername ist bereits vergeben.')
            if form.errors.get('email'):
                messages.error(request, 'Diese E-Mail-Adresse wird bereits verwendet.')
            if form.errors.get('password1'):
                messages.error(request, 'Die Passwörter stimmen nicht überein oder sind zu kurz.')

    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

@login_required  
def fasting_view(request):
    user_profile = request.user.userprofile

    # Pass intermittent_timer and intermittent_type to the template
    
    intermittent_timer = user_profile.intermittent_timer.isoformat() if user_profile.intermittent_timer else None
    intermittent_type = user_profile.intermittent_type
    
    return render(request, 'fasting.html', {
        'intermittent_timer': intermittent_timer,
        'intermittent_type': intermittent_type,
    })  


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('trackerapp')
        else:
            messages.error(request, "Ungültiger Benutzername oder Passwort!")
    
    return render(request, 'account/login.html')

def recipes_view(request):
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

        exists = User.objects.filter(username=username).exists()
        return JsonResponse({'exists': exists})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def check_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'valid': False}, status=400)

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
    return render(request, 'recipes/high_protein.html') 

def low_carb(request):
    return render(request, 'recipes/low_carb.html') 

def low_fat(request):
    return render(request, 'recipes/low_fat.html') 

def calories_100_200(request):
    return render(request, 'recipes/calories_100_200.html')  

def calories_200_400(request):
    return render(request, 'recipes/calories_200_400.html')

def calories_400_600(request):
    return render(request, 'recipes/calories_400_600.html') 

def calories_600_800(request):
    return render(request, 'recipes/calories_600_800.html')

def calories_800_1000(request):
    return render(request, 'recipes/calories_800_1000.html')  

def calories_1000_1200(request):
    return render(request, 'recipes/calories_1000_1200.html')

def calories_1200_1400(request):
    return render(request, 'recipes/calories_1200_1400.html')


from django import forms
from django.forms import ModelForm

from datetime import datetime, timedelta
from django.utils.timezone import now
from django.shortcuts import render, redirect
from .models import DailyFood, UserProfile
from nutrition.models import Food_Unit
from django.db.models import Q

@login_required
def trackerapp(request):
    today = now().date()  # Get today's date
    user = request.user

    # Handle the food tracker data
    daily_food_today = DailyFood.objects.filter(user=user, day=today).first()

    # If no daily food entry for today, create a new one based on the user's profile
    if not daily_food_today:
        try:
            user_profile = UserProfile.objects.get(user=user)
            DailyFood.objects.create(
                user=user,
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

    # Handle the selected date
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

    # Fetch daily food entry for the selected date
    daily_food_entry = DailyFood.objects.filter(user=user, day=selected_date).first()

    # Categories for food data
    categories = {
        'breakfast': 'Frühstück',
        'lunch': 'Mittagessen',
        'dinner': 'Abendessen',
        'snack': 'Snack'
    }

    # Fetch food items for each category for the selected date
    category_data = {}
    for category_key, category_label in categories.items():
        category_data[category_label] = Food_Unit.objects.filter(
            Q(user=user) &
            Q(time_eaten__date=selected_date) &
            Q(food_categorie=category_key)
        ).values('food_unit_id', 'food_unit_name', 'calories')

    # Handle workout data for the selected date
    selected_date_start = datetime.combine(selected_date, datetime.min.time())  # Start of the selected date
    selected_date_end = selected_date_start + timedelta(days=1)  # End of the selected date

    workout_units_selected_date = Workout_Unit.objects.filter(user=user, time__gte=selected_date_start, time__lt=selected_date_end)

    # Handle the navigation for the previous and next day
    prev_date = selected_date - timedelta(days=1)
    next_date = selected_date + timedelta(days=1) if selected_date < today else None

    context = {
        'daily_food_entry': daily_food_entry,
        'category_data': category_data,
        'selected_date': selected_date,
        'prev_date': prev_date if prev_date <= today else None,
        'next_date': next_date,
        'today': today,
        'workout_units': workout_units_selected_date,  # Pass workout data to template
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


from django.http import JsonResponse
from django.shortcuts import redirect

@login_required
def delete_food_entry(request, food_unit_id):
    try:
       
        food_unit = Food_Unit.objects.get(
            food_unit_id=food_unit_id, 
            user=request.user
        )

        
        entry_date = food_unit.time_eaten.date()
        calories_to_remove = food_unit.calories
        carbohydrates_to_remove = food_unit.carbohydrates
        fat_to_remove = food_unit.fat
        protein_to_remove = food_unit.protein

        
        food_unit.delete()

        
        daily_food_entry = DailyFood.objects.filter(user=request.user, day=entry_date).first()
        if daily_food_entry:
            
            daily_food_entry.calories_eaten = max(0, daily_food_entry.calories_eaten - calories_to_remove)
            daily_food_entry.carbohydrates_eaten = max(0, daily_food_entry.carbohydrates_eaten - carbohydrates_to_remove)
            daily_food_entry.fat_eaten = max(0, daily_food_entry.fat_eaten - fat_to_remove)
            daily_food_entry.protein_eaten = max(0, daily_food_entry.protein_eaten - protein_to_remove)

         
            daily_food_entry.calorie_result = (
                daily_food_entry.daily_calorie_target
                - daily_food_entry.calories_eaten
                + daily_food_entry.calories_burned
            )

            # Speichere die Änderungen
            daily_food_entry.save()
    except Food_Unit.DoesNotExist:
        
        pass

   
    return redirect('trackerapp')


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import DailyFood

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import DailyFood

@login_required
def get_completed_days(request):
    
    completed_days = DailyFood.objects.filter(
        user=request.user,
        calories_eaten__gt=0  
    ).values_list('day', flat=True)

    completed_days_list = [day.strftime('%Y-%m-%d') for day in completed_days]

    return JsonResponse({'completed_days': completed_days_list})


@login_required
@csrf_exempt
def save_timer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        start_time = data.get("start_time")

        if start_time:
            user_profile = request.user.userprofile
            user_profile.intermittent_timer = start_time
            user_profile.save()
            return JsonResponse({"message": "Timer saved successfully"}, status=200)

        return JsonResponse({"error": "Start time is required"}, status=400)

@login_required
@csrf_exempt
def clear_timer(request):
    if request.method == "POST":
        user_profile = request.user.userprofile
        user_profile.intermittent_timer = None
        user_profile.save()
        return JsonResponse({"message": "Timer cleared successfully"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
@csrf_exempt
def save_fasting_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        intermittent_timer = data.get('intermittent_timer')
        intermittent_type = data.get('intermittent_type')

        # Mapping fasting types (like "18:6", "16:8", "20:4") to numeric values
        fasting_type_map = {
            "18:6": 1,  # 18 hours fasting, 6 hours eating -> 1
            "16:8": 2,  # 16 hours fasting, 8 hours eating -> 2
            "20:4": 3,  # 20 hours fasting, 4 hours eating -> 3
        }

        # Check if the provided intermittent_type is valid
        numeric_fasting_type = fasting_type_map.get(intermittent_type)

        if numeric_fasting_type is not None:  # Valid fasting type found
            if intermittent_timer:
                user_profile = request.user.userprofile
                user_profile.intermittent_timer = datetime.fromisoformat(intermittent_timer)
                user_profile.intermittent_type = numeric_fasting_type  # Save the numeric fasting type
                user_profile.save()

                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'No timer data provided'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid fasting type provided'}, status=400)

    return JsonResponse({'status': 'error'}, status=400)
