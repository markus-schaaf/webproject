from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from fitness.models import Workout_Type, Workout_Unit

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Bitte geben Sie eine gültige E-Mail-Adresse ein.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'gender', 'height', 'weight', 'activity', 'goal', 'daily_calories']
        widgets = {
            'gender': forms.RadioSelect,
            'activity': forms.RadioSelect,
            'goal': forms.RadioSelect,
        }
        labels = {
            'age': 'Alter',
            'gender': 'Geschlecht',
            'height': 'Größe (cm)',
            'weight': 'Gewicht (kg)',
            'activity': 'Aktivitätslevel',
            'goal': 'Ziel',
            'daily_calories': 'Tägliche Kalorien (optional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Entferne die leere Auswahl explizit
        self.fields['gender'].choices = [
            (choice[0], choice[1]) for choice in self.fields['gender'].choices if choice[0] != ''
        ]
        self.fields['activity'].choices = [
            (choice[0], choice[1]) for choice in self.fields['activity'].choices if choice[0] != ''
        ]
        self.fields['goal'].choices = [
            (choice[0], choice[1]) for choice in self.fields['goal'].choices if choice[0] != ''
        ]



class NewExerciseForm(forms.ModelForm):
    class Meta:
        model = Workout_Unit
        fields = ['workout_class', 'workout_type', 'workout_length', 'weight']
        widgets = {
            'workout_class': forms.Select(attrs={
                "hx-get": "/fitness/workout_type_options/",
                "hx-target": "#workout_type_options",
                "hx-trigger": "change"
            }),
            'workout_type': forms.Select(attrs={"id": "workout_type_options"}),
            'workout_length': forms.NumberInput(attrs={"min": 1}),
            'weight': forms.NumberInput(attrs={"min": 0.1, "step": 0.1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['workout_type'].queryset = Workout_Type.objects.none()

        if 'workout_class' in self.data:
            try:
                workout_class_id = int(self.data.get('workout_class'))
                self.fields['workout_type'].queryset = Workout_Type.objects.filter(workout_class_id=workout_class_id).order_by('workout_class')
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            self.fields['workout_type'].queryset = Workout_Type.objects.filter(workout_class=self.instance.workout_class)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.workout_type and instance.weight and instance.workout_length:
            calories_per_kg_per_h = instance.workout_type.calories_per_kg_per_h
            instance.calories_burned = int(instance.workout_length * float(instance.weight) * float(calories_per_kg_per_h) / 60)
        if commit:
            instance.save()
        return instance
    
from .models import DailyFood

from django import forms
from .models import DailyFood

class DailyFoodForm(forms.ModelForm):
    class Meta:
        model = DailyFood
        fields = [
            'day',
            'calories_eaten',
            'calories_burned',
            'daily_calorie_target',
            'fat_eaten',  # Neues Feld
            'carbohydrates_eaten',  # Neues Feld
            'protein_eaten',  # Neues Feld
        ]
        widgets = {
            'day': forms.DateInput(attrs={'type': 'date'}),
            'calories_eaten': forms.NumberInput(attrs={'min': 0}),
            'calories_burned': forms.NumberInput(attrs={'min': 0}),
            'daily_calorie_target': forms.NumberInput(attrs={'min': 0}),
            'fat_eaten': forms.NumberInput(attrs={'min': 0, 'step': 0.1}),
            'carbohydrates_eaten': forms.NumberInput(attrs={'min': 0, 'step': 0.1}),
            'protein_eaten': forms.NumberInput(attrs={'min': 0, 'step': 0.1}),
        }
        labels = {
            'day': 'Datum',
            'calories_eaten': 'Kalorien gegessen',
            'calories_burned': 'Kalorien verbrannt',
            'daily_calorie_target': 'Tägliches Kalorienziel',
            'fat_eaten': 'Gegessenes Fett (g)',
            'carbohydrates_eaten': 'Gegessene Kohlenhydrate (g)',
            'protein_eaten': 'Gegessenes Protein (g)',
        }