from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
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