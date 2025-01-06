import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib


data = pd.read_csv('gewichtsverlust.csv')


X = data[['Aktuelles Gewicht (kg)', 'Kalorienaufnahme (kcal)', 'Kalorienverbrauch (kcal)', 'Verbleibende Tage']] 
y = data['Gewichtsverlust (kg)']  


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LinearRegression()


model.fit(X_train, y_train)


y_pred = model.predict(X_test)


mse = mean_squared_error(y_test, y_pred)
print(f"Mittlere quadratische Abweichung (MSE): {mse}")


joblib.dump(model, 'gewichtsverlust_modell.pkl')
print("Das Modell wurde erfolgreich gespeichert.")

