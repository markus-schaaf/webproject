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
  
  def __str__(self):
    return self.daily_food_id
