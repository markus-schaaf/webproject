from django.contrib import admin
from .models import UserProfile
from .models import DailyFood

admin.site.register(UserProfile)


@admin.register(DailyFood)
class DailyFoodAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'day',
        'calories_eaten',
        'calories_burned',
        'daily_calorie_target',
        'calorie_result',
        'fat_eaten',  # Neues Feld
        'carbohydrates_eaten',  # Neues Feld
        'protein_eaten',  # Neues Feld
    ]