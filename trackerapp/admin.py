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
        'fat_eaten', 
        'carbohydrates_eaten', 
        'protein_eaten', 
    ]


from .models import DailyWaterIntake

@admin.register(DailyWaterIntake)
class DailyWaterIntakeAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'glasses') 
    list_filter = ('date',) 
    search_fields = ('user__username',)  