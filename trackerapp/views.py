from django.shortcuts import render
from .models import Food_Unit
import openfoodfacts

# Create your views here.
def trackerapp(request):
    return render(request, 'Trackerapp.html')

def login_view(request):
    return render(request, 'login.html')  


# View für Food Suche / API Suche
def search_food(request):
    query = request.GET.get('query')  # Nutzer-Eingabe
    if not query:
        return render(request, 'search_food.html', {'error': 'Bitte geben Sie ein Lebensmittel ein.'})

    # 1. Suche in der lokalen Datenbank
    food_item = Food_Unit.objects.filter(food_unit_name__iexact=query).first()

    if food_item:
        # Lebensmittel wurde lokal gefunden
        return render(request, 'search_food.html', {'food_item': food_item})

    # 2. Wenn nicht gefunden, API-Abfrage
    api = openfoodfacts.API(user_agent="MyAwesomeApp/1.0")
    response = api.product.text_search(query, page_size=1)

    if response and "products" in response:
        product = response["products"][0]
        code = product.get("code", "Kein Code")
        name = product.get("product_name", query)  # Fallback auf Suchbegriff
        nutriments = product.get("nutriments", {})
        calories = nutriments.get("energy-kcal", 0)
        proteins = nutriments.get("proteins_100g", 0)
        carbs = nutriments.get("carbohydrates_100g", 0)
        fats = nutriments.get("fat_100g", 0)

        # 3. Speichern in der lokalen Datenbank
        food_item = Food_Unit.objects.create(
            # user=request.user,
            food_unit_name=name,
            calories=calories,
            carbohydrates=carbs,
            fat=fats,
            protein=proteins
        )

        # Detailansicht des Lebensmittels
        return render(request, 'search_food.html', {'food_item': food_item})

    # 4. Fehlerhandling
    return render(request, 'search_food.html', {'error': 'Lebensmittel nicht gefunden.'})
