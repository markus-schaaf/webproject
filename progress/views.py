from django.shortcuts import render
from django.http import JsonResponse
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
from datetime import timedelta

# NICHT REaL
data = {
    "Kalorienaufnahme": [2000, 2200, 2100, 2000, 2300, 1900, 2500, 2000, 2100, 2200],
    "Kalorienverbrauch": [2500, 2400, 2600, 2500, 2400, 2700, 2200, 2500, 2600, 2400],
    "Gewicht": [80, 79.8, 79.7, 79.6, 79.8, 79.4, 79.5, 79.3, 79.2, 79.4]
}


df = pd.DataFrame(data)
X = df[["Kalorienaufnahme", "Kalorienverbrauch"]]
y = df["Gewicht"]
model = LinearRegression()
model.fit(X, y)



def calculate_reward(kalorienaufnahme, kalorienverbrauch):
    defizit = kalorienverbrauch - kalorienaufnahme
    return defizit * 0.1 if defizit > 0 else defizit * -0.1



def generate_recommendations(kalorienaufnahme, kalorienverbrauch):
    defizit = kalorienverbrauch - kalorienaufnahme
    if defizit > 500:
        return "Super! Dein Defizit ist optimal. Halte es so für schnelle Fortschritte."
    elif defizit < 0:
        return "Du hast ein Kalorienüberschuss. Reduziere deine Aufnahme oder erhöhe deinen Verbrauch."
    else:
        return "Dein Defizit ist gering. Versuche es leicht zu erhöhen."

from django.http import JsonResponse

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def predict_progress(request):
    if request.method == "POST":
        try:
           
            current_weight = float(request.POST.get("current_weight"))
            target_weight = float(request.POST.get("target_weight"))
            kalorienaufnahme = float(request.POST.get("kalorienaufnahme"))
            kalorienverbrauch = float(request.POST.get("kalorienverbrauch"))
            days_remaining = int(request.POST.get("days_remaining"))

            
            if current_weight <= 0 or target_weight <= 0 or kalorienaufnahme <= 0 or kalorienverbrauch <= 0 or days_remaining <= 0:
                return JsonResponse({"error": "Alle Werte müssen positiv sein!"}, status=400)

            
            predicted_weight = current_weight - (kalorienaufnahme - kalorienverbrauch) * days_remaining / 7700
            tage_bis_ziel = (current_weight - target_weight) * 7700 / (kalorienaufnahme - kalorienverbrauch)

            
            aktivitaeten_zeitersparnis = {
                "Laufen": "1 Tag",
                "Krafttraining": "2 Tage"
            }

            return JsonResponse({
                "predicted_weight": predicted_weight,
                "tage_bis_ziel": tage_bis_ziel,
                "aktivitaeten_zeitersparnis": aktivitaeten_zeitersparnis
            })

        except Exception as e:
            return JsonResponse({"error": f"Fehler bei der Berechnung: {str(e)}"}, status=400)
    return JsonResponse({"error": "Ungültige Anfrage"}, status=400)



def progress_home(request):
    kalorienaufnahme = 2200
    kalorienverbrauch = 2400
    recommendation = generate_recommendations(kalorienaufnahme, kalorienverbrauch)
    return render(request, "progress/progress.html", {"recommendation": recommendation})



def predict_progress_with_activities(request):
    try:
       
        current_weight = float(request.POST.get('current_weight', 0))
        target_weight = float(request.POST.get('target_weight', 0))
        kalorienaufnahme = float(request.POST.get('kalorienaufnahme', 0))
        kalorienverbrauch = float(request.POST.get('kalorienverbrauch', 0))
        days = int(request.POST.get('days', 0))


        
        kalorienbilanz = kalorienaufnahme - kalorienverbrauch
        taegliche_gewichtveraenderung = kalorienbilanz / 7700.0
        predicted_weight = current_weight + (taegliche_gewichtveraenderung * days)
        tage_bis_ziel = (current_weight - target_weight) / taegliche_gewichtveraenderung if kalorienbilanz != 0 else None

     
        aktivitaeten = {
            "Joggen (30 min)": 200,
            "Fahrradfahren (30 min)": 150,
            "Schwimmen (30 min)": 250,
        }
        aktivitaeten_zeitersparnis = {}
        for aktivitaet, kalorien in aktivitaeten.items():
            neue_bilanz = kalorienbilanz - kalorien
            if neue_bilanz != 0:
                neue_tage = (current_weight - target_weight) * 7700.0 / neue_bilanz
                aktivitaeten_zeitersparnis[aktivitaet] = max(0, tage_bis_ziel - neue_tage)

 
        response = {
            "current_weight": current_weight,
            "target_weight": target_weight,
            "predicted_weight": round(predicted_weight, 2),
            "tage_bis_ziel": round(tage_bis_ziel, 2) if tage_bis_ziel else "Unendlich",
            "aktivitaeten_zeitersparnis": aktivitaeten_zeitersparnis,
        }
        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({"error": "Fehler bei der Berechnung", "details": str(e)}, status=400)



import pickle
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse


with open('progress\gewichtsverlust_modell.pkl', 'rb') as model_file:
    model = pickle.load(model_file)


def progress_home(request):
    return render(request, 'progress/progress_home.html')


def predict_progress(request):
    if request.method == 'POST':
        
        aktuelles_gewicht = float(request.POST.get('aktuelles_gewicht'))
        zielgewicht = float(request.POST.get('zielgewicht'))
        kalorienaufnahme = float(request.POST.get('kalorienaufnahme'))
        kalorienverbrauch = float(request.POST.get('kalorienverbrauch'))
        verbleibende_tage = int(request.POST.get('verbleibende_tage'))
        aktivitaetslevel = float(request.POST.get('aktivitaetslevel'))

        
        kalorien_defizit = kalorienverbrauch - kalorienaufnahme
        tagesverlust = kalorien_defizit * 0.000129  #Nur ein BSP

      
        features = np.array([[aktuelles_gewicht, zielgewicht, kalorienaufnahme, kalorienverbrauch, verbleibende_tage, tagesverlust, aktivitaetslevel]])

     
        predicted_gewicht = model.predict(features)[0]
        tage_bis_ziel = (aktuelles_gewicht - zielgewicht) / tagesverlust

       
        return JsonResponse({
            'predicted_weight': predicted_gewicht,
            'tage_bis_ziel': tage_bis_ziel
        })


