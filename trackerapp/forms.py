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
            # Calculate calories burned
            calories_per_kg_per_h = instance.workout_type.calories_per_kg_per_h
            instance.calories_burned = int(instance.workout_length * float(instance.weight) * float(calories_per_kg_per_h) / 60)
        if commit:
            instance.save()
        return instance