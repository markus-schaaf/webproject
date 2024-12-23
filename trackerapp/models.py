from django.db import models
from django.utils.timezone import now

# Create your models here.

class User (models.Model):
  user_id = models.IntegerField (primary_key=True)
  user_first_name = models.CharField (max_length=30)
  user_last_name = models.CharField (max_length=30)
  created_at = models.DateTimeField (auto_now_add=True)
  weight = models.DecimalField (max_digits=4, decimal_places=1)
  weight_target = models.DecimalField (max_digits=4, decimal_places=1)
  daily_calorie_target = models.IntegerField

  def __str__(self):
    return self.user_id


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


class Workout_Unit (models.Model):
  workout_unit_id = models.IntegerField (primary_key=True)
  user_id = models.ForeignKey (User, on_delete=models.CASCADE)
  time = models.DateTimeField
  workout_type_id = models.IntegerField
  workout_length = models.TimeField
  calories_per_kg_per_h = models.DecimalField (max_digits=16, decimal_places=15)
  weight = models.DecimalField (max_digits=4, decimal_places=1)
  calories_burned = models.IntegerField

  def __str__(self):
    return self.workout_unit_id


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


class Food_Unit(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # null und blank nur für erste Testzwecke True
  food_unit_id = models.AutoField(primary_key=True)  # Automatische ID
  food_unit_name = models.CharField(max_length=30, null=True)
  time_eaten = models.DateTimeField(default=now)
  calories = models.IntegerField(default=0)
  carbohydrates = models.DecimalField(max_digits=8, decimal_places=4, default=0)
  fat = models.DecimalField(max_digits=8, decimal_places=4, default=0)
  protein = models.DecimalField(max_digits=8, decimal_places=4, default=0)


  def __str__(self):
    return f"Food Unit {self.food_unit_id} for User {self.user.user_first_name} {self.user.user_last_name}" 