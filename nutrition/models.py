from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Food_Unit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Testzwecke True

    CATEGORIE_CHOICES = [
        ('breakfast', 'Frühstück'),
        ('lunch', 'Mittagessen'),
        ('dinner', 'Abendessen'),
        ('snack', 'Snack'),
    ]

    food_unit_id = models.AutoField(primary_key=True)  # Automatische ID
    food_unit_name = models.CharField(max_length=30, null=True)
    food_categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, default="Frühstück")
    time_eaten = models.DateTimeField(default=now)

    # Eingabewerte für 100g
    calories_per_100g = models.IntegerField(default=0)
    carbohydrates_per_100g = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    fat_per_100g = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    protein_per_100g = models.DecimalField(max_digits=8, decimal_places=4, default=0)

    # Menge in Gramm
    food_amount = models.IntegerField(default=100)

    # Berechnete Werte basierend auf Menge
    calories = models.IntegerField(default=0)
    carbohydrates = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    fat = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    protein = models.DecimalField(max_digits=8, decimal_places=4, default=0)

    def __str__(self):
        return f"Food Unit {self.food_unit_id} for User {self.user}"
