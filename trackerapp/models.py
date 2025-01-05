from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


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


from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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

    age = models.PositiveIntegerField(default=25)  
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    height = models.FloatField(default=170.0, help_text="Height in cm")
    weight = models.FloatField(default=70.0, help_text="Weight in kg") 
    activity = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default='sedentary') 
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES, default='maintenance') 
    daily_calories = models.PositiveIntegerField(default=2000)  
    daily_carbohydrates = models.PositiveIntegerField(default=250, help_text="Daily Carbohydrates in grams")
    daily_proteins = models.PositiveIntegerField(default=75, help_text="Daily Proteins in grams") 
    daily_fats = models.PositiveIntegerField(default=70, help_text="Daily Fats in grams") 


    def save(self, *args, **kwargs):
        if self.pk: 
            old_instance = UserProfile.objects.get(pk=self.pk)
            calories_changed = old_instance.daily_calories != self.daily_calories
        else:
            calories_changed = False

        if calories_changed:
            carbs_calories = self.daily_calories * 0.4  
            proteins_calories = self.daily_calories * 0.3  
            fats_calories = self.daily_calories * 0.3 

            self.daily_carbohydrates = round(carbs_calories / 4)  
            self.daily_proteins = round(proteins_calories / 4) 
            self.daily_fats = round(fats_calories / 9) 
        else:
            gender_factor = 5 if self.gender == 'M' else -161
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + gender_factor

            activity_factors = {
                'sedentary': 1.2,
                'light': 1.375,
                'moderate': 1.55,
                'active': 1.725,
                'very_active': 1.9,
            }
            bmr *= activity_factors[self.activity]

            if self.goal == 'weight_loss':
                bmr -= 500
            elif self.goal == 'weight_gain':
                bmr += 500

            self.daily_calories = round(bmr)

            carbs_calories = self.daily_calories * 0.4  
            proteins_calories = self.daily_calories * 0.3 
            fats_calories = self.daily_calories * 0.3 

            self.daily_carbohydrates = round(carbs_calories / 4)  
            self.daily_proteins = round(proteins_calories / 4)  
            self.daily_fats = round(fats_calories / 9)

        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.user.username 


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class DailyFood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.DateField(default=now)
    calories_eaten = models.PositiveIntegerField(default=0)
    fat_eaten = models.FloatField(default=0)
    carbohydrates_eaten = models.FloatField(default=0)
    protein_eaten = models.FloatField(default=0)
    calories_burned = models.PositiveIntegerField(default=0)
    daily_calorie_target = models.PositiveIntegerField(default=2000)
    calorie_result = models.IntegerField(default=0)
    fat = models.FloatField(default=0)
    carbohydrates = models.FloatField(default=0)
    protein = models.FloatField(default=0)

    class Meta:
        unique_together = ('user', 'day')

    def save(self, *args, **kwargs):
        # Automatische Berechnung von calorie_result
        self.calorie_result = self.daily_calorie_target - self.calories_eaten + self.calories_burned
        super().save(*args, **kwargs)  # Speichert das Modell wie gewohnt

    def __str__(self):
        return f"{self.user.username} - {self.day}"


from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class DailyWaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=now)
    glasses = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.glasses} Gläser"
