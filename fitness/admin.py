from django.contrib import admin
from .models import Workout_Unit

@admin.register(Workout_Unit)
class WorkoutUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'workout_type', 'workout_class', 'time', 'workout_length', 'weight', 'calories_burned')
    list_filter = ('time', 'workout_type', 'workout_class', 'user')
    search_fields = ('name', 'user__username')
    ordering = ('-time',)  # Zeigt die neuesten Einträge zuerst
    date_hierarchy = 'time'  # Fügt eine Zeitnavigation hinzu
