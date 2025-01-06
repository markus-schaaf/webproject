import pickle
import numpy as np
from flask import Flask, request, jsonify

# Lade das Modell
with open('gewichtsverlust_modell.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Hole die Formulardaten
    data = request.get_json()

    # Extrahiere die relevanten Daten aus dem Request
    aktuelles_gewicht = float(data['aktuelles_gewicht'])
    zielgewicht = float(data['zielgewicht'])
    kalorienaufnahme = float(data['kalorienaufnahme'])
    kalorienverbrauch = float(data['kalorienverbrauch'])
    verbleibende_tage = int(data['verbleibende_tage'])
    aktivitaetslevel = float(data['aktivitaetslevel'])

    # Berechne den täglichen Kalorienüberschuss oder -defizit
    kalorien_defizit = kalorienverbrauch - kalorienaufnahme

    # Berechne das tägliche Gewicht, das du verlieren könntest
    tagesverlust = kalorien_defizit * 0.000129

    # Feature-Vektor für das Modell
    features = np.array([[aktuelles_gewicht, zielgewicht, kalorienaufnahme, kalorienverbrauch, verbleibende_tage, tagesverlust, aktivitaetslevel]])

    # Treffen einer Vorhersage
    predicted_gewicht = model.predict(features)[0]
    
    # Berechne, wie viele Tage es dauert, das Zielgewicht zu erreichen
    tage_bis_ziel = (aktuelles_gewicht - zielgewicht) / tagesverlust

    # Gebe die Ergebnisse als JSON zurück
    return jsonify({
        'predicted_weight': predicted_gewicht,
        'tage_bis_ziel': tage_bis_ziel
    })

if __name__ == '__main__':
    app.run(debug=True)