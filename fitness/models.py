from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Workout_Unit (models.Model):
  user = models.ForeignKey (User, on_delete=models.CASCADE)
  workout_unit_id = models.IntegerField (primary_key=True)
  workout_unit_name = models.CharField(max_length=30)
  time_worked = models.DateTimeField
  workout_type = models.CharField(max_length=30)
  workout_length = models.TimeField
  calories_per_kg_per_h = models.DecimalField (max_digits=16, decimal_places=15)

  def __str__(self):
    return self.workout_unit_id
  

"""
Original Model von Thomas
class Workout_Unit (models.Model):
  user = models.ForeignKey (User, on_delete=models.CASCADE)
  workout_unit_id = models.IntegerField (primary_key=True)
  workout_unit_name = models.CharField(max_length=30)
  time = models.DateTimeField
  workout_type_id = models.IntegerField
  workout_length = models.TimeField
  calories_per_kg_per_h = models.DecimalField (max_digits=16, decimal_places=15)
  weight = models.DecimalField (max_digits=4, decimal_places=1)
  calories_burned = models.IntegerField

  def __str__(self):
    return self.workout_unit_id
"""