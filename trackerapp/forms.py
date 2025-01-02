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