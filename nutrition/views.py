from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from .models import Food_Unit
import openfoodfacts

# Template-Routing: search_food
def search_food(request):
    return render(request, 'search_food.html')  # Rendert die HTML-Seite mit JavaScript

# API: Suche nach ersten 10 Ergebnissen
def search_food_api(request):
    query = request.GET.get('query')
    if not query:
        return JsonResponse({'results': []})

    # API-Suche
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

# API: Detaillierte Infos für ausgewähltes Produkt
def food_details_api(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'success': False})

    # API-Suche für Details
    api = openfoodfacts.API(user_agent="MyAwesomeApp/1.0")
    response = api.product.get(code, fields=["product_name", "nutriments"])

    if response and "nutriments" in response and "product_name" in response:
        nutriments = response["nutriments"]
        name = response["product_name"]

        # Extrahiere die Nährwerte
        calories = nutriments.get("energy-kcal", 0)
        proteins = nutriments.get("proteins_100g", 0)
        carbs = nutriments.get("carbohydrates_100g", 0)
        fats = nutriments.get("fat_100g", 0)

        # Speichern in der lokalen Datenbank
        Food_Unit.objects.create(
            user=request.user,
            food_unit_name=name,
            calories=calories,
            carbohydrates=carbs,
            fat=fats,
            protein=proteins
        )

        return JsonResponse({
            'success': True,
            'name': name,
            'calories': calories,
            'protein': proteins,
            'carbohydrates': carbs,
            'fat': fats
        })

    return JsonResponse({'success': False})



# Zuletzt genutzte Food Units (letzter Monat)
def recent_food_units(request):
    one_month_ago = now() - timedelta(days=30)
    units = Food_Unit.objects.filter(time_eaten__gte=one_month_ago, user=request.user).order_by('-time_eaten')
    
    results = [{'id': unit.food_unit_id, 'name': unit.food_unit_name} for unit in units]
    print(f"Benutzer: {request.user.username}, Anzahl der gefundenen Einträge: {len(results)}")  # Debugging
    print(results) # debugging
    return JsonResponse({'results': results})



# API: Details für eine spezifische Food Unit abrufen
def food_unit_details(request):
    unit_id = request.GET.get('id')
    if not unit_id:
        return JsonResponse({'success': False, 'error': 'Keine ID angegeben.'})

    # Hole die Food Unit aus der Datenbank
    food_unit = get_object_or_404(Food_Unit, pk=unit_id, user=request.user)
    print(food_unit)
    return JsonResponse({
        'success': True,
        'name': food_unit.food_unit_name,
        'calories': food_unit.calories,
        'carbohydrates': food_unit.carbohydrates,
        'fat': food_unit.fat,
        'protein': food_unit.protein,
        'time_eaten': food_unit.time_eaten.strftime('%Y-%m-%d %H:%M:%S')
    })
