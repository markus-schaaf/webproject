from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class User_Food (models.Model):
  user = models.ForeignKey (User, on_delete=models.CASCADE)
  # food = 

class User_Workout (models.Model):
  user = models.ForeignKey (User, on_delete=models.CASCADE)
  # workout = 

class User_Daily (models.Model):
  user = models.ForeignKey (User, on_delete=models.CASCADE)
  # calorien_eaten = 
  # calorien_worked
  # calorien_diff

class Workout_Type (models.Model):
  workout_type_id = models.IntegerField(primary_key=True)
  workout_name = models.CharField (max_length=80)
  workout_category = models.CharField (max_length=30)
  calories_per_kg_per_h = models.DecimalField (max_digits=16, decimal_places=15)

  def __str__(self):
    return self.workout_type_id


class Daily_Workouts (models.Model):
  daily_workout_id = models.IntegerField (primary_key=True)
  user_id = models.ForeignKey (User, on_delete=models.CASCADE)
  workout_length = models.TimeField
  calories_burned = models.IntegerField

  def __str__(self):
    return self.daily_workout_id


class Daily_Food (models.Model):
  daily_food_id = models.IntegerField (primary_key=True)
  user = models.ForeignKey (User, on_delete=models.CASCADE, null=True, blank=True) # null/blank zum testen
  day = models.DateField 
  calories_eaten = models.IntegerField
  calories_burned = models.IntegerField
  daily_calorie_target = models.IntegerField
  calorie_result = models.IntegerField
  fat = models.DecimalField (max_digits=8, decimal_places=4)
  carbohydrates = models.DecimalField (max_digits=8, decimal_places=4)
  protein = models.DecimalField (max_digits=8, decimal_places=4)

  #user
  #day
  #name
  #menge
  #carbs
  #fat
  #protein
  #calories_eaten
  #calories_goal
  #time (frühstück, ...)


  def __str__(self):
    return self.daily_food_id

from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Verknüpfung mit User
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('light', 'Lightly Active'),
        ('moderate', 'Moderately Active'),
        ('active', 'Active'),
        ('very_active', 'Very Active'),
    ]

    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('maintenance', 'Maintenance'),
        ('weight_gain', 'Weight Gain'),
    ]

    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")
    activity = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    daily_calories = models.PositiveIntegerField()
    daily_carbohydrates = models.PositiveIntegerField(help_text="Daily Carbohydrates in grams")
    daily_proteins = models.PositiveIntegerField(help_text="Daily Proteins in grams")
    daily_fats = models.PositiveIntegerField(help_text="Daily Fats in grams")

    def __str__(self):
        return self.user.username  # Zeige den Namen aus der User-Tabelle


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)