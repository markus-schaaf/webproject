from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

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