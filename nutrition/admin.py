from django.contrib import admin
from .models import Food_Unit


@admin.register(Food_Unit)
class FoodUnitAdmin(admin.ModelAdmin):
    list_display = (
        'food_unit_id',
        'food_unit_name',
        'food_categorie',
        'time_eaten',
        'calories_per_100g',
        'carbohydrates_per_100g',
        'fat_per_100g',
        'protein_per_100g',
        'food_amount',
        'calories',
        'carbohydrates',
        'fat',
        'protein',
        'user',
    )
    list_filter = ('food_categorie', 'time_eaten', 'user')
    search_fields = ('food_unit_name', 'user__username')
    ordering = ('-time_eaten',)
