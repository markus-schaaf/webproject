from django.contrib import admin
from .models import UserProfile
from .models import DailyFood

admin.site.register(UserProfile)


# Register DailyFood Model
@admin.register(DailyFood)
class DailyFoodAdmin(admin.ModelAdmin):
    list_display = ('user', 'day', 'calories_eaten', 'calories_burned', 'daily_calorie_target', 'calorie_result', 'eaten_fat', 'eaten_carbohydrates', 'eaten_protein')
    list_filter = ('user', 'day')  # Ermöglicht Filterung nach User und Datum
    search_fields = ('user__username',)  # Ermöglicht Suche nach Benutzername