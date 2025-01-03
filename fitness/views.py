from django.shortcuts import render, redirect
from trackerapp.forms import NewExerciseForm
from fitness.models import Workout_Type

# Create your views here.
def exercise_overview_view(request):
    return render(request, 'exercise_overview.html')

def new_exercise_view(request):
    form = NewExerciseForm()

    if request.method =='POST':
        form = NewExerciseForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["workout_class"])
            print(form.cleaned_data["workout_type"])
        else:
            print(form.errors)
    else: form = NewExerciseForm()
    return render(request, 'new_exercise.html' , {'form' : form})

def workout_type_options(request):
    workout_class_id = request.GET.get("workout_class")
    workout_types = Workout_Type.objects.filter(workout_class_id=workout_class_id)
    return render (request, "fitness/workout_type_options.html", {"workout_types": workout_types})

