from django.db import models
from django.contrib.auth.models import User

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