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
        fields = ['username', 'age', 'gender', 'height', 'weight', 'activity', 'goal']
