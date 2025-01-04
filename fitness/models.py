from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

  
class Workout_Class (models.Model):
  workout_class_id = models.IntegerField (primary_key=True)
  workout_class = models.CharField (verbose_name="Übungsart", max_length=63)

  def __str__(self):
    return self.workout_class

class Workout_Type (models.Model):
  workout_type_id = models.IntegerField (primary_key=True)
  workout_type = models.CharField (max_length=255 )
  workout_class = models.ForeignKey (Workout_Class, on_delete=models.CASCADE, default=4)
  calories_per_kg_per_h = models.DecimalField (max_digits=16, decimal_places=15)
  
  def __str__(self):
    return self.workout_type
  
class Workout_Unit(models.Model):
    workout_type_unit = models.IntegerField (primary_key=True)
    name = models.CharField(max_length=30)
    time = models.DateTimeField(default=now)
    workout_type = models.ForeignKey(Workout_Type, on_delete=models.CASCADE)
    workout_class = models.ForeignKey (Workout_Class, on_delete=models.CASCADE)
    workout_length = models.IntegerField(default=0)  # Länge in Minuten
    weight = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)  # Gewicht in kg
    calories_burned = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.time.strftime('%Y-%m-%d')})"

