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

@login_required
def workout_overview(request):
    now_local = localtime(now())

    today_start = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    
    workout_units_today = Workout_Unit.objects.filter(user=request.user,time__gte=today_start, time__lt=today_end)

    return render(request, 'workout_overview.html', {'workout_units': workout_units_today})

@login_required
def delete_workout_unit(request, workout_unit_id):
    workout_unit = get_object_or_404(Workout_Unit, workout_type_unit=workout_unit_id)
    
    calories_burned = workout_unit.calories_burned
    user = request.user

    workout_unit.delete()

    today = now().date()
    try:
        daily_food = DailyFood.objects.get(user=user, day=today)

        daily_food.calories_burned = F('calories_burned') - calories_burned
        daily_food.calorie_result = F('calorie_result') + calories_burned

        daily_food.save()

        daily_food.refresh_from_db()
        if daily_food.calories_burned <= 0:
            daily_food.calories_burned = 0 
            daily_food.save()

    except DailyFood.DoesNotExist:
        pass

    return redirect('workout_overview')


def new_workout_view(request):
    return render(request, 'new_workout.html')

def get_workout_classes(request):
    workout_classes = Workout_Class.objects.all()
    results = [{"id": wc.workout_class_id, "name": wc.workout_class} for wc in workout_classes]
    return JsonResponse({"results": results})

def get_workout_types(request):
    workout_class_id = request.GET.get('workout_class_id')
    if not workout_class_id:
        return JsonResponse({"results": []})
    
    workout_types = Workout_Type.objects.filter(workout_class_id=workout_class_id)
    results = [{"id": wt.workout_type_id, "name": wt.workout_type, "calories_per_kg_per_h": float(wt.calories_per_kg_per_h)} for wt in workout_types]
    return JsonResponse({"results": results})

@login_required
def save_workout_unit(request):
    if request.method == 'POST':
        print(request.POST)
        data = request.POST
        workout_class_id = data.get('workout_class_id')
        if not workout_class_id:
            return redirect('workout_overview')

        try:
            workout_class = Workout_Class.objects.get(workout_class_id=workout_class_id)
        except Workout_Class.DoesNotExist:
            return JsonResponse({"status": "error", "message": f"Workout Class mit der ID {workout_class_id} existiert nicht"})
        workout_type_id = data.get('workout_type_id')
        try:
            user_profile = request.user.userprofile 
            weight = user_profile.weight
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User profile not found. Please update your profile."})
        workout_length = int(data.get('workout_length', 0))
        
        workout_class = Workout_Class.objects.get(workout_class_id=workout_class_id)
        workout_type = Workout_Type.objects.get(workout_type_id=workout_type_id)

        calories_per_kg_per_h = workout_type.calories_per_kg_per_h
        weight_decimal = Decimal(weight) 
        calories_decimal =Decimal(calories_per_kg_per_h)
        workout_hours = Decimal(workout_length / 60)
        calories_burned = int(calories_decimal * weight_decimal * workout_hours)
        
        workout_unit = Workout_Unit.objects.create(
            user=request.user,
            name=f"{workout_type.workout_type}",
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
                'calorie_result': -calories_burned 
            }
        )

        if not created:
            
            daily_food.calories_burned = F('calories_burned') + calories_burned
            daily_food.calorie_result = F('calorie_result') - calories_burned
            daily_food.save()

        return JsonResponse({"status": "success", "workout_unit_id": workout_unit.workout_type_unit})
    
    return JsonResponse({"status": "error", "message": "Invalid request method"})
