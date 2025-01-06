from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from .models import Food_Unit
from trackerapp.models import DailyFood
import openfoodfacts
import json

def search_food(request):
    return render(request, 'search_food.html')

def search_food_api(request):
    query = request.GET.get('query')
    if not query:
        return JsonResponse({'results': []})

    api = openfoodfacts.API(user_agent="MyAwesomeApp/1.0")
    response = api.product.text_search(query, page_size=10)

    results = []
    if response and "products" in response:
        for product in response["products"]:
            results.append({
                'code': product.get("code"),
                'name': product.get("product_name", "Unbekannt")
            })

    return JsonResponse({'results': results})

def food_details_api(request):
    code = request.GET.get('code')

    if not code:
        return JsonResponse({'success': False})

    api = openfoodfacts.API(user_agent="MyAwesomeApp/1.0")
    response = api.product.get(code, fields=["product_name", "nutriments"])

    if response and "nutriments" in response and "product_name" in response:
        nutriments = response["nutriments"]
        name = response["product_name"]

        calories_100g = nutriments.get("energy-kcal", 0)
        proteins_100g = nutriments.get("proteins_100g", 0)
        carbs_100g = nutriments.get("carbohydrates_100g", 0)
        fats_100g = nutriments.get("fat_100g", 0)

        return JsonResponse({
            'success': True,
            'name': name,
            'calories_100g': int(calories_100g),
            'protein_100g': int(proteins_100g),
            'carbohydrates_100g': int(carbs_100g),
            'fat_100g': int(fats_100g),
        })

    return JsonResponse({'success': False})

def recent_food_units(request):
    one_month_ago = now() - timedelta(days=30)
    units = Food_Unit.objects.filter(time_eaten__gte=one_month_ago, user=request.user).order_by('-time_eaten')

    results = [{'id': unit.food_unit_id, 'name': unit.food_unit_name} for unit in units]
    return JsonResponse({'results': results})

def food_unit_details(request):
    unit_id = request.GET.get('id')
    if not unit_id:
        return JsonResponse({'success': False, 'error': 'Keine ID angegeben.'})

    food_unit = get_object_or_404(Food_Unit, pk=unit_id, user=request.user)
    return JsonResponse({
        'success': True,
        'name': food_unit.food_unit_name,
        'calories': int(food_unit.calories_per_100g),
        'carbohydrates': int(food_unit.carbohydrates_per_100g),
        'fat': int(food_unit.fat_per_100g),
        'protein': int(food_unit.protein_per_100g),
        'time_eaten': food_unit.time_eaten.strftime('%Y-%m-%d %H:%M:%S')
    })

def save_food_unit(request):
    if request.method == "POST":
        try:
            unit_data = json.loads(request.body)

            name = unit_data.get('name')
            amount = int(''.join(filter(str.isdigit, unit_data.get('amount', '100'))))
            calories_100g = int(''.join(filter(str.isdigit, unit_data.get('calories_100g', '0'))))
            carbs_100g = int(''.join(filter(str.isdigit, unit_data.get('carbohydrates_100g', '0'))))
            fat_100g = int(''.join(filter(str.isdigit, unit_data.get('fat_100g', '0'))))
            protein_100g = int(''.join(filter(str.isdigit, unit_data.get('protein_100g', '0'))))
            categorie = unit_data.get('categorie')

            calories = (calories_100g / 100) * amount
            carbs = (carbs_100g / 100) * amount
            fat = (fat_100g / 100) * amount
            protein = (protein_100g / 100) * amount

            today = now().date()
            daily_food_entry, created = DailyFood.objects.get_or_create(
                user=request.user, day=today,
                defaults={
                    'calories_eaten': calories,
                    'fat_eaten': fat,
                    'carbohydrates_eaten': carbs,
                    'protein_eaten': protein,
                }
            )

            if not created:
                daily_food_entry.calories_eaten += calories
                daily_food_entry.fat_eaten += fat
                daily_food_entry.carbohydrates_eaten += carbs
                daily_food_entry.protein_eaten += protein
                daily_food_entry.save()

            daily_food_entry.calorie_result = daily_food_entry.daily_calorie_target - daily_food_entry.calories_eaten + daily_food_entry.calories_burned
            daily_food_entry.save()
            
            print(f"carbs aus text: ", carbs_100g)
            print(protein, type(protein))
            print(carbs, type(carbs))
            print(fat, type(fat))


            Food_Unit.objects.create(
                user=request.user,
                food_unit_name=name,
                food_categorie=categorie,
                food_amount=amount,
                calories_per_100g=calories_100g,
                carbohydrates_per_100g=carbs_100g,
                fat_per_100g=fat_100g,
                protein_per_100g=protein_100g,
                calories=calories,
                carbohydrates=carbs,
                fat=fat,
                protein=protein,
            )

            return JsonResponse({'success': True})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'success': False}, status=405)
