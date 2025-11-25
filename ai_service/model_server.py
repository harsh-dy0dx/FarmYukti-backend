import os
import json
import random
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

app = Flask(__name__)

# File path to save the trained model
MODEL_FILE = 'crop_recommendation_model.pkl'

# --- 1. DATA GENERATION & TRAINING LOGIC ---
def train_model():
    """
    Generates synthetic agricultural data based on real-world scientific ranges
    and trains a Random Forest Classifier.
    """
    print("Training new AI model from synthetic data...")
    
    # Define crop profiles: Approximate ranges for Nitrogen, Phosphorus, Potassium, pH, Rainfall
    crop_profiles = {
        'rice': {'n': (60, 90), 'p': (35, 60), 'k': (35, 45), 'ph': (5.0, 7.8), 'rain': (150, 250)},
        'maize': {'n': (60, 100), 'p': (30, 60), 'k': (15, 25), 'ph': (5.5, 7.0), 'rain': (60, 100)},
        'chickpea': {'n': (20, 60), 'p': (50, 80), 'k': (70, 90), 'ph': (6.0, 7.5), 'rain': (60, 90)},
        'kidneybeans': {'n': (10, 40), 'p': (50, 80), 'k': (15, 25), 'ph': (5.5, 6.5), 'rain': (60, 120)},
        'pigeonpeas': {'n': (10, 40), 'p': (50, 80), 'k': (15, 25), 'ph': (4.5, 7.0), 'rain': (80, 150)},
        'mothbeans': {'n': (0, 40), 'p': (30, 60), 'k': (15, 25), 'ph': (3.5, 9.0), 'rain': (30, 70)},
        'mungbean': {'n': (0, 40), 'p': (30, 60), 'k': (15, 25), 'ph': (6.0, 7.5), 'rain': (30, 60)},
        'blackgram': {'n': (20, 60), 'p': (50, 80), 'k': (15, 25), 'ph': (6.5, 7.8), 'rain': (60, 80)},
        'lentil': {'n': (0, 40), 'p': (50, 80), 'k': (15, 25), 'ph': (5.8, 7.0), 'rain': (35, 60)},
        'pomegranate': {'n': (10, 50), 'p': (5, 30), 'k': (35, 45), 'ph': (5.5, 7.2), 'rain': (100, 120)},
        'banana': {'n': (80, 120), 'p': (70, 95), 'k': (45, 55), 'ph': (5.5, 6.5), 'rain': (90, 120)},
        'mango': {'n': (0, 40), 'p': (15, 40), 'k': (25, 35), 'ph': (4.5, 6.5), 'rain': (80, 100)},
        'grapes': {'n': (0, 50), 'p': (120, 145), 'k': (195, 205), 'ph': (5.5, 6.5), 'rain': (60, 80)},
        'watermelon': {'n': (80, 120), 'p': (5, 30), 'k': (45, 55), 'ph': (6.0, 7.0), 'rain': (40, 60)},
        'muskmelon': {'n': (80, 120), 'p': (5, 30), 'k': (45, 55), 'ph': (6.0, 6.8), 'rain': (40, 60)},
        'apple': {'n': (0, 40), 'p': (120, 145), 'k': (195, 205), 'ph': (5.5, 6.5), 'rain': (100, 120)},
        'orange': {'n': (0, 40), 'p': (5, 30), 'k': (5, 15), 'ph': (6.0, 7.5), 'rain': (100, 120)},
        'papaya': {'n': (30, 70), 'p': (40, 70), 'k': (45, 55), 'ph': (6.0, 7.0), 'rain': (100, 200)},
        'coconut': {'n': (0, 40), 'p': (5, 30), 'k': (25, 35), 'ph': (5.0, 6.5), 'rain': (150, 250)},
        'cotton': {'n': (100, 140), 'p': (35, 60), 'k': (15, 25), 'ph': (5.5, 7.5), 'rain': (60, 100)},
        'jute': {'n': (60, 100), 'p': (35, 60), 'k': (35, 45), 'ph': (6.0, 7.5), 'rain': (150, 200)},
        'coffee': {'n': (80, 120), 'p': (15, 40), 'k': (25, 35), 'ph': (6.0, 7.5), 'rain': (120, 200)},
    }

    data = []
    labels = []
    
    # Generate 100 synthetic samples per crop to train the model
    for crop, profile in crop_profiles.items():
        for _ in range(100):
            n = random.uniform(*profile['n'])
            p = random.uniform(*profile['p'])
            k = random.uniform(*profile['k'])
            ph = random.uniform(*profile['ph'])
            rain = random.uniform(*profile['rain'])
            
            # Simulated Temperature and Humidity (Generic reasonable ranges)
            temp = random.uniform(20, 35) 
            hum = random.uniform(40, 90)

            # Feature Order: [N, P, K, Temp, Humidity, pH, Rainfall]
            data.append([n, p, k, temp, hum, ph, rain])
            labels.append(crop)

    X = np.array(data)
    y = np.array(labels)

    # Split and Train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=20)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"Model trained successfully! Accuracy: {accuracy:.2f}")
    
    # Save the model to disk so we don't have to retrain every time
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)
    
    return model

# Load Model on Startup (or train if missing)
if os.path.exists(MODEL_FILE):
    try:
        with open(MODEL_FILE, 'rb') as f:
            model = pickle.load(f)
            print("Model loaded from disk.")
    except:
        model = train_model()
else:
    model = train_model()

# --- 2. API ENDPOINTS ---

@app.route('/predict_crop', methods=['POST'])
def predict_crop():
    """
    Endpoint for Crop Recommendation
    Input JSON: { "nitrogen": 90, "phosphorus": 42, "potassium": 43, "phLevel": 6.5, "rainfall": 200, "temperature": 25, "humidity": 70 }
    """
    try:
        data = request.json
        
        # Features must match training order: [N, P, K, temp, hum, ph, rain]
        features = [[
            float(data.get('nitrogen')),
            float(data.get('phosphorus')),
            float(data.get('potassium')),
            float(data.get('temperature', 25.0)), # Default to 25C if missing
            float(data.get('humidity', 60.0)),    # Default to 60% if missing
            float(data.get('phLevel')),
            float(data.get('rainfall'))
        ]]
        
        # Get the single best prediction
        prediction = model.predict(features)[0]
        
        # Get probabilities to suggest alternatives (top 3)
        probabilities = model.predict_proba(features)[0]
        top3_indices = np.argsort(probabilities)[-3:][::-1]
        top3_crops = [model.classes_[i] for i in top3_indices]
        
        return jsonify({
            "recommended_crop": prediction,
            "alternatives": top3_crops,
            "message": "Success"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/predict_fertilizer', methods=['POST'])
def predict_fertilizer():
    """
    Endpoint for Fertilizer Recommendation.
    Uses a hybrid Rule-Based approach since fertilizer logic is strictly chemical.
    """
    try:
        data = request.json
        n = float(data.get('nitrogen'))
        p = float(data.get('phosphorus'))
        k = float(data.get('potassium'))
        
        recs = []
        
        # Logic for Nitrogen
        if n < 50:
            recs.append("Urea (High N)")
        elif n > 140:
            recs.append("Avoid Nitrogen fertilizers")

        # Logic for Phosphorus
        if p < 20:
            recs.append("Super Phosphate (High P)")
            recs.append("DAP (Di-ammonium Phosphate)")
        
        # Logic for Potassium
        if k < 20:
            recs.append("Muriate of Potash (High K)")
        
        # General Advice
        if not recs:
            recs.append("NPK 19:19:19 (Balanced)")
            
        return jsonify({
            "recommended_fertilizer": recs,
            "message": "Based on NPK soil analysis"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Run the server on Port 5000
    print("Starting Python AI Server on port 5000...")
    app.run(port=5000, debug=True)
