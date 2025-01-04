from django.shortcuts import render, redirect, get_object_or_404
from fitness.models import Workout_Type, Workout_Class, Workout_Unit
from account.models import User
from django.http import JsonResponse
from django.utils.timezone import now, localtime
from decimal import Decimal
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import F
from trackerapp.models import DailyFood

def workout_overview(request):
    now_local = localtime(now())

    # Set the start and end of today in the local timezone
    today_start = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    
    # Filter Workout_Unit objects that were created today
    workout_units_today = Workout_Unit.objects.filter(time__gte=today_start, time__lt=today_end)

    # Pass the data to the template
    return render(request, 'workout_overview.html', {'workout_units': workout_units_today})

@login_required
def delete_workout_unit(request, workout_unit_id):
    # Fetch the Workout_Unit object
    workout_unit = get_object_or_404(Workout_Unit, workout_type_unit=workout_unit_id)
    
    # Save the calories burned value and the user before deletion
    calories_burned = workout_unit.calories_burned
    user = request.user

    # Delete the workout unit
    workout_unit.delete()

    # Update the corresponding DailyFood entry
    today = now().date()
    try:
        daily_food = DailyFood.objects.get(user=user, day=today)

        # Subtract the burned calories and adjust the calorie result
        daily_food.calories_burned = F('calories_burned') - calories_burned
        daily_food.calorie_result = F('calorie_result') + calories_burned

        # Save the updated DailyFood entry
        daily_food.save()

        # Reload the DailyFood entry to check if calories_burned is zero
        daily_food.refresh_from_db()
        if daily_food.calories_burned <= 0:
            daily_food.calories_burned = 0  # Ensure no negative values
            daily_food.save()

    except DailyFood.DoesNotExist:
        # If no DailyFood entry exists, there's nothing to update
        pass

    return redirect('workout_overview')


def new_workout_view(request):
    return render(request, 'new_workout.html')

def get_workout_classes(request):
    workout_classes = Workout_Class.objects.all()
    results = [{"id": wc.workout_class_id, "name": wc.workout_class} for wc in workout_classes]
    return JsonResponse({"results": results})

# API: Workout-Typen basierend auf der ausgewählten Klasse abrufen
def get_workout_types(request):
    workout_class_id = request.GET.get('workout_class_id')
    if not workout_class_id:
        return JsonResponse({"results": []})
    
    workout_types = Workout_Type.objects.filter(workout_class_id=workout_class_id)
    results = [{"id": wt.workout_type_id, "name": wt.workout_type, "calories_per_kg_per_h": float(wt.calories_per_kg_per_h)} for wt in workout_types]
    return JsonResponse({"results": results})

# API: Ein neues Workout-Unit speichern
@login_required
def save_workout_unit(request):
    if request.method == 'POST':
        print(request.POST)
        data = request.POST
        workout_class_id = data.get('workout_class_id')
        if not workout_class_id:
            return redirect('workout_overview')

        try:
            # Workout-Class-Objekt aus der DB holen
            workout_class = Workout_Class.objects.get(workout_class_id=workout_class_id)
        except Workout_Class.DoesNotExist:
            return JsonResponse({"status": "error", "message": f"Workout Class mit der ID {workout_class_id} existiert nicht"})
        workout_type_id = data.get('workout_type_id')
        try:
            user_profile = request.user.userprofile  # Assuming a OneToOne relation exists
            weight = user_profile.weight
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User profile not found. Please update your profile."})
        workout_length = int(data.get('workout_length', 0))
        
        # Workout_Type und Workout_Class validieren
        workout_class = Workout_Class.objects.get(workout_class_id=workout_class_id)
        workout_type = Workout_Type.objects.get(workout_type_id=workout_type_id)

        # Kalorien berechnen
        calories_per_kg_per_h = workout_type.calories_per_kg_per_h
        weight_decimal = Decimal(weight)  # Convert weight to Decimal
        calories_decimal =Decimal(calories_per_kg_per_h)
        workout_hours = Decimal(workout_length / 60)
        calories_burned = int(calories_decimal * weight_decimal * workout_hours)
        
        # Neues Workout_Unit erstellen
        workout_unit = Workout_Unit.objects.create(
            name=f"{workout_type.workout_type} Session",
            workout_type=workout_type,
            workout_class=workout_class,
            time=now(),
            workout_length=workout_length,
            weight=weight,
            calories_burned=calories_burned
        )

        today = now().date()
        daily_food, created = DailyFood.objects.get_or_create(
            user=request.user,
            day=today,
            defaults={
                'calories_burned': calories_burned,
                'calorie_result': -calories_burned  # Subtract burned calories from target
            }
        )

        if not created:
            # Add calories_burned to the existing entry
            daily_food.calories_burned = F('calories_burned') + calories_burned
            daily_food.calorie_result = F('calorie_result') - calories_burned
            daily_food.save()

        return JsonResponse({"status": "success", "workout_unit_id": workout_unit.workout_type_unit})
    
    return JsonResponse({"status": "error", "message": "Invalid request method"})
