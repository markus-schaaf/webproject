from django.db import models

# Create your models here.

class User (models.Model):
  user_id = models.IntegerField(primary_key=True)
  user_first_name = models.CharField(max_length=30)
  user_last_name = models.CharField(max_length=30)
  created_at = models.DateTimeField(auto_now_add=True)
  weight = models.DecimalField(max_digits=4, decimal_places=1)
  weight_target = models.DecimalField(max_digits=4, decimal_places=1)
  daily_calorie_target = models.IntegerField

  def __str__(self):
    return self.user_id


class Workout_Type (models.Model):
  workout_type_id = models.IntegerField(primary_key=True)
  workout_name = models.CharField(max_length=80)
  workout_category = models.CharField(max_length=30)
  calories_per_kg_per_h = models.DecimalField(max_digits=16, decimal_places=15)

  def __str__(self):
    return self.workout_type_id


