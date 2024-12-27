from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Bitte eine gültige E-Mail-Adresse eingeben.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")