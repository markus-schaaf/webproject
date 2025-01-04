from django.shortcuts import render
from fitness.models import Workout_Type, Workout_Class, Workout_Unit
from django.http import JsonResponse
from django.utils.timezone import now

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
def save_workout_unit(request):
    if request.method == 'POST':
        print(request.POST)
        data = request.POST
        workout_class_id = data.get('workout_class_id')
        if not workout_class_id:
            return JsonResponse({"status": "error", "message": "Workout class ID fehlt"})

        try:
            # Workout-Class-Objekt aus der DB holen
            workout_class = Workout_Class.objects.get(workout_class_id=workout_class_id)
        except Workout_Class.DoesNotExist:
            return JsonResponse({"status": "error", "message": f"Workout Class mit der ID {workout_class_id} existiert nicht"})
        workout_type_id = data.get('workout_type_id')
        weight = float(data.get('weight', 0))
        workout_length = int(data.get('workout_length', 0))
        
        # Workout_Type und Workout_Class validieren
        workout_class = Workout_Class.objects.get(workout_class_id=workout_class_id)
        workout_type = Workout_Type.objects.get(workout_type_id=workout_type_id)

        # Kalorien berechnen
        calories_per_kg_per_h = workout_type.calories_per_kg_per_h
        calories_burned = int(calories_per_kg_per_h * weight * (workout_length / 60))
        
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
        return JsonResponse({"status": "success", "workout_unit_id": workout_unit.workout_type_unit})
    
    return JsonResponse({"status": "error", "message": "Invalid request method"})
