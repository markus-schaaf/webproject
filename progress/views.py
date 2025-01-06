from django.shortcuts import render
from django.http import JsonResponse
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from datetime import timedelta


# Fortschrittstracker-View
def progress_home(request):
    
    new_target_time = timedelta(days=15)

    return render(request, "progress.html", {"new_target_time": new_target_time})

# Gewichtsvorhersage-View
def predict_progress(request):
    try:
        # Hole die Werte aus der Anfrage
        current_weight = request.GET.get('current_weight', 0)
        target_weight = request.GET.get('target_weight', 0)
        days_remaining = request.GET.get('days_remaining', 0)

        # Konvertiere die Werte in Ganzzahlen und überprüfe auf Fehler
        current_weight = int(current_weight)
        target_weight = int(target_weight)
        days_remaining = int(days_remaining)

        # Berechnung oder weitere Verarbeitung
        prediction = {
            'current_weight': current_weight,
            'target_weight': target_weight,
            'days_remaining': days_remaining,
            # Beispielberechnung: durchschnittliche tägliche Abnahme erforderlich
            'daily_change_needed': round((current_weight - target_weight) / days_remaining, 2) if days_remaining > 0 else None,
        }

        return JsonResponse(prediction)

    except ValueError as e:
        # Falls ein Wert keine gültige Zahl ist
        return JsonResponse({'error': 'Invalid input. Please provide numeric values.', 'details': str(e)}, status=400)

    except ZeroDivisionError:
        # Falls `days_remaining` = 0 ist und eine Division durchgeführt wurde
        return JsonResponse({'error': 'Days remaining cannot be zero.'}, status=400)

    except Exception as e:
        # Allgemeine Fehlerbehandlung
        return JsonResponse({'error': 'An unexpected error occurred.', 'details': str(e)}, status=500)


# Simulierte Trainingsdaten
data = {
    "Kalorienaufnahme": [2000, 2200, 2100, 2000, 2300, 1900, 2500, 2000, 2100, 2200],
    "Kalorienverbrauch": [2500, 2400, 2600, 2500, 2400, 2700, 2200, 2500, 2600, 2400],
    "Gewicht": [80, 79.8, 79.7, 79.6, 79.8, 79.4, 79.5, 79.3, 79.2, 79.4]
}

# Linear Regression für Gewichtsvorhersage
df = pd.DataFrame(data)
X = df[["Kalorienaufnahme", "Kalorienverbrauch"]]
y = df["Gewicht"]
model = LinearRegression()
model.fit(X, y)

# Reinforcement Learning Variablen
reward_history = []

# Reinforcement Learning - Belohnung basierend auf Kaloriendefizit
def calculate_reward(kalorienaufnahme, kalorienverbrauch):
    defizit = kalorienverbrauch - kalorienaufnahme
    reward = 0
    
    # Belohnung für Kaloriendefizit
    if defizit > 0:
        reward = defizit * 0.1  # Positive Belohnung für Defizit
    else:
        reward = defizit * -0.1  # Negative Belohnung für Überschuss
    return reward

from django.http import JsonResponse
def predict_progress(request):
    # Hole die Werte aus der Anfrage (POST statt GET)
    current_weight = request.POST.get('current_weight')
    target_weight = request.POST.get('target_weight')
    days_remaining = request.POST.get('days_remaining')
    kalorienaufnahme = request.POST.get('kalorienaufnahme')
    kalorienverbrauch = request.POST.get('kalorienverbrauch')

    # Überprüfe, ob Werte vorhanden sind und setze Standardwerte für None
    if current_weight is None or current_weight == "":
        current_weight = 0
    else:
        current_weight = int(current_weight)
    
    if target_weight is None or target_weight == "":
        target_weight = 0
    else:
        target_weight = int(target_weight)

    if days_remaining is None or days_remaining == "":
        days_remaining = 0
    else:
        days_remaining = int(days_remaining)

    if kalorienaufnahme is None or kalorienaufnahme == "":
        kalorienaufnahme = 0
    else:
        kalorienaufnahme = int(kalorienaufnahme)

    if kalorienverbrauch is None or kalorienverbrauch == "":
        kalorienverbrauch = 0
    else:
        kalorienverbrauch = int(kalorienverbrauch)

    # Berechnung der Kalorienbilanz
    kalorienbilanz = kalorienaufnahme - kalorienverbrauch

    if kalorienbilanz >= 0:
        # Wenn Kalorienbilanz >= 0, kein Gewichtsverlust
        predicted_weight = current_weight
        new_target_time = 0  # Keine Veränderung möglich
    else:
        # Berechne die tägliche Gewichtveränderung (in kg)
        taegliche_gewichtveraenderung = kalorienbilanz / 7700.0

        # Berechne die gesamte Gewichtveränderung in den verbleibenden Tagen
        gewichtveraenderung = taegliche_gewichtveraenderung * days_remaining

        # Berechne das vorhergesagte Gewicht
        predicted_weight = current_weight + gewichtveraenderung

        # Berechne die angepasste Zielzeit (Tage bis Zielgewicht)
        if current_weight > target_weight:
            # Berechne die verbleibenden Tage bis zum Zielgewicht
            new_target_time = (current_weight - target_weight) * 7700.0 / abs(kalorienbilanz)
        else:
            # Wenn das Zielgewicht bereits erreicht ist, keine weiteren Tage nötig
            new_target_time = 0

    # Bereite die Antwort vor und runde auf zwei Dezimalstellen
    prediction = {
        'current_weight': current_weight,
        'target_weight': target_weight,
        'days_remaining': days_remaining,
        'predicted_weight': round(predicted_weight, 2),
        'tage_bis_ziel': round(new_target_time, 2),  # Keine unendliche Zahl mehr
    }

    return JsonResponse(prediction)















def generate_recommendations(kalorienaufnahme, kalorienverbrauch):
    """Generiert spezifische Empfehlungen basierend auf den Eingabedaten."""
    defizit = kalorienverbrauch - kalorienaufnahme
    
    # Beispielempfehlung basierend auf Kaloriendefizit
    if defizit > 500:
        return "Gut gemacht! Versuche, weiterhin für mehr als 500 kcal Defizit zu sorgen, um dein Ziel noch schneller zu erreichen."
    elif defizit < 0:
        return "Du hast ein Kalorienüberschuss! Versuche, deinen Kalorienverbrauch zu erhöhen oder die Aufnahme zu reduzieren."
    else:
        return "Halte deinen Kalorienverbrauch und deine Aufnahme im Gleichgewicht, um dein Ziel sicher zu erreichen."
    
def progress_home(request):
    """Zeigt die Fortschrittstracker-Seite an und gibt Empfehlungen."""
    kalorienaufnahme = 2200  # Hier solltest du die Eingabe des Nutzers verwenden
    kalorienverbrauch = 2400  # Hier solltest du die Eingabe des Nutzers verwenden
    
    # Generiere Empfehlungen basierend auf den Daten
    recommendation = generate_recommendations(kalorienaufnahme, kalorienverbrauch)
    
    return render(request, "progress/progress.html", {"recommendation": recommendation})

def adjust_target_time(kalorienaufnahme, kalorienverbrauch, gewicht):
    """Passen die Zielzeit basierend auf den Fortschritten des Nutzers an."""
    defizit = kalorienverbrauch - kalorienaufnahme
    if defizit > 0:
        # Wenn der Nutzer einen Kaloriendefizit erreicht, kann das Ziel schneller erreicht werden
        target_adjustment = 0.9  # Zielt darauf ab, das Ziel schneller zu erreichen
    else:
        target_adjustment = 1.1  # Das Ziel wird langsamer erreicht
    new_target_time = gewicht / defizit * target_adjustment
    return round(new_target_time, 2)

def progress_home(request):
    """Zeigt die Fortschrittstracker-Seite an und gibt die angepasste Zielzeit zurück."""
    kalorienaufnahme = 2200  # Hier solltest du die Eingabe des Nutzers verwenden
    kalorienverbrauch = 2400  # Hier solltest du die Eingabe des Nutzers verwenden
    gewicht = 80  # Hier solltest du das aktuelle Gewicht des Nutzers verwenden
    
    # Berechne die angepasste Zielzeit
    new_target_time = adjust_target_time(kalorienaufnahme, kalorienverbrauch, gewicht)
    
    return render(request, "progress/progress.html", {"new_target_time": new_target_time})


